# Sistema Web de Registro Escolar

## What This Is

Sistema web para registro e acompanhamento escolar, permitindo que pais visualizem notas e frequência dos filhos, professores lancem chamadas e notas, e administradores gerenciem alunos e turmas. Desenvolvido como projeto integrador da UNIVESP (Polo Valinhos), com potencial de uso real na escola parceira.

## Core Value

Pais acompanham o desempenho escolar dos filhos — notas e presença — sem precisar ir até a escola.

## Requirements

### Validated

- [x] Autenticação com três perfis distintos: administrador, docente e pai — Validated in Phase 2: Autenticação
- [x] Administrador gerencia alunos, turmas e usuários do sistema — Validated in Phase 3: Painel Admin
- [x] Docente registra chamada (presença/falta) por aula e turma — Validated in Phase 4: Portal do Professor
- [x] Docente lança notas por aluno e disciplina — Validated in Phase 4: Portal do Professor

### Validated

- [x] Autenticação com três perfis distintos: administrador, docente e pai — Validated in Phase 2: Autenticação
- [x] Administrador gerencia alunos, turmas e usuários do sistema — Validated in Phase 3: Painel Admin
- [x] Docente registra chamada (presença/falta) por aula e turma — Validated in Phase 4: Portal do Professor
- [x] Docente lança notas por aluno e disciplina — Validated in Phase 4: Portal do Professor
- [x] Pai visualiza boletim (notas) e frequência do filho — Validated in Phase 5: Portal do Responsável
- [x] Dashboard com métricas de desempenho por turma — Validated in Phase 6: Dashboard e Polish

### Active

- [ ] Deploy em produção (Render + GitHub Actions)

### Out of Scope

- Comunicação em tempo real (chat) — alta complexidade, não é o foco do v1
- App mobile — web-first, mobile é v2
- Múltiplas escolas/multi-tenant — projeto é para uma escola específica
- Pagamentos / mensalidades — fora do escopo educacional do projeto

## Context

- **Projeto acadêmico** da UNIVESP — disciplina Projeto Integrador em Computação I, Turma 004
- **Tutor:** Edson Ricardo Nunes Nascimento
- **Polo:** Valinhos, SP
- **Equipe:** 8 integrantes com papéis distribuídos (frontend, backend, QA, docs)
- **Entrevista com comunidade escolar** realizada em 08/03/2026 com Elizabete Ap. Godoy de Toledo (professora da rede municipal) — validou a necessidade do sistema
- **Repositório GitHub** já criado com estrutura inicial
- Proposta surgiu da dificuldade de comunicação entre escola e responsáveis

## Constraints

- **Tech Stack**: Python FastAPI (backend) + React (frontend) + SQLite (banco) — já definido e fixado no relatório
- **Prazo**: Entrega do Relatório Final e Vídeo até 24/05/2026 (conforme PDCA)
- **Equipe**: 8 pessoas com diferentes níveis técnicos — separação frontend/backend é necessária
- **Escopo**: Protótipo funcional que pode virar produto real — qualidade de código importa

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| FastAPI + React + SQLite | Definido pela equipe com base nas habilidades técnicas e simplicidade de deploy | Implemented |
| Autenticação JWT | Padrão para APIs REST, stateless, fácil de integrar com React | Implemented |
| Separação frontend/backend | Permite trabalho paralelo entre membros da equipe | Working |
| SQLite como banco de dados | Simplicidade para protótipo, sem necessidade de servidor de banco | Working |

---
*Last updated: 2026-04-28 after Phase 6 completion*
