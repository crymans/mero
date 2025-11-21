from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ContentType, PreCheckoutQuery
from app.crud import operations_with_user_stars
from app.database import AsyncSessionLocal
from .create_bot import bot
import logging, json

logger = logging.getLogger('bot')

user_router = Router()

@user_router.pre_checkout_query()
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@user_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(msg: Message):
    try:
        amount = msg.successful_payment.invoice_payload.lower()
        price = int(msg.successful_payment.total_amount)
        transaction = msg.successful_payment.telegram_payment_charge_id
        is_error = 0

        stars_to_add = price
        async with AsyncSessionLocal() as db:
            if not await operations_with_user_stars(db, msg.from_user.id, stars_to_add, '+'):
                is_error = 1
                print(f'User:{msg.from_user.id} Purchase ERRROR stars:{price} added')    
            else:
                await msg.answer(f'''Ваш баланс успешно пополнен на {stars_to_add} stars!\n\n''')
    
    except Exception as e:
        logger.critical(f'User:{msg.from_user.id} Purchase stars:{price} error: {e}')

@user_router.message(CommandStart())
async def start(msg: Message):
    try:
        await msg.answer(f'''Привет! 👋\n\nРады видеть тебя на нашем мероприятии!\n\n🗓 13 декабря\n
📍 Улица Московская 64\n
⏰ С 16:00 до 05:00\n\n
Билет можно преобрести в мини приложении\n
Приходи за яркими впечатлениями! ✨''')
    except:
        pass