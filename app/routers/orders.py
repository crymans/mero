# app/routers/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user, get_chef_or_admin_user, get_officiant_or_admin_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: schemas.OrderCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await crud.create_order(db, order, current_user.id)
    except crud.CRUDError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my", response_model=list[schemas.Order])
async def get_my_orders(
    current_user = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_user_orders(db, current_user.id, skip, limit)

@router.get("/", response_model=list[schemas.Order])
async def get_all_orders(
    current_user = Depends(get_chef_or_admin_user),
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_all_orders(db, skip, limit)

@router.get("/recent-fulfilled", response_model=list[schemas.Order])
async def get_recent_fulfilled_orders(
    current_user = Depends(get_officiant_or_admin_user),
    db: AsyncSession = Depends(get_db)
):
    return await crud.get_recent_fulfilled_orders(db)

@router.patch("/{order_id}/fulfill", response_model=schemas.Order)
async def update_order_fulfillment(
    order_id: int,
    order_update: schemas.OrderUpdate,
    current_user = Depends(get_chef_or_admin_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await crud.update_order_fulfillment(db, order_id, order_update.is_fulfilled)
    except crud.CRUDError as e:
        raise HTTPException(status_code=404, detail=str(e))