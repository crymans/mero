from .router import user_router
from .create_bot import bot, dp
import asyncio

async def main():
    dp.include_router(user_router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
            

if __name__ == '__main__':
    asyncio.run(main())