from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings


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


@app.get("/health")
def health_check():
    """Endpoint de verificação de saúde — confirma que API está online."""
    return {"status": "ok", "environment": settings.ENVIRONMENT}
