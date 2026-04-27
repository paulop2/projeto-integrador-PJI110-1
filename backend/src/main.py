import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

from src.config import settings
from src.auth.router import router as auth_router
from src.auth.service import maybe_renew_token
from src.password_reset.router import router as reset_router
from src.admin.router import router as admin_router


app = FastAPI(
    title="Sistema Escolar API",
    version="1.0.0",
    description="API do sistema de registro escolar",
)

# CORS deve ser adicionado PRIMEIRO — antes de qualquer outro middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # ["http://localhost:5173"] — nunca ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TokenRenewalMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        response = await call_next(request)
        # Only attempt renewal on successful (2xx) responses
        if 200 <= response.status_code < 300:
            auth_header = request.headers.get("Authorization", "")
            match = re.match(r"^Bearer\s+(.+)$", auth_header, re.IGNORECASE)
            if match:
                token = match.group(1)
                new_token = maybe_renew_token(token)
                if new_token:
                    response.headers["X-New-Token"] = new_token
        return response


app.add_middleware(TokenRenewalMiddleware)

app.include_router(auth_router)
app.include_router(reset_router, prefix="/auth")
app.include_router(admin_router)


@app.get("/health")
def health_check():
    """Endpoint de verificação de saúde — confirma que API está online."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}
