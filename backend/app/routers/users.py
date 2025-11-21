# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user
import json, requests, aiohttp
from tg_bot.create_bot import TOKEN

router = APIRouter(prefix="/rostov_api/users", tags=["users"])



@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(
    request:Request,
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        data = json.loads(request.headers['user-data'])
        username = data.get('username')
        if username == None:
            username = ''
        user.telegram_id = data['id']
        user.username = username
        try:
            return await crud.create_user(db, user)
        except:
            return await get_current_user(request, db)
    except crud.CRUDError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me", response_model=schemas.User)
async def get_current_user_info(
    current_user: schemas.User = Depends(get_current_user)
):
    return current_user

@router.patch("/me", response_model=schemas.User)
async def update_user_me(
    user_update: schemas.UserUpdate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await crud.update_user(db, current_user.telegram_id, user_update)
    except crud.CRUDError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/purchase")
async def invoice_purchase(
    stars_amount: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        title='Stars'
        description='Stars'
        prices=schemas.LabeledPrice(label='XTR', amount=stars_amount).to_json()
        link = requests.get(f'https://api.telegram.org/bot'+TOKEN+'/createInvoiceLink?title='+title+'&description='+description+'&payload='+title+'&currency=XTR&prices=['+prices+']')
        link = (link.json())['result']
        return link
    except Exception as e:
        return False