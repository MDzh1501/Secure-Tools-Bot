from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select
from .models import User, Password
from dotenv import load_dotenv
from tools.password_manager import encrypt_pwd, decrypt_pwd
import os

load_dotenv()

LINK_DB = os.getenv('LINK_DB')


class DBRequestsHandler:
    engine = create_async_engine(url=LINK_DB)
    session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

    @staticmethod
    def connection(method):
        async def wrapper(*args, **kwargs):
            async with DBRequestsHandler.session_maker() as session:
                try:
                    return await method(*args, session=session, **kwargs)
                except Exception as e:
                    await session.rollback()
                    raise e
        return wrapper

    @connection
    async def add_user(self, tg_id: int, session: AsyncSession):
        new_user = User(tg_id=tg_id)
        session.add(new_user)
        await session.commit()

    @connection
    async def add_password_for_user(self, tg_id: int, encrypted_pwd: str, salt: str, description: str, session: AsyncSession):
        user = await self._get_user(tg_id, session=session)
        if not user:
            raise ValueError(f"User with tg_id={tg_id} not found")

        new_password = Password(
            encrypted_pwd=encrypted_pwd,
            salt=salt,
            description=description,
            user=user
        )

        session.add(new_password)
        await session.commit()

    async def store_user_password(self, tg_id: int, plain_pwd: str, description: str):
        """Encrypt and store a password for a user."""
        encrypted = encrypt_pwd(plain_pwd)

        await self.add_password_for_user(
            tg_id=tg_id,
            encrypted_pwd=encrypted["encrypted"],
            salt=encrypted["salt"],
            description=description
        )
    
    @connection
    async def delete_password(self, tg_id: int, pwd_id: int, session: AsyncSession):
        """Delete a specific password belonging to a user by password id."""
        user = await self._get_user(tg_id, session=session)
        if not user:
            return None

        stmt = select(Password).where(
            Password.id == pwd_id,
            Password.user_id == user.id
        )
        result = await session.execute(stmt)
        password_entry = result.scalar_one_or_none()

        if not password_entry:
            return False

        await session.delete(password_entry)
        await session.commit()
        return True
    
    # @connection
    # async def update_password(self, tg_id: int, session: AsyncSession):
    #     """Delete password, created by the user user"""
    #     user = await self._get_user(tg_id, session=session)
    #     if not user:
    #         return None
        
    #     if user.password:
    #         await session.delete(user.password)
    #         await session.commit()
    #         return True

    #     return False
    
    @connection
    async def get_decrypted_password_selection_map(self, tg_id: int, session: AsyncSession):
        user = await self._get_user(tg_id, session=session)
        if not user:
            return {}

        stmt = select(Password).where(Password.user_id == user.id)
        result = await session.execute(stmt)
        passwords = result.scalars().all()

        selection_map = {}

        for i, pwd_entry in enumerate(passwords, start=1):
            try:
                decrypted = decrypt_pwd(pwd_entry.encrypted_pwd, pwd_entry.salt)
            except Exception:
                decrypted = "[decryption failed]"

            selection_map[i] = {
                "id": pwd_entry.id,
                "description": pwd_entry.description,
                "password": decrypted
            }

        return selection_map
        
    async def _get_user(self, tg_id: int, session: AsyncSession):
        query = select(User).filter(User.tg_id == tg_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
