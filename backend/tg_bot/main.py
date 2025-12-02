from .router import user_router
from .create_bot import bot, dp
import asyncio

gift_relayer = 7969223738

async def main():
    await bot.refund_star_payment(971495895, 'stx2QdLvPcjq6kO1-F45co3sddQQQecVoMwuSlSjiVKgTCUg3GcNufp07WanxkI03FETIsx1oTWq1f7WBx8ot2W3FB4lPGJqiBQxybt2PajiUnPIxTW0EXDJpTxmTs_N-gU')
    dp.include_router(user_router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
            

if __name__ == '__main__':
    asyncio.run(main())