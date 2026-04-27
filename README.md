# Sistema Web de Registro Escolar

Sistema web para registro e acompanhamento escolar, permitindo que pais visualizem notas e frequência dos filhos, professores lancem chamadas e notas, e administradores gerenciem alunos e turmas.

Desenvolvido como Projeto Integrador (PJI110) — Turma 004 da UNIVESP, Polo Valinhos.

---

## ✨ Funcionalidades

- **Autenticação JWT** com três perfis de acesso distintos
- **Painel Administrativo** — CRUD completo de alunos, turmas, disciplinas, professores e responsáveis
- **Portal do Professor** — Registro de chamada (presença/falta) e lançamento de notas por turma/bimestre
- **Portal do Responsável** — Boletim e frequência do filho com cálculos automáticos e alertas LDB
- **Dashboard** — Visão agregada de desempenho para admin e professores

---

## 🏗️ Arquitetura

Separação frontend/backend para permitir trabalho paralelo entre os membros da equipe:

| Camada | Tecnologia |
|--------|------------|
| **Backend** | Python 3.12 + FastAPI + SQLAlchemy 2.0 (síncrono) + Alembic |
| **Frontend** | React 18 + TypeScript + Vite + React Router 6 + TanStack Query 5 |
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
│   │   ├── auth/         # Módulo de autenticação
│   │   ├── models/       # SQLAlchemy models
│   │   ├── config.py     # Configurações
│   │   └── main.py       # Entry point
│   ├── .env.example
│   └── requirements.txt
├── frontend/             # Aplicação React
│   ├── src/
│   │   ├── components/   # Componentes reutilizáveis
│   │   ├── pages/        # Telas
│   │   ├── contexts/     # Contextos React (Auth, etc.)
│   │   └── api.ts        # Cliente HTTP (Axios)
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
| 2. Autenticação | 🚧 Em andamento | Login JWT, rotas protegidas, recuperação de senha |
| 3. Painel Admin | ⏳ Pendente | CRUD de alunos, turmas, disciplinas, professores |
| 4. Portal do Professor | ⏳ Pendente | Chamada e notas |
| 5. Portal do Responsável | ⏳ Pendente | Boletim e frequência |
| 6. Dashboard e Polish | ⏳ Pendente | Dashboard agregado, alertas LDB, estados de erro/loading |

> **Progresso atual:** 1/6 fases concluídas (33% dos planos)

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
