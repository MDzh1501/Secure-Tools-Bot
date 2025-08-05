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

    async def get_decrypted_passwords(self, tg_id: int):
        """Fetch and decrypt all stored passwords for a user."""
        password_entries = await self.get_passwords(tg_id)

        if not password_entries:
            return

        decrypted_passwords = []

        for entry in password_entries:
            decrypted = decrypt_pwd(entry.encrypted_pwd, entry.salt)
            decrypted_passwords.append({
                "description": entry.description,
                "password": decrypted
            })

        return decrypted_passwords

    @connection
    async def get_passwords(self, tg_id: int, session: AsyncSession):
        user = await self._get_user(tg_id, session=session)
        if not user:
            return None

        stmt = select(Password).filter(Password.user_id == user.id)
        result = await session.execute(stmt)
        return result.scalars().all()
                
    async def _get_user(self, tg_id: int, session: AsyncSession):
        query = select(User).filter(User.tg_id == tg_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
