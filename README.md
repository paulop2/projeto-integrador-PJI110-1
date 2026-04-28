# Sistema Web de Registro Escolar

Sistema web para registro e acompanhamento escolar, permitindo que pais visualizem notas e frequência dos filhos, professores lancem chamadas e notas, e administradores gerenciem alunos e turmas.

Desenvolvido como Projeto Integrador (PJI110) — Turma 004 da UNIVESP, Polo Valinhos.

---

## ✨ Funcionalidades

- **Autenticação JWT** com três perfis de acesso distintos
- **Painel Administrativo** — CRUD completo de alunos, turmas, disciplinas, professores e responsáveis
- **Portal do Professor** — Registro de chamada (presença/falta) e lançamento de notas por turma/bimestre
- **Portal do Responsável** — Boletim e frequência do filho com cálculos automáticos e alertas LDB
- **Dashboard** — Visão agregada de desempenho para admin (alertas de risco + tabela por turma) e professores (média e % aprovação por turma)
- **Skeleton Loading** — Estados de carregamento com placeholders animados em todas as telas
- **Toast de Erros** — Mensagens amigáveis em português para falhas de API

---

## 🏗️ Arquitetura

Separação frontend/backend para permitir trabalho paralelo entre os membros da equipe:

| Camada | Tecnologia |
|--------|------------|
| **Backend** | Python 3.12 + FastAPI + SQLAlchemy 2.0 (síncrono) + Alembic + pytest |
| **Frontend** | React 19 + TypeScript + Vite + Tailwind CSS v3 + React Router 6 + TanStack Query 5 + react-hook-form + zod + Sonner |
| **Banco de Dados** | SQLite (WAL mode, foreign keys ON) |
| **Autenticação** | JWT (localStorage, 7 dias, renovação automática) |
| **Email** | Mailtrap (desenvolvimento/demo) |

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12+
- Node.js 20+
- npm ou yarn

### Backend

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt

# Copiar e preencher variáveis de ambiente
cp .env.example .env

# Criar banco e aplicar migrations
alembic upgrade head

# Iniciar servidor
uvicorn src.main:app --reload
```

O backend estará disponível em `http://localhost:8000`.

Documentação interativa (Swagger): `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

O frontend estará disponível em `http://localhost:5173`.

---

## 👥 Perfis de Acesso

| Perfil | Capacidades |
|--------|-------------|
| **Administrador** | Gerencia usuários, alunos, turmas, disciplinas e vínculos professor/turma |
| **Professor** | Registra chamada e lança notas apenas das turmas às quais está vinculado |
| **Responsável** | Visualiza boletim e frequência dos filhos vinculados |

---

## 📁 Estrutura do Projeto

```
├── backend/              # API FastAPI
│   ├── alembic/          # Migrations
│   ├── src/
│   │   ├── auth/         # Autenticação JWT (login, dependências, hash)
│   │   ├── password_reset/ # Recuperação de senha (tokens opacos, SMTP)
│   │   ├── admin/        # CRUD administrativo (6 entidades)
│   │   ├── professor/    # Portal do professor (chamada, notas, frequência)
│   │   ├── responsavel/  # Portal do responsável (boletim, meus-filhos)
│   │   ├── models/       # SQLAlchemy models (11 tabelas)
│   │   ├── config.py     # Configurações (pydantic-settings)
│   │   └── main.py       # Entry point FastAPI
│   ├── .env.example
│   └── requirements.txt
├── frontend/             # Aplicação React
│   ├── src/
│   │   ├── components/   # Componentes reutilizáveis (ProtectedRoute, AppLayout, AdminLayout, Modal, EntityTable, TurmaCard, BoletimTable, StatusBadge, SummaryCard, SkeletonCard, SkeletonTable)
│   │   ├── pages/        # Telas (Login, AdminDashboard, ProfessorLandingPage, ProfessorTurmaPage, ResponsavelBoletimPage)
│   │   ├── contexts/     # Contextos React (AuthContext)
│   │   ├── services/     # Clientes HTTP (api.ts com interceptores)
│   │   └── main.tsx      # Entry point React
│   └── package.json
├── docs/                 # Documentação do projeto
│   └── relatorio-final.md
├── .planning/            # Planejamento e roadmap do desenvolvimento
└── README.md
```

---

## 📊 Roadmap do Desenvolvimento

| Fase | Status | Descrição |
|------|--------|-----------|
| 1. Infraestrutura | ✅ Concluída | Esqueleto backend + frontend + banco + migrations |
| 2. Autenticação | ✅ Concluída | Login JWT, rotas protegidas por papel, recuperação de senha, localStorage com renovação automática |
| 3. Painel Admin | ✅ Concluída | CRUD completo de 6 entidades com modais, validação, paginação e testes |
| 4. Portal do Professor | ✅ Concluída | Chamada e notas por turma/bimestre, com controle de acesso por turma vinculada |
| 5. Portal do Responsável | ✅ Concluída | Boletim e frequência com cálculo automático de média, alertas LDB e verificação de IDOR |
| 6. Dashboard e Polish | ✅ Concluída | Dashboard com métricas agregadas, alertas LDB, skeleton loading e toast de erros |
| 7. Deploy | ⏳ Pendente | Render + GitHub Actions CI/CD |

> **Progresso atual:** 6/7 fases concluídas (~86%)

---

## 👨‍💻 Equipe

- **Luiz Eduardo Rodrigues Firmino**
- **Thalita Fernanda Rospendowski Mazzini**
- **Rafael Gustavo Leite**
- **Luiz Henrique de Toledo**
- **Diego Miguel Mafra**
- **Nicholas Prado de Sousa Medeiros**
- **Paulo Vitor de Souza**
- **Leonardo Matheus Anselmo Matiazzo**

**Tutor:** Edson Ricardo Nunes Nascimento  
**Polo:** Valinhos — SP, 2026

---

## 📄 Contexto Acadêmico

Este projeto foi desenvolvido na disciplina de **Projeto Integrador em Computação I — Turma 004** da **Universidade Virtual do Estado de São Paulo (UNIVESP)**.

A proposta surgiu da dificuldade de comunicação entre escola e responsáveis, validada por entrevista com a professora Elizabete Ap. Godoy de Toledo (rede municipal de ensino) em 08/03/2026.

**Entrega:** Relatório Final e Vídeo de apresentação até 24/05/2026.

---

## 📚 Documentação

- [Relatório Final](docs/relatorio-final.md) — Documento técnico-científico completo
- [Roadmap e Planejamento](.planning/ROADMAP.md) — Estrutura de fases e objetivos
- [Estado do Projeto](.planning/STATE.md) — Decisões, métricas e contexto acumulado

---

## 🛡️ Decisões Técnicas Principais

| Decisão | Justificativa |
|---------|---------------|
| SQLAlchemy síncrono | Evita problemas de lock no SQLite em ambiente de protótipo |
| JWT em localStorage | Prazo de 7 dias com renovação automática; sessionStorage seria inconveniente para protótipo |
| Business rules na service layer | Nota ≤ máxima, aluno pertence à turma — validados em Python, não em triggers SQLite |
| Alembic com commit explícito | SQLAlchemy 2.0 + SQLite requer `connection.commit()` após `context.run_migrations()` |

---

## 📜 Licença

Projeto acadêmico — UNIVESP Polo Valinhos, 2026.
