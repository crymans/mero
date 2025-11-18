# app/routers/tickets.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud, schemas
from app.dependencies import get_current_user, get_qr_user

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/", response_model=schemas.Ticket, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    ticket: schemas.TicketCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await crud.create_ticket(db, ticket, current_user.id)
    except crud.CRUDError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my", response_model=schemas.Ticket)
async def get_my_ticket(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    ticket = await crud.get_user_ticket(db, current_user.id)
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