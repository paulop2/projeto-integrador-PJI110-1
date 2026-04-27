# Feature Research

**Domain:** School Web Registration System (SIS) — Brazilian K-12 context
**Researched:** 2026-04-26
**Confidence:** HIGH (project scope confirmed by team meeting notes + domain research)

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete or unusable.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Login with role-based access | No SIS works without identity; admin/teacher/parent have radically different needs | LOW | JWT already decided. Three roles: admin, professor, responsavel |
| Student registration (CRUD) | Admin must enroll students before anything else works | LOW | Needs link to responsavel and turma |
| Class (turma) management | Students belong to classes; attendance and grades reference turma | LOW | Fields: nome, ano, serie, turno. Already modeled in schema |
| Subject (disciplina) management | Grades and attendance are recorded per subject | LOW | Independent table, CRUD by admin |
| Teacher registration (CRUD) | Teachers must exist before assignments and grade entry work | LOW | Linked to usuarios via FK |
| Parent (responsavel) registration (CRUD) | Parents need accounts before they can see their child's data | LOW | Requires CPF, email, phone |
| Teacher-class-subject assignment | A teacher must be assigned to a turma+disciplina before they can take attendance or enter grades | MEDIUM | Junction table professor_turma. Easy to underscope |
| Daily attendance (chamada) registration | Core teacher workflow: mark present/absent per student per class session | MEDIUM | One chamada per (turma, disciplina, date). Bulk operation (whole class at once) |
| Grade entry by assessment | Teachers create an avaliacao (prova, trabalho, etc.) then enter scores per student | MEDIUM | valor_maximo configurable per assessment. bimestre (1-4) required |
| Parent view: report card (boletim) | Core parent value: see child's grades per subject per bimestre | MEDIUM | Calculated view — aggregates notas by disciplina+bimestre. Must show media |
| Parent view: attendance report (frequencia) | Core parent value: see how many classes their child attended/missed | MEDIUM | Show count and percentage. Must show absences clearly |
| Session management (logout / token refresh) | Users expect to stay logged in during work; must be able to log out | LOW | Refresh token already in plan |
| Admin dashboard summary | Admin needs a quick overview of the system state (total students, classes, recent activity) | LOW | Counts only; no complex analytics needed for v1 |
| Teacher dashboard (minhas turmas) | Teacher needs to see which classes they are assigned to and quickly navigate to attendance/grades | LOW | Simple list filtered by professor_id |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required for v1, but add real value.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Automatic grade average (media) calculation per bimestre | Parents and teachers see computed averages instantly without manual math; reduces errors | LOW | Computed at query time using weighted or simple average. Differentiator only if displayed clearly in boletim |
| Passing/failing status indicator | Immediately shows parent if child is at risk (e.g., media < 5.0 or 6.0 per school rule) | LOW | Requires knowing the school's passing threshold. Make it configurable in admin |
| Absence alert threshold | Flag students who exceed the legal 25% absence limit (LDB art. 24, inciso VI) | MEDIUM | Brazilian law: >25% absences = failure regardless of grades. High value for parents and admin |
| PDF export of boletim | Parent can print or save the report card without visiting school | MEDIUM | Use a library like ReportLab (Python) or a headless browser. Useful for parent-teacher meetings |
| Password recovery via email | Users can self-service reset their password; reduces admin burden | MEDIUM | Requires SMTP configuration. Simple token-based reset flow |
| Teacher edit of past attendance | Mistakes happen; teacher should be able to correct a past chamada | LOW | Already modeled (historico chamadas in plan). Needs permission guard so only the original teacher or admin can edit |
| Absence justification field | Teacher can record the reason for an absence (medical, etc.) | LOW | Already in schema as `justificativa` on presencas. Minimal UI effort |
| Admin can override grades | Correction of data entry errors without asking the teacher | LOW | Admin-only endpoint already scoped in meeting notes (PUT /notas/{id}) |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem useful but would jeopardize the prototype deadline or introduce disproportionate complexity.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Email / WhatsApp notifications on grade/absence entry | Keeps parents informed without logging in | Requires external SMTP or WhatsApp Business API configuration, deliverability concerns, and significant backend plumbing. Doubles testing surface for a prototype | Ship the parent dashboard first; active check-in is sufficient for v1. Add notifications in v1.x |
| Real-time updates (WebSockets) | "Live" grade/attendance feed | Massively overengineered for a school with one teacher updating a class list. Adds infra complexity with no real user benefit at this scale | Simple REST polling or page refresh is fine |
| Multi-school (multi-tenant) support | Imagined future SaaS | Requires schema changes (school_id on every table), separate auth scopes, and billing concepts. Incompatible with single-institution prototype goal | Design with clear boundaries so adding it later is feasible; do not build it now |
| Parent-to-teacher messaging | Seems like natural next step | Two-way comms require moderation, notification plumbing, and clear ownership of the message store. Easily becomes the biggest feature on the board | Out of scope. Direct phone/email contact between parent and school office handles this for a prototype |
| Grade history across school years | Academic transcripts spanning multiple years | Requires year-to-year data archiving strategy, student continuity logic, and much larger dataset management | v1 is single ano letivo (2026). Year field on turmas already enables filtering; history can be unlocked later |
| Student login (self-service) | Students want to check their own grades | Adds a fourth role, additional auth paths, and scope questions (can students see all grades or only their own?). Not in project brief | Parent is the designated viewer. Students use the parent account if needed |
| Mobile app (iOS/Android) | Better experience on phones | Native app is a separate project. React with a responsive layout achieves 90% of the value | Make the React frontend mobile-responsive; it is not a separate app |
| Timetable / scheduling engine | Class schedule per day of week | Scheduling logic is complex (conflict detection, room assignment). Not needed: teacher-class-subject assignment already scopes who teaches what; per-session attendance does not require a formal schedule | Skip. Teachers do attendance by selecting the date manually |

---

## Feature Dependencies

```
Authentication (login + JWT + roles)
    └──required by──> ALL other features

Student CRUD
    └──required by──> Attendance registration
    └──required by──> Grade entry
    └──required by──> Parent dashboard (boletim, frequencia)

Class (turma) CRUD
    └──required by──> Student CRUD (student assigned to turma)
    └──required by──> Teacher-class-subject assignment
    └──required by──> Attendance registration
    └──required by──> Grade entry

Subject (disciplina) CRUD
    └──required by──> Teacher-class-subject assignment
    └──required by──> Attendance registration
    └──required by──> Grade entry

Teacher-class-subject assignment
    └──required by──> Attendance registration (teacher must be assigned before taking chamada)
    └──required by──> Grade entry (teacher must be assigned before entering notas)

Attendance registration (chamada)
    └──enhances──> Parent dashboard (frequencia view)
    └──required by──> Absence alert threshold [differentiator]

Grade entry (notas)
    └──required by──> Parent dashboard (boletim view)
    └──required by──> Automatic average calculation [differentiator]
    └──required by──> Passing/failing status [differentiator]

Parent registration (CRUD)
    └──required by──> Parent dashboard (parent must exist and be linked to student)

Automatic average calculation
    └──enhances──> Parent dashboard (shows media per bimestre)
    └──enables──> Passing/failing status indicator

PDF export
    └──depends on──> Parent dashboard (boletim must work before export)

Password recovery
    └──independent of──> all features (standalone auth flow)
```

### Dependency Notes

- **Authentication is the root dependency:** Nothing works without working login and role guards. It must be the first completed module.
- **CRUD entities before transactions:** Alunos, turmas, disciplinas, and professor assignments must exist before any attendance or grade entry is possible. CRUD modules are foundational, not cosmetic.
- **Teacher assignment is often underscoped:** Teams commonly skip the explicit teacher-turma-disciplina assignment step and hardcode it or leave it implicit. This causes access control failures when teachers try to take attendance for classes they are not assigned to.
- **Boletim depends on grade entry schema being correct:** The bimestre field and valor_maximo per assessment must be in place before the boletim view can aggregate correctly. The schema already supports this.

---

## MVP Definition

### Launch With (v1) — Deadline 24/05/2026

Minimum viable product to validate the concept and meet academic requirements.

- [ ] Authentication — login, JWT, role-based routing, logout, token refresh
- [ ] Admin: CRUD for usuarios, professores, responsaveis, alunos, turmas, disciplinas
- [ ] Admin: Teacher-class-subject assignment (professor_turma)
- [ ] Admin: Admin dashboard (totals: students, classes, teachers)
- [ ] Teacher: View assigned classes (minhas turmas)
- [ ] Teacher: Attendance registration (fazer chamada) — per class session, bulk mark present/absent for all students in turma
- [ ] Teacher: Assessment creation (avaliacoes) — title, type, bimestre, valor_maximo, date
- [ ] Teacher: Grade entry (lancar notas) — per student per assessment
- [ ] Teacher: Edit past attendance (historico chamadas) — correct mistakes
- [ ] Parent: View children linked to their account
- [ ] Parent: Report card (boletim) — grades per subject per bimestre, with computed average
- [ ] Parent: Attendance report (frequencia) — absences and percentage per subject

### Add After Validation (v1.x)

Features to add once core is proven working and before real deployment.

- [ ] Passing/failing status on boletim — when school confirms their passing threshold (media >= 5.0 or 6.0)
- [ ] Absence alert threshold — flag >25% absences per LDB (legal requirement for real use)
- [ ] PDF export of boletim — needed for parent-teacher meetings; use ReportLab or WeasyPrint
- [ ] Password recovery via email — needed before real users are onboarded
- [ ] Absence justification field visible in parent dashboard (field exists in schema, just needs UI)

### Future Consideration (v2+)

Features to defer until the prototype proves its value.

- [ ] Email/WhatsApp notifications — high UX value but high infra cost; defer until the read-only dashboard is validated
- [ ] Multi-year grade history — defer until ano letivo 2026 data is complete
- [ ] Multi-school support — only relevant if the project is adopted beyond Polo Valinhos
- [ ] Student login — evaluate demand after parents are using the system
- [ ] Analytics and charts — admin reports on at-risk students; add when dataset is large enough to be meaningful

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Authentication + role routing | HIGH | LOW | P1 |
| CRUD: alunos, turmas, disciplinas | HIGH | LOW | P1 |
| CRUD: professores, responsaveis | HIGH | LOW | P1 |
| Teacher-class-subject assignment | HIGH | LOW | P1 |
| Attendance registration (chamada) | HIGH | MEDIUM | P1 |
| Grade entry (notas) | HIGH | MEDIUM | P1 |
| Parent boletim (with computed media) | HIGH | MEDIUM | P1 |
| Parent frequencia view | HIGH | MEDIUM | P1 |
| Admin dashboard (counts) | MEDIUM | LOW | P1 |
| Teacher dashboard (minhas turmas) | MEDIUM | LOW | P1 |
| Edit past attendance | MEDIUM | LOW | P1 |
| Assessment creation (avaliacoes) | HIGH | LOW | P1 |
| Passing/failing status indicator | HIGH | LOW | P2 |
| Absence alert (>25% LDB) | HIGH | MEDIUM | P2 |
| PDF boletim export | MEDIUM | MEDIUM | P2 |
| Password recovery | MEDIUM | MEDIUM | P2 |
| Absence justification in UI | LOW | LOW | P2 |
| Email notifications | MEDIUM | HIGH | P3 |
| WhatsApp integration | MEDIUM | HIGH | P3 |
| Multi-year history | LOW | HIGH | P3 |
| Student login | LOW | MEDIUM | P3 |
| Mobile app | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch (v1 deadline 24/05/2026)
- P2: Should have, add when possible (v1.x post-validation)
- P3: Nice to have, future consideration (v2+)

---

## Competitor / Reference System Analysis

Brazilian schools use a range of systems. The closest reference products for this context:

| Feature | SED (SP state system) | Diário Escola / Activesoft | Our Approach |
|---------|----------------------|---------------------------|--------------|
| Grade entry by bimestre | Yes, 4 bimestres | Yes | Yes — bimestre field on avaliacoes |
| Daily attendance (chamada) | Yes, per aula | Yes, per aula | Yes — per chamada (turma+disciplina+date) |
| Parent portal (boletim) | Yes — read-only web | Yes — read-only web | Yes — responsavel dashboard, read-only |
| PDF export | Yes | Yes | v1.x target |
| Email notifications | Some | Yes (paid tier) | v2+ |
| Multi-school | Yes (state-wide) | Yes (SaaS) | Deliberately excluded from v1 |
| Student login | Yes | Yes | Deliberately excluded from v1 |
| Role-based access | Yes | Yes | Yes — admin/professor/responsavel |
| WhatsApp integration | No | Some vendors | v3+ |

Key insight from Brazilian market: the boletim by bimestre (4 per year) is the universal expectation. Parents specifically look for: nota por bimestre, media final, and percentage of faltas. These three data points are the minimum viable parent dashboard.

---

## Brazilian Context Notes

These are specific to Brazilian K-12 schools and affect feature design decisions:

1. **Bimestral grading cycle:** Brazilian public and private K-12 schools divide the year into 4 bimestres. Grades must be shown per bimestre, not per semester or quarter.

2. **LDB 25% absence rule:** Article 24, Section VI of Lei de Diretrizes e Bases (LDB 9394/96) states that a student failing to attend 75% of classes per subject fails automatically, regardless of grades. The system must track and display frequency percentage so parents can see when a child is at risk. This is a legal compliance issue, not just a nice-to-have.

3. **LGPD compliance:** LGPD Article 14 requires explicit parental consent for processing data of minors (crianças e adolescentes). For a prototype at a single polo, administrative enrollment by admin (creating the responsavel account and linking it to the student) satisfies consent implicitly — the parent is being given access, not having data harvested. For production deployment, a formal consent record should be added.

4. **CPF as identity anchor:** Brazilian school systems use CPF as the unique identifier for adults (responsaveis and professores). The schema already includes CPF on responsaveis. This is correct and expected.

5. **Turno (shift):** Brazilian schools commonly operate in multiple shifts (matutino, vespertino, noturno). The schema models this on turmas. The UI should surface this to avoid teachers taking attendance for the wrong shift.

---

## Sources

- Team meeting notes: `docs/Ata 01_02 - Reunião PI Turma 19.md`
- Project vision: `docs/projeto-visao-geral.md`
- Database schema: `docs/database-schema.md`
- Brazilian SIS reference: [Secretaria Escolar Digital - SP](https://sed.educacao.sp.gov.br/)
- Brazilian SIS reference: [Diário Escola](https://diarioescola.com.br/)
- [Activesoft — Diário de Classe Online](https://activesoft.com.br/diario-de-classe-online-2/)
- [Boletim Escolar Online 2024 — via carreira](https://viacarreira.com/boletim-escolar-online/)
- [LGPD nas Escolas — isaac.com.br](https://isaac.com.br/blog/lgpd-nas-escolas)
- [LGPD e educação — Serpro](https://www.serpro.gov.br/lgpd/noticias/2020/educacao-lgpd)
- [What is a SIS? — Classe365](https://www.classe365.com/blog/what-is-a-student-information-system-sis-features-and-benefits/)
- [School Management MVP — lowcode.agency](https://www.lowcode.agency/blog/build-school-management-app-bubble)
- [Parent Portal overview — Maestro SIS](https://www.bocavox.com/student-guardian-portal-system)

---
*Feature research for: Sistema Web de Registro Escolar — UNIVESP Polo Valinhos*
*Researched: 2026-04-26*
