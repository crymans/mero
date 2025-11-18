# import requests
# import json

# BASE_URL = "http://localhost:8000/api/v1"

# # Создаем пользователя
# user_data = {
#     "telegram_id": "123456789",
#     "username": "test_user",
#     "first_name": "Иван",
#     "last_name": "Тестов",
#     "phone": "+79123456789"
# }

# response = requests.post(f"{BASE_URL}/users/", json=user_data)
# user = response.json()
# print("Создан пользователь:", user)

# # Создаем билет
# ticket_data = {
#     "user_id": user["id"],
#     "price": 1000.0
# }

# response = requests.post(f"{BASE_URL}/tickets/", json=ticket_data)
# ticket = response.json()
# print("Создан билет:", ticket)

# # Получаем продукты
# response = requests.get(f"{BASE_URL}/products/")
# products = response.json()
# print("Доступные продукты:", products)

# # Создаем заказ
# if products:
#     order_data = {
#         "user_id": user["id"],
#         "product_id": products[0]["id"],
#         "quantity": 2
#     }
    
#     response = requests.post(f"{BASE_URL}/orders/", json=order_data)
#     order = response.json()
#     print("Создан заказ:", order)

import requests
print(requests.get('http://127.0.0.1:8000/docs#/').json())