import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.config import settings
from src.models.usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode = {**data, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def authenticate_user(db: Session, email: str, senha: str) -> Usuario | None:
    user = db.query(Usuario).filter(Usuario.email == email.lower()).first()
    if not user:
        return None
    if not user.ativo:
        return None
    if not verify_password(senha, user.senha_hash):
        return None
    return user


def get_display_name(db: Session, user: Usuario) -> str:
    if user.tipo.value == "professor":
        result = db.execute(
            text("SELECT nome FROM professores WHERE usuario_id = :uid"),
            {"uid": user.id},
        ).scalar()
        return result or user.email
    elif user.tipo.value == "responsavel":
        result = db.execute(
            text("SELECT nome FROM responsaveis WHERE usuario_id = :uid"),
            {"uid": user.id},
        ).scalar()
        return result or user.email
    else:
        return "Administrador"


def maybe_renew_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
    except jwt.InvalidTokenError:
        return None
    exp = payload.get("exp")
    if not exp:
        return None
    now = datetime.now(timezone.utc).timestamp()
    if (exp - now) < 86400:  # less than 24 hours remaining
        new_data = {"sub": payload.get("sub"), "tipo": payload.get("tipo")}
        return create_access_token(new_data)
    return None
