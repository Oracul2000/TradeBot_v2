import asyncio

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram import Dispatcher, types
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import CommandStart
from aiogram.types import Message

import logging
import multiprocessing as mp
from typing import Callable, Dict, Any, Awaitable

from .backgroundtasks import *
from .config import *
from handlers import common, adduser, allusers, traidingpairs, addtraidingpair, start, apikeys, changedepo, closepos
from handlers import deletedata, getstatistics

class SomeMiddleware(BaseMiddleware):
    def __init__(self, allowed_users):
        super().__init__()
        self.allowed_users = allowed_users

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.chat.id
        if user_id not in self.allowed_users:
            return 0
        result = await handler(event, data)
        return result



async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(TOKEN)

    common.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    adduser.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    allusers.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    start.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    apikeys.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    changedepo.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    deletedata.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    closepos.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    getstatistics.router.message.middleware(SomeMiddleware(ALLOWED_USERS))

    traidingpairs.router.message.middleware(SomeMiddleware(ALLOWED_USERS))
    addtraidingpair.router.message.middleware(SomeMiddleware(ALLOWED_USERS))

    dp.include_router(common.router)
    dp.include_router(adduser.router)
    dp.include_router(allusers.router)
    dp.include_router(start.router)

    dp.include_router(traidingpairs.router)
    dp.include_router(addtraidingpair.router)
    dp.include_router(apikeys.router)
    dp.include_router(changedepo.router)
    dp.include_router(deletedata.router)
    dp.include_router(closepos.router)
    dp.include_router(getstatistics.router)

    asyncio.create_task(newreports(bot))

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())