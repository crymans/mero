# app/crud.py
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from app import models, schemas
from typing import List, Optional, Literal
from datetime import datetime, timedelta
import uuid

class CRUDError(Exception):
    pass

# User CRUD
async def get_user_by_telegram_id(db: AsyncSession, telegram_id: str):
    result = await db.execute(
        select(models.User).where(models.User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()

async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User).where(models.User.telegram_id == user_id)
    )
    return result.scalar_one_or_none()

async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.User).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    existing_user = await get_user_by_telegram_id(db, user.telegram_id)
    if existing_user:
        raise CRUDError("User already exists")
    
    db_user = models.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, telegram_id: str, user_update: schemas.UserUpdate):
    user = await get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise CRUDError("User not found")
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    return user

async def update_user_role(db: AsyncSession, telegram_id: str, role: str):
    user = await get_user_by_telegram_id(db, telegram_id)
    if not user:
        raise CRUDError("User not found")
    
    allowed_roles = ['member', 'qr', 'chef', 'officiant', 'admin']
    if role not in allowed_roles:
        raise CRUDError(f"Invalid role. Allowed: {allowed_roles}")
    
    user.role = role
    await db.commit()
    await db.refresh(user)
    return user

async def operations_with_user_stars(db: AsyncSession, user_id:str, stars_count:int, operation:Literal['+', '-']) -> bool:
    # try:
    user = await db.execute(select(models.User).where(models.User.telegram_id == user_id))
    user = user.scalars().one_or_none()
    if operation == '+':
        user.balance += stars_count
    if operation == '-':
        if user.balance - stars_count < 0:
            raise Exception()
        user.balance -= stars_count
    await db.commit()
    return True
    # except Exception as e:
    #     return False

# Ticket CRUD
async def get_ticket_by_id(db: AsyncSession, ticket_id: int):
    result = await db.execute(
        select(models.Ticket).where(models.Ticket.id == ticket_id)
    )
    return result.scalar_one_or_none()

async def get_ticket_by_qr(db: AsyncSession, qr_code: str):
    result = await db.execute(
        select(models.Ticket).where(models.Ticket.qr_code == qr_code)
    )
    return result.scalar_one_or_none()

async def get_user_ticket(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Ticket).where(models.Ticket.user_id == user_id)
    )
    return result.scalar_one_or_none()

async def get_all_tickets(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Ticket).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def create_ticket(db: AsyncSession, ticket: schemas.TicketCreate, user_id: int):
    existing_ticket = await get_user_ticket(db, user_id)
    if existing_ticket:
        raise CRUDError("User already has a ticket")
    
    db_ticket = models.Ticket(**ticket.dict(), user_id=user_id)
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket

async def mark_ticket_used(db: AsyncSession, ticket_id: int):
    ticket = await get_ticket_by_id(db, ticket_id)
    if not ticket:
        raise CRUDError("Ticket not found")
    
    ticket.is_used = True
    await db.commit()
    await db.refresh(ticket)
    return ticket

# Product CRUD
async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Product).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_product(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(models.Product).where(models.Product.id == product_id)
    )
    return result.scalar_one_or_none()

async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

async def update_product(db: AsyncSession, product_id: int, product_update: schemas.ProductUpdate):
    product = await get_product(db, product_id)
    if not product:
        raise CRUDError("Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    await db.commit()
    await db.refresh(product)
    return product

async def delete_product(db: AsyncSession, product_id: int):
    product = await get_product(db, product_id)
    if not product:
        raise CRUDError("Product not found")
    
    await db.delete(product)
    await db.commit()
    return product

# Order CRUD
async def get_user_orders(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Order)
        .where(models.Order.user_id == user_id)
        .order_by(models.Order.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_order_by_id(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(models.Order).where(models.Order.id == order_id)
    )
    return result.scalar_one_or_none()

async def get_all_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Order)
        .order_by(models.Order.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_recent_fulfilled_orders(db: AsyncSession, minutes: int = 20):
    time_threshold = datetime.now() - timedelta(minutes=minutes)
    result = await db.execute(
        select(models.Order)
        .where(and_(
            models.Order.is_fulfilled == True
        ))
        .order_by(models.Order.created_at.desc())
    )
    return result.scalars().all()

async def get_user_active_orders_count(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.Order)
        .where(and_(
            models.Order.user_id == user_id,
            models.Order.is_fulfilled == False
        ))
    )
    return len(result.scalars().all())

async def create_order(db: AsyncSession, order: schemas.OrderCreate, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise CRUDError("User not found")
    
    active_orders_count = await get_user_active_orders_count(db, user_id)
    if active_orders_count >= 2 and user.role != 'vip':
        raise CRUDError("Maximum active orders limit reached")
    total_price = 0
    if user.role != 'vip':
        product_ids = [int(pid) for pid in order.products_ids.split(',') if pid.strip()]
        for product_id in product_ids:
            product = await get_product(db, product_id)
            total_price += product.price
            if product and product.is_for_table:
                raise CRUDError("Non-VIP users cannot order table products")
    if await operations_with_user_stars(db, user_id, total_price, '-'):
    
        db_order = models.Order(**order.dict(), user_id=user_id)
        db.add(db_order)
        await db.commit()
        await db.refresh(db_order)
        return db_order
    raise CRUDError("Недостаточно средств!")

async def update_order_fulfillment(db: AsyncSession, order_id: int, is_fulfilled: bool):
    order = await get_order_by_id(db, order_id)
    if not order:
        raise CRUDError("Order not found")
    
    order.is_fulfilled = is_fulfilled
    await db.commit()
    await db.refresh(order)
    return order


# app/crud.py - добавляем метод create_product
async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    """Создание нового продукта"""
    # Проверяем, существует ли продукт с таким именем
    result = await db.execute(
        select(models.Product).where(models.Product.name == product.name)
    )
    existing_product = result.scalar_one_or_none()
    
    if existing_product:
        raise CRUDError("Product with this name already exists")
    
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product

# app/crud.py - добавляем недостающие методы
async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить всех пользователей"""
    result = await db.execute(
        select(models.User).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_all_tickets(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Получить все билеты"""
    result = await db.execute(
        select(models.Ticket).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def update_product(db: AsyncSession, product_id: int, product_update: schemas.ProductUpdate):
    """Обновить продукт"""
    product = await get_product(db, product_id)
    if not product:
        raise CRUDError("Product not found")
    
    update_data = product_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    await db.commit()
    await db.refresh(product)
    return product