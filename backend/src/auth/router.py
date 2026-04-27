from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth.schemas import LoginRequest, LoginResponse, UserInfo
from src.auth.service import authenticate_user, create_access_token, get_display_name
from src.auth.dependencies import get_current_user
from src.database import get_db
from src.models.usuario import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, body.email, body.senha)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    token = create_access_token({"sub": str(user.id), "tipo": user.tipo.value})
    nome = get_display_name(db, user)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        user=UserInfo(
            id=user.id,
            email=user.email,
            tipo=user.tipo.value,
            nome=nome,
        ),
    )


@router.get("/me")
def me(current_user: Usuario = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "tipo": current_user.tipo.value,
    }
