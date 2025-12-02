# app/routers/tickets.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.utils.authUser import AuthUser
from app import crud, schemas
from app.dependencies import get_current_user, get_qr_user
import uuid, time

router = APIRouter(prefix="/rostov_api/tickets", tags=["tickets"])

@router.post("/", response_model=schemas.Ticket, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket: schemas.TicketCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
<<<<<<< HEAD
        if int(ticket.price) not in [400, 450, 650]:
=======
        if int(ticket.price) not in [700, 900, 1500]:
>>>>>>> 7e9ba3fe22c549f8ccc0e6223dbc5677b26f11aa
            raise Exception()
        existing_ticket = await crud.get_user_ticket(db, current_user.telegram_id)
        if existing_ticket:
            raise crud.CRUDError("User already has a ticket")
        token = await AuthUser.create_jwt({'user_id':current_user.telegram_id})
        qr_code = f'https://tg-gift-store.ru/rostov_party/check_ticket?token={token}'
        ticket = schemas.TicketCreate(price=ticket.price, qr_code=qr_code)
        if await crud.operations_with_user_stars(db, current_user.telegram_id, ticket.price, '-'):
            return await crud.create_ticket(db, ticket, current_user.telegram_id)
        raise Exception()
    except crud.CRUDError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my", response_model=schemas.Ticket)
async def get_my_ticket(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    ticket = await crud.get_user_ticket(db, current_user.telegram_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/qr/{qr_code}", response_model=schemas.Ticket)
async def get_ticket_by_qr(
    qr_code: str,
    current_user = Depends(get_qr_user),
    db: AsyncSession = Depends(get_db)
):
    ticket = await crud.get_ticket_by_qr(db, qr_code)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/{token}/mark-used", response_model=schemas.EntryAnswer)
async def mark_ticket_used(
    token: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        data = await AuthUser.decode_jwt(token)
        print(data)
        if data['exp'] > time.time():
            user = await crud.get_user_by_telegram_id(db, data['user_id'])
            print(user)
            ticket = await crud.get_user_ticket(db, user.telegram_id)
            ticket_used = await crud.mark_ticket_used(db, ticket.id)
            return schemas.EntryAnswer(ticket=ticket_used, user=user)

        raise Exception()
    except crud.CRUDError as e:
        raise HTTPException(status_code=404, detail=str(e))