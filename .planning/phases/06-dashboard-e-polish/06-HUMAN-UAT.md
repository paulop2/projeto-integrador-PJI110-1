---
status: partial
phase: 06-dashboard-e-polish
source: [06-VERIFICATION.md]
started: 2026-04-28
updated: 2026-04-28
---

## Current Test

[awaiting human testing]

## Tests

### 1. Admin Dashboard
expected: Count cards display (Alunos, Turmas, Disciplinas, Professores, Responsáveis); alert card appears below counts (green if no risk, yellow if alunos em risco > 0); performance table shows Turma | Alunos | Média Geral | % Aprovados | Status with green/red badges
result: [pending]

### 2. Professor Portal
expected: TurmaCards show nome, disciplinas, num_alunos, Média geral, % Aprovados; clicking TurmaCard navigates to turma details
result: [pending]

### 3. Error Toast
expected: When backend is stopped, navigating pages shows red toast: "Erro no servidor. Tente novamente em instantes."
result: [pending]

### 4. Skeleton Loading
expected: With Slow 3G throttling, refreshing admin dashboard shows gray pulsing skeleton placeholders instead of "Carregando..." text
result: [pending]

## Summary

total: 4
passed: 0
issues: 0
pending: 4
skipped: 0
blocked: 0

## Gaps
