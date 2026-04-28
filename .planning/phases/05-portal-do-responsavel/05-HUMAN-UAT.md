---
status: partial
phase: 05-portal-do-responsavel
source: [05-03-VERIFICATION.md]
started: 2026-04-27T22:50:00Z
updated: 2026-04-27T22:50:00Z
---

## Current Test

awaiting human testing

## Tests

### 1. Boletim page loads for responsavel
expected: Responsavel logs in, sees "Boletim Escolar" page with current year subtitle
result: pending

### 2. Notas by disciplina and calculated média
expected: Table shows 8 columns, missing notas display "—", média calculated automatically
result: pending

### 3. Frequência per disciplina with alert
expected: Format "82% (15/18)", red highlight when freq < 75%
result: pending

### 4. Approval status badge
expected: Green "Aprovado" when media >= 5.0 AND freq >= 75%, else red "Reprovado"
result: pending

### 5. Summary card state
expected: Green card when all pass, yellow card when any discipline at risk
result: pending

### 6. Ownership check (IDOR)
expected: Crafting request to /responsavel/boletim?aluno_id=999 returns 403 with "Acesso negado"
result: pending

### 7. Multi-child selector
expected: Dropdown appears when > 1 child, switching reloads boletim without stale data
result: pending

### 8. Empty states
expected: "Nenhum aluno vinculado" when no children, "Boletim não disponível" when no data
result: pending

## Summary

total: 8
passed: 0
issues: 0
pending: 8
skipped: 0
blocked: 0

## Gaps
