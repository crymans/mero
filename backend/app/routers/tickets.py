# app/routers/tickets.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user, get_qr_user
import uuid

router = APIRouter(prefix="/rostov_api/tickets", tags=["tickets"])

@router.post("/", response_model=schemas.Ticket, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket: schemas.TicketCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        if int(ticket.price) not in [500, 900, 1300]:
            raise Exception()
        existing_ticket = await crud.get_user_ticket(db, current_user.telegram_id)
        if existing_ticket:
            raise crud.CRUDError("User already has a ticket")
        ticket = schemas.TicketCreate(price=ticket.price, qr_code=str(uuid.uuid4()))
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

@router.patch("/{ticket_id}/mark-used", response_model=schemas.Ticket)
async def mark_ticket_used(
    ticket_id: int,
    current_user = Depends(get_qr_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await crud.mark_ticket_used(db, ticket_id)
    except crud.CRUDError as e:
        raise HTTPException(status_code=404, detail=str(e))