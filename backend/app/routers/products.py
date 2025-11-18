# app/routers/products.py - обновляем для поддержки создания продуктов
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user, get_admin_user

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[schemas.Product])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех продуктов"""
    return await crud.get_products(db, skip, limit)

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: schemas.ProductCreate,
    current_user = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db)
):
    """Создать новый продукт (только для админа)"""
    try:
        return await crud.create_product(db, product)
    except crud.CRUDError as e:
        raise HTTPException(status_code=400, detail=str(e))