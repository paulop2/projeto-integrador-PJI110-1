import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTPException

from sqlalchemy.orm import Session

from src.auth.service import hash_password
from src.config import settings
from src.models.usuario import Usuario, ResetToken


def generate_reset_token(db: Session, email: str) -> str | None:
    user = db.query(Usuario).filter(Usuario.email == email.lower()).first()
    if not user:
        return None
    if not user.ativo:
        return None

    # Delete existing unused tokens for this user
    db.query(ResetToken).filter_by(usuario_id=user.id, usado=False).delete()

    token = secrets.token_urlsafe(32)
    expira_em = datetime.now(timezone.utc) + timedelta(hours=24)
    reset_token = ResetToken(
        usuario_id=user.id,
        token=token,
        expira_em=expira_em,
        usado=False,
    )
    db.add(reset_token)
    db.commit()
    return token


def send_reset_email(to_email: str, token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/redefinir-senha?token={token}"

    if not settings.SMTP_USER:
        print(f"[DEV] Reset link: {reset_url}")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Redefinição de senha — Sistema Escolar"
    msg["From"] = settings.SMTP_SENDER
    msg["To"] = to_email

    body = (
        f"Olá!\n\n"
        f"Você solicitou a redefinição de senha para o Sistema Escolar.\n\n"
        f"Clique no link abaixo para criar uma nova senha:\n"
        f"{reset_url}\n\n"
        f"Este link expira em 24 horas e só pode ser usado uma vez.\n\n"
        f"Se você não solicitou esta redefinição, ignore este email.\n"
    )

    part = MIMEText(body, "plain", "utf-8")
    msg.attach(part)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.sendmail(settings.SMTP_SENDER, to_email, msg.as_string())
    except SMTPException as exc:
        raise RuntimeError(f"Failed to send reset email: {exc}") from exc


def validate_and_consume_token(db: Session, token: str) -> Usuario | None:
    reset_token = db.query(ResetToken).filter(ResetToken.token == token).first()
    if not reset_token:
        return None
    if reset_token.usado:
        return None
    now = datetime.now(timezone.utc)
    expira_em = reset_token.expira_em
    if expira_em.tzinfo is None:
        expira_em = expira_em.replace(tzinfo=timezone.utc)
    if expira_em < now:
        return None
    reset_token.usado = True
    db.commit()
    return db.get(Usuario, reset_token.usuario_id)


def update_password(db: Session, user: Usuario, nova_senha: str) -> None:
    user.senha_hash = hash_password(nova_senha)
    db.commit()
