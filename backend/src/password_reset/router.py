from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.auth.service import create_access_token, get_display_name
from src.database import get_db
from src.password_reset.schemas import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)
from src.password_reset.service import (
    generate_reset_token,
    send_reset_email,
    update_password,
    validate_and_consume_token,
)

router = APIRouter(tags=["password-reset"])


@router.post("/forgot-password", response_model=ForgotPasswordResponse)
def forgot_password(body: ForgotPasswordRequest, db: Session = Depends(get_db)):
    token = generate_reset_token(db, body.email)
    if token:
        send_reset_email(body.email, token)
    # Always return the same message — do NOT reveal if email exists
    return ForgotPasswordResponse(
        message="Se este email estiver cadastrado, você receberá um link de redefinição em breve."
    )


@router.post("/reset-password", response_model=ResetPasswordResponse)
def reset_password(body: ResetPasswordRequest, db: Session = Depends(get_db)):
    if len(body.nova_senha) < 8:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 8 caracteres")
    user = validate_and_consume_token(db, body.token)
    if not user:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")
    update_password(db, user, body.nova_senha)
    # Auto-login: issue new JWT
    access_token = create_access_token({"sub": str(user.id), "tipo": user.tipo.value})
    nome = get_display_name(db, user)
    return ResetPasswordResponse(
        access_token=access_token,
        token_type="bearer",
        user={"id": user.id, "email": user.email, "tipo": user.tipo.value, "nome": nome},
    )
