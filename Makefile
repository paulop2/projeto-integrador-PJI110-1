.PHONY: backend frontend dev install-backend install-frontend migrate setup

# Iniciar apenas o backend
backend:
	cd backend && source venv/bin/activate && uvicorn src.main:app --reload --port 8000

# Iniciar apenas o frontend
frontend:
	cd frontend && npm run dev

# Iniciar ambos em paralelo (requer make 3.81+)
dev:
	make -j2 backend frontend

# Instalar dependências do backend (criar venv se necessário)
install-backend:
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Instalar dependências do frontend
install-frontend:
	cd frontend && npm install

# Executar migrations Alembic
migrate:
	cd backend && source venv/bin/activate && alembic upgrade head

# Setup completo do projeto do zero
setup: install-backend install-frontend migrate
	@echo "Setup completo! Execute 'make dev' para iniciar."

# NOTA: Os comandos com `source venv/bin/activate` são compatíveis com macOS/Linux.
# No Windows (Git Bash), use `source venv/Scripts/activate`.
# No Windows (CMD/PowerShell), execute os comandos manualmente:
#   Backend: cd backend && venv\Scripts\activate && uvicorn src.main:app --reload --port 8000
#   Frontend: cd frontend && npm run dev
