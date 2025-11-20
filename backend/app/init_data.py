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
                telegram_id="971495895",
                username="admin_user",
                first_name="Администратор",
                last_name="Системный",
                phone="+79181112233"
            )
            
            try:
                admin_user = await crud.create_user(db, admin_data)
                print(admin_user)
                # Обновляем роль на admin
                await crud.update_user_role(db, "971495895", "admin")
                print("✅ Тестовый админ создан")
            except crud.CRUDError as e:
                if "already exists" in str(e):
                    print("ℹ️ Админ уже существует")
                else:
                    raise e

            # 2. Создаем тестовые продукты
            test_products = [
            {
                "name": "9 шотов из ликера",
                "description": "3 малина, 3 апельсин, 3 мандарин",
                "price": 1800,
                "category": "drink",
                "count": 100,
                "is_for_table": True,
                "image_url": "https://img.freepik.com/free-photo/assorted-color-liqueur-shots-glasses_140725-282.jpg"
            },
            {
                "name": "Хот-Дог",
                "description": "Сочный хот-дог с мясной сосиской",
                "price": 250.0,
                "category": "food",
                "count": 50,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/hot-dog-with-mustard-ketchup_1339-998.jpg"
            },
            {
                "name": "Мясная тарелка",
                "description": "Ассорти колбас, украшенных зеленью",
                "price": 500,
                "category": "food",
                "count": 50,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/assorted-sliced-sausages-wooden-board_114579-7620.jpg"
            },
            {
                "name": "Сырная тарелка",
                "description": "Ассорти сыров",
                "price": 500,
                "category": "food",
                "count": 50,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/cheese-plate-with-various-types-cheese_1150-5762.jpg"
            },
            {
                "name": "Сырная + Мясная",
                "description": "Ассорти сыров, колбас",
                "price": 800,
                "category": "food",
                "count": 50,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/cheese-meat-platter-with-grapes_114579-24079.jpg"
            },
            {
                "name": "27 шотов из ликера",
                "description": "9 малина, 9 апельсин, 9 мандарин",
                "price": 500,
                "category": "drink",
                "count": 100,
                "is_for_table": True,
                "image_url": "https://img.freepik.com/free-photo/multiple-colored-liqueur-shots_140725-280.jpg"
            },
            {
                "name": "Ликер апельсин",
                "description": "Апельсиновый ликер",
                "price": 250,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/orange-liqueur-glass_1339-1104.jpg"
            },
            {
                "name": "Отвертка",
                "description": "Водка с апельсиновым соком",
                "price": 350.0,
                "category": "drink",
                "count": 50,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/screwdriver-cocktail-glass_140725-1041.jpg"
            },
            {
                "name": "Виски-кола",
                "description": "Виски с колой :)",
                "price": 350.0,
                "category": "drink",
                "count": 40,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/whiskey-coke-drink-glass_1339-1006.jpg"
            },
            {
                "name": "Куба Либре",
                "description": "Виски, кола, лайм",
                "price": 370.0,
                "category": "drink",
                "count": 40,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/cuba-libre-cocktail-with-lime_140725-1053.jpg"
            },
            {
                "name": "Ёрш",
                "description": "Водка, пиво",
                "price": 300.0,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/beer-vodka-cocktail-glass_140725-1038.jpg"
            },
            {
                "name": "Ликер малина",
                "description": "Малиновый ликер",
                "price": 250,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/raspberry-liqueur-glass_1339-1106.jpg"
            },
            {
                "name": "Ликер мандарин",
                "description": "Мандариновый ликер",
                "price": 250,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/tangerine-liqueur-glass_1339-1107.jpg"
            },
            {
                "name": "Виски",
                "description": "Виски в стакане",
                "price": 350,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/whiskey-glass-with-ice_140725-1029.jpg"
            },
            {
                "name": "Коньяк",
                "description": "Коньяк в стакане",
                "price": 350,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/cognac-glass_1339-1098.jpg"
            },
            {
                "name": "Пиво",
                "description": "Пиво 0.5л светлое",
                "price": 200,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/glass-beer-with-foam_140725-1179.jpg"
            },
            {
                "name": "Пиво",
                "description": "Пиво 0.5л темное",
                "price": 200,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/dark-beer-glass_1339-1120.jpg"
            },
            {
                "name": "Энергетик",
                "description": "Энергетик на выбор",
                "price": 200,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/energy-drink-can_1339-1132.jpg"
            },
            {
                "name": "Сок",
                "description": "Сок 250мл в асссортименте",
                "price": 150,
                "category": "drink",
                "count": 100,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/fruit-juices-glasses_140725-295.jpg"
            },
            {
                "name": "Вода",
                "description": "Вода 0.5л",
                "price": 70.0,
                "category": "drink",
                "count": 30,
                "is_for_table": False,
                "image_url": "https://img.freepik.com/free-photo/bottle-water-glass-ice_1339-1144.jpg"
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
                        await crud.create_ticket(db, ticket_create, user.telegram_id)
                        tickets_created += 1
                except crud.CRUDError as e:
                    if "already has a ticket" not in str(e):
                        print(f"⚠️ Ошибка при создании билета для {ticket_data['user_telegram_id']}: {e}")

            print(f"✅ Создано {tickets_created} тестовых билетов")

            print("🎉 Инициализация тестовых данных завершена!")

        except Exception as e:
            print(f"❌ Ошибка при инициализации тестовых данных: {e}")
            raise