# app/init_data.py
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.database import AsyncSessionLocal
import asyncio

async def init_test_data():
    """Инициализация тестовых данных при запуске приложения"""
    async with AsyncSessionLocal() as db:
        try:
            print("🔄 Инициализация тестовых данных...")
            
            # 1. Создаем тестового админа
            admin_data = schemas.UserCreate(
                id="admin",
                username="admin_user",
                first_name="Администратор",
                last_name="Системный",
                phone="+79181112233"
            )
            
            try:
                admin_user = await crud.create_user(db, admin_data)
                print(admin_user)
                # Обновляем роль на admin
                await crud.update_user_role(db, "admin", "admin")
                print("✅ Тестовый админ создан")
            except crud.CRUDError as e:
                if "already exists" in str(e):
                    print("ℹ️ Админ уже существует")
                else:
                    raise e

            # 2. Создаем тестовые продукты
            test_products = [
                {
                    "name": "Jack Daniels",
                    "description": "Классический виски с карамельными нотами",
                    "price": 350.0,
                    "category": "drink",
                    "count": 50,
                    "is_for_table": False,
                    "image_url": None
                },
                {
                    "name": "Jameson",
                    "description": "Ирландский виски с мягким вкусом",
                    "price": 320.0,
                    "category": "drink",
                    "count": 40,
                    "is_for_table": False,
                    "image_url": None
                },
                {
                    "name": "Red Bull",
                    "description": "Энергетический напиток",
                    "price": 200.0,
                    "category": "drink",
                    "count": 100,
                    "is_for_table": False,
                    "image_url": None
                },
                {
                    "name": "Coca-Cola",
                    "description": "Классическая газировка",
                    "price": 150.0,
                    "category": "drink",
                    "count": 100,
                    "is_for_table": False,
                    "image_url": None
                },
                {
                    "name": "Бургер",
                    "description": "Сочный бургер с говядиной и овощами",
                    "price": 450.0,
                    "category": "food",
                    "count": 30,
                    "is_for_table": False,
                    "image_url": None
                },
                {
                    "name": "Картофель фри",
                    "description": "Хрустящий картофель с солью",
                    "price": 200.0,
                    "category": "food",
                    "count": 50,
                    "is_for_table": False,
                    "image_url": None
                },
                {
                    "name": "Куриные крылья",
                    "description": "Острые куриные крылья в соусе",
                    "price": 350.0,
                    "category": "food",
                    "count": 25,
                    "is_for_table": False,
                    "image_url": None
                },
                {
                    "name": "Салат Цезарь",
                    "description": "Классический салат с курицей и соусом цезарь",
                    "price": 300.0,
                    "category": "food",
                    "count": 20,
                    "is_for_table": False,
                    "image_url": None
                },
                {
                    "name": "VIP Бутылка шампанского",
                    "description": "Премиальное шампанское для VIP гостей",
                    "price": 2500.0,
                    "category": "drink",
                    "count": 10,
                    "is_for_table": True,
                    "image_url": None
                },
                {
                    "name": "Фруктовая тарелка",
                    "description": "Свежие фрукты для стола",
                    "price": 800.0,
                    "category": "food",
                    "count": 15,
                    "is_for_table": True,
                    "image_url": None
                }
            ]

            products_created = 0
            for product_data in test_products:
                try:
                    product_schema = schemas.ProductCreate(**product_data)
                    await crud.create_product(db, product_schema)
                    products_created += 1
                except crud.CRUDError as e:
                    if "already exists" not in str(e):
                        print(f"⚠️ Ошибка при создании продукта {product_data['name']}: {e}")

            print(f"✅ Создано {products_created} тестовых продуктов")

            # 3. Создаем тестовых пользователей с разными ролями
            test_users = [
                {
                    "id": "officiant_1",
                    "username": "officiant_user",
                    "first_name": "Анна",
                    "last_name": "Официантова",
                    "phone": "+79182223344",
                    "role": "officiant"
                },
                {
                    "id": "chef_1",
                    "username": "chef_user",
                    "first_name": "Иван",
                    "last_name": "Поваров",
                    "phone": "+79183334455",
                    "role": "chef"
                },
                {
                    "id": "qr_1",
                    "username": "qr_user",
                    "first_name": "Петр",
                    "last_name": "Сканеров",
                    "phone": "+79184445566",
                    "role": "qr"
                },
                {
                    "id": "vip_user",
                    "username": "vip_client",
                    "first_name": "Мария",
                    "last_name": "VIP",
                    "phone": "+79185556677",
                    "role": "vip"
                },
                {
                    "id": "regular_user",
                    "username": "regular_client",
                    "first_name": "Алексей",
                    "last_name": "Обычный",
                    "phone": "+79186667788",
                    "role": "member"
                }
            ]

            users_created = 0
            for user_data in test_users:
                try:
                    user_create = schemas.UserCreate(
                        id=user_data["id"],
                        username=user_data["username"],
                        first_name=user_data["first_name"],
                        last_name=user_data["last_name"],
                        phone=user_data["phone"]
                    )
                    user = await crud.create_user(db, user_create)
                    await crud.update_user_role(db, user_data["id"], user_data["role"])
                    users_created += 1
                except crud.CRUDError as e:
                    if "already exists" not in str(e):
                        print(f"⚠️ Ошибка при создании пользователя {user_data['id']}: {e}")

            print(f"✅ Создано {users_created} тестовых пользователей")

            # 4. Создаем тестовые билеты для некоторых пользователей
            test_tickets = [
                {
                    "user_telegram_id": "vip_user",
                    "qr_code": "VIP_TICKET_001",
                    "price": 1300.0
                },
                {
                    "user_telegram_id": "regular_user",
                    "qr_code": "STANDARD_TICKET_001",
                    "price": 500.0
                }
            ]

            tickets_created = 0
            for ticket_data in test_tickets:
                try:
                    user = await crud.get_user_by_telegram_id(db, ticket_data["user_telegram_id"])
                    if user:
                        ticket_create = schemas.TicketCreate(
                            qr_code=ticket_data["qr_code"],
                            price=ticket_data["price"]
                        )
                        await crud.create_ticket(db, ticket_create, user.id)
                        tickets_created += 1
                except crud.CRUDError as e:
                    if "already has a ticket" not in str(e):
                        print(f"⚠️ Ошибка при создании билета для {ticket_data['user_telegram_id']}: {e}")

            print(f"✅ Создано {tickets_created} тестовых билетов")

            print("🎉 Инициализация тестовых данных завершена!")

        except Exception as e:
            print(f"❌ Ошибка при инициализации тестовых данных: {e}")
            raise