from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from typing import Callable, Any, Dict, Awaitable
from app.database.requests import DBRequestsHandler
from sqlalchemy.exc import IntegrityError


class UserInitMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        state: FSMContext = data.get("state")
        db = DBRequestsHandler()

        if state is None or db is None:
            # Якщо немає контексту FSM або DB - просто викликаємо хендлер
            return await handler(event, data)

        data_state = await state.get_data()
        if not data_state.get("started"):
            # Ініціалізуємо користувача
            try:
                await db.add_user(event.from_user.id)
                await state.update_data(started=True)
            except IntegrityError:
                await state.update_data(started=True)

        return await handler(event, data)