# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.init_data import init_test_data
from app.routers import users, tickets, orders, products, admin
from .middleware import register_middleware

app = FastAPI(title="Event Management API", docs_url='/rostov_api/')

# Настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://localhost:3001",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # Инициализируем базу данных
    await init_db()
    
    # Инициализируем тестовые данные
    await init_test_data()

app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(orders.router)
app.include_router(products.router)
app.include_router(admin.router)
register_middleware(app)

@app.get("/")
async def root():
    return {"message": "Event Management API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}