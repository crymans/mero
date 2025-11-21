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
        "price": 1800.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://static.tildacdn.com/tild3333-6339-4361-a237-356565366533/photo.png",
        "id": 1
    },
    {
        "name": "Хот-Дог",
        "description": "Сочный хот-дог с мясной сосиской",
        "price": 250.0,
        "category": "food",
        "count": 50,
        "is_for_table": False,
        "image_url": "https://s.yimg.com/ny/api/res/1.2/GAetlObbVuGHwFwq7sFKKA--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyNDI7aD02OTc7Y2Y9d2VicA--/https://media.zenfs.com/en/food_republic_969/79a01c480d6e7a58fa81630239537c42",
        "id": 2
    },
    {
        "name": "Мясная тарелка",
        "description": "Ассорти колбас, украшенных зеленью",
        "price": 500.0,
        "category": "food",
        "count": 50,
        "is_for_table": False,
        "image_url": "https://avatars.mds.yandex.net/get-mpic/1673800/img_id2543626385768152155.jpeg/9hq",
        "id": 3
    },
    {
        "name": "Сырная тарелка",
        "description": "Ассорти сыров",
        "price": 500.0,
        "category": "food",
        "count": 50,
        "is_for_table": False,
        "image_url": "https://avatars.mds.yandex.net/i?id=a99592e5aeeeb5609d4a14b53116db92_l-5877103-images-thumbs&n=33&w=1242&h=1242",
        "id": 4
    },
    {
        "name": "Сырная + Мясная",
        "description": "Ассорти сыров, колбас",
        "price": 800.0,
        "category": "food",
        "count": 50,
        "is_for_table": False,
        "image_url": "https://i.pinimg.com/736x/0c/90/ad/0c90ad934876bc62b5e49c199c8eade2.jpg",
        "id": 5
    },
    {
        "name": "27 шотов из ликера",
        "description": "9 малина, 9 апельсин, 9 мандарин",
        "price": 500.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://png.pngtree.com/thumb_back/fh260/background/20230610/pngtree-group-of-shots-lined-up-with-liquor-and-shots-of-other-image_2898973.jpg",
        "id": 6
    },
    {
        "name": "Ликер апельсин",
        "description": "Апельсиновый ликер",
        "price": 250.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://artcafe-royal.ru/wp-content/uploads/e/1/4/e148ec239b598135d115167b8a1d86ae.jpeg",
        "id": 7
    },
    {
        "name": "Отвертка",
        "description": "Водка с апельсиновым соком",
        "price": 350.0,
        "category": "drink",
        "count": 50,
        "is_for_table": False,
        "image_url": "https://cdn.lifehacker.ru/wp-content/uploads/2018/11/shutterstock_1312434527_1576742288-e1576742317105-1140x570.jpg",
        "id": 8
    },
    {
        "name": "Виски-кола",
        "description": "Виски с колой :)",
        "price": 350.0,
        "category": "drink",
        "count": 40,
        "is_for_table": False,
        "image_url": "https://avatars.mds.yandex.net/get-sprav-products/5234963/2a0000018d0990fecdd9872ae39fa53f88db/M_height",
        "id": 9
    },
    {
        "name": "Куба Либре",
        "description": "Виски, кола, лайм",
        "price": 370.0,
        "category": "drink",
        "count": 40,
        "is_for_table": False,
        "image_url": "https://i.pinimg.com/originals/77/9d/b1/779db18387c80c8bbb6cfea83d29e60a.png",
        "id": 10
    },
    {
        "name": "Ёрш",
        "description": "Водка, пиво",
        "price": 300.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://i.pinimg.com/736x/0f/54/c9/0f54c9bc470874cd07ea31e3d38d61f7.jpg",
        "id": 11
    },
    {
        "name": "Ликер малина",
        "description": "Малиновый ликер",
        "price": 250.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://static.wixstatic.com/media/81cd5a_c709e51b68594cb29545a4a9c545c2d8~mv2.webp/v1/fit/w_500,h_500,q_90/file.webp",
        "id": 12
    },
    {
        "name": "Ликер мандарин",
        "description": "Мандариновый ликер",
        "price": 250.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://tvoirecepty.ru/files/imagecache/colorbox/recept/recept-liker-mandarinovyi-shag_5.jpg",
        "id": 13
    },
    {
        "name": "Виски",
        "description": "Виски в стакане",
        "price": 350.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://i.pinimg.com/originals/76/98/7c/76987c9e8161d72cd4884243d9c8328c.jpg",
        "id": 14
    },
    {
        "name": "Коньяк",
        "description": "Коньяк в стакане",
        "price": 350.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://i.pinimg.com/736x/41/6e/90/416e900a7b6d57ac3b60f163df9961a6.jpg",
        "id": 15
    },
    {
        "name": "Пиво",
        "description": "Пиво 0.5л светлое",
        "price": 200.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://avatars.mds.yandex.net/get-shedevrum/10502823/video_preview_886323cefdc711eea6cf16dfc2a2c98f_4/orig",
        "id": 16
    },
    {
        "name": "Энергетик",
        "description": "Энергетик на выбор",
        "price": 200.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://avatars.mds.yandex.net/i?id=192e9fbc6c746295e4608151b1cfa6a4_l-5225319-images-thumbs&n=13",
        "id": 17
    },
    {
        "name": "Сок",
        "description": "Сок 250мл в асссортименте",
        "price": 150.0,
        "category": "drink",
        "count": 100,
        "is_for_table": False,
        "image_url": "https://cdn.culture.ru/images/26cf7a87-ed42-56c6-baf2-41c89fce140f",
        "id": 18
    },
    {
        "name": "Вода",
        "description": "Вода 0.5л",
        "price": 70.0,
        "category": "drink",
        "count": 30,
        "is_for_table": False,
        "image_url": "https://img.freepik.com/free-photo/bottle-water-glass-ice_1339-1144.jpg",
        "id": 19
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