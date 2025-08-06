from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.auth import AuthService
from models import UserRole

# Security for protected routes
security = HTTPBearer()

async def get_current_user(auth_service: AuthService = Depends()) -> dict:
    credentials: HTTPAuthorizationCredentials = Depends(security)
    token = credentials.credentials
    user = await auth_service.verify_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_admin_user(auth_service: AuthService = Depends()) -> dict:
    current_user: dict = await get_current_user(auth_service=auth_service)
    if current_user["role"] not in [UserRole.ADMIN, UserRole.SUPERADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted for this user role",
        )
    return current_user