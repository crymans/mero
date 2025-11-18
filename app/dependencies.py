# app/dependencies.py
from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app import crud

async def get_current_user(
    x_user_telegram_id: str = Header(..., alias="X-User-Telegram-ID"),
    db: AsyncSession = Depends(get_db)
):
    user = await crud.get_user_by_telegram_id(db, x_user_telegram_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

def require_role(required_role: str):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user.role != required_role and current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role {required_role} required"
            )
        return current_user
    return role_checker

def require_roles(required_roles: list):
    def roles_checker(current_user = Depends(get_current_user)):
        if current_user.role not in required_roles and current_user.role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"One of roles {required_roles} required"
            )
        return current_user
    return roles_checker

# Специальные зависимости для разных ролей
get_qr_user = require_role("qr")
get_chef_user = require_role("chef")
get_officiant_user = require_role("officiant")
get_admin_user = require_role("admin")
get_chef_or_admin_user = require_roles(["chef", "admin"])
get_officiant_or_admin_user = require_roles(["officiant", "admin"])