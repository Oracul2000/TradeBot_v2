from ui.telegram.telegram import bot
from database.init import init_db
import asyncio


init_db()
asyncio.run(bot.main())