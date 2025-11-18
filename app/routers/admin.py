# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas
from app.dependencies import get_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=list[schemas.User])
async def get_all_users(
    current_user: schemas.User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Получить всех пользователей (только для админа)"""
    return await crud.get_all_users(db, skip=skip, limit=limit)

@router.get("/products", response_model=list[schemas.Product])
async def get_all_products(
    current_user: schemas.User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Получить все продукты (только для админа)"""
    return await crud.get_products(db, skip=skip, limit=limit)

@router.get("/tickets", response_model=list[schemas.Ticket])
async def get_all_tickets(
    current_user: schemas.User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Получить все билеты (только для админа)"""
    return await crud.get_all_tickets(db, skip=skip, limit=limit)

@router.patch("/users/{telegram_id}/role", response_model=schemas.User)
async def update_user_role(
    telegram_id: str,
    role_update: schemas.UserRoleUpdate,
    current_user: schemas.User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить роль пользователя (только для админа)"""
    try:
        return await crud.update_user_role(db, telegram_id, role_update.role)
    except crud.CRUDError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/products", response_model=schemas.Product)
async def create_product(
    product: schemas.ProductCreate,
    current_user: schemas.User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать новый продукт (только для админа)"""
    try:
        return await crud.create_product(db, product)
    except crud.CRUDError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    current_user: schemas.User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить продукт (только для админа)"""
    try:
        return await crud.update_product(db, product_id, product)
    except crud.CRUDError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    current_user: schemas.User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Удалить продукт (только для админа)"""
    try:
        await crud.delete_product(db, product_id)
        return {"message": "Product deleted successfully"}
    except crud.CRUDError as e:
        raise HTTPException(status_code=404, detail=str(e))