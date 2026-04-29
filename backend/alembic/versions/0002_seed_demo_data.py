"""seed demo data

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-29 00:00:00.000000

Popula o banco com dados de demonstração realistas para o ambiente de produção.
Roda automaticamente em todo novo deploy via `alembic upgrade head`.

Senhas:
  Admin:        Admin@123
  Professores:  Prof@123
  Responsáveis: Resp@123
"""

from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

# Hashes pré-computados com bcrypt cost=12
_HASH_PROF = "$2b$12$.FC/dOKuZkJpTJtle7Cx1efZ1mwsJpPkQVdu8QL83br4Lh5IlZ.ZW"
_HASH_RESP = "$2b$12$QucrpN028GdpJwdEbyIpn.FAtjcEb48ZqeWu19j3hsHMRXUiPhTDy"


def upgrade() -> None:
    # ------------------------------------------------------------------
    # Disciplinas
    # ------------------------------------------------------------------
    op.execute("""
        INSERT INTO disciplinas (nome, carga_horaria) VALUES
            ('Matemática',  80),
            ('Português',   80),
            ('Ciências',    60),
            ('História',    60),
            ('Geografia',   60),
            ('Inglês',      40)
    """)

    # ------------------------------------------------------------------
    # Turmas
    # ------------------------------------------------------------------
    op.execute("""
        INSERT INTO turmas (nome, ano, serie, turno) VALUES
            ('6º Ano A', 2026, '6º Ano', 'Manhã'),
            ('7º Ano B', 2026, '7º Ano', 'Tarde'),
            ('8º Ano C', 2026, '8º Ano', 'Manhã')
    """)

    # ------------------------------------------------------------------
    # Usuários → Professores
    # ------------------------------------------------------------------
    op.execute(f"""
        INSERT INTO usuarios (email, senha_hash, tipo, ativo) VALUES
            ('prof.joao@escola.dev',   '{_HASH_PROF}', 'professor', 1),
            ('prof.maria@escola.dev',  '{_HASH_PROF}', 'professor', 1),
            ('prof.carlos@escola.dev', '{_HASH_PROF}', 'professor', 1),
            ('prof.ana@escola.dev',    '{_HASH_PROF}', 'professor', 1)
    """)

    # Os IDs de usuário do admin já existem (id=1); os professores ficam id=2..5
    op.execute("""
        INSERT INTO professores (usuario_id, nome, cpf) VALUES
            (2, 'João Silva',      '123.456.789-00'),
            (3, 'Maria Souza',     '234.567.890-11'),
            (4, 'Carlos Oliveira', '345.678.901-22'),
            (5, 'Ana Lima',        '456.789.012-33')
    """)

    # ------------------------------------------------------------------
    # Usuários → Responsáveis
    # ------------------------------------------------------------------
    op.execute(f"""
        INSERT INTO usuarios (email, senha_hash, tipo, ativo) VALUES
            ('resp.pedro@escola.dev',    '{_HASH_RESP}', 'responsavel', 1),
            ('resp.lucia@escola.dev',    '{_HASH_RESP}', 'responsavel', 1),
            ('resp.roberto@escola.dev',  '{_HASH_RESP}', 'responsavel', 1),
            ('resp.fernanda@escola.dev', '{_HASH_RESP}', 'responsavel', 1),
            ('resp.marcos@escola.dev',   '{_HASH_RESP}', 'responsavel', 1),
            ('resp.claudia@escola.dev',  '{_HASH_RESP}', 'responsavel', 1)
    """)

    # usuarios id=6..11
    op.execute("""
        INSERT INTO responsaveis (usuario_id, nome, cpf, telefone) VALUES
            (6,  'Pedro Almeida',    '111.222.333-44', '(11) 99001-0001'),
            (7,  'Lúcia Ferreira',   '222.333.444-55', '(11) 99001-0002'),
            (8,  'Roberto Costa',    '333.444.555-66', '(11) 99001-0003'),
            (9,  'Fernanda Martins', '444.555.666-77', '(11) 99001-0004'),
            (10, 'Marcos Rocha',     '555.666.777-88', '(21) 98002-0005'),
            (11, 'Cláudia Nunes',    '666.777.888-99', '(21) 98002-0006')
    """)

    # ------------------------------------------------------------------
    # Alunos  (responsavel_id = id na tabela responsaveis, turma_id = 1..3)
    # ------------------------------------------------------------------
    op.execute("""
        INSERT INTO alunos (nome, data_nascimento, turma_id, responsavel_id, ativo) VALUES
            -- 6º Ano A (turma_id=1)
            ('Lucas Almeida',      '2013-03-15', 1, 1, 1),
            ('Sofia Almeida',      '2013-07-22', 1, 1, 1),
            ('Gabriel Ferreira',   '2013-11-05', 1, 2, 1),
            ('Isabela Ferreira',   '2014-01-30', 1, 2, 1),
            ('Mateus Costa',       '2013-05-18', 1, 3, 1),
            ('Laura Costa',        '2013-09-12', 1, 3, 1),
            -- 7º Ano B (turma_id=2)
            ('Rafael Martins',     '2012-02-28', 2, 4, 1),
            ('Beatriz Martins',    '2012-06-14', 2, 4, 1),
            ('Felipe Rocha',       '2012-08-03', 2, 5, 1),
            ('Julia Rocha',        '2012-12-20', 2, 5, 1),
            ('Arthur Nunes',       '2012-04-09', 2, 6, 1),
            ('Valentina Nunes',    '2012-10-17', 2, 6, 1),
            -- 8º Ano C (turma_id=3)
            ('Pedro Alves',        '2011-01-07', 3, 1, 1),
            ('Ana Alves',          '2011-03-25', 3, 2, 1),
            ('Bruno Lima',         '2011-06-11', 3, 3, 1),
            ('Camila Lima',        '2011-08-29', 3, 4, 1),
            ('Diego Santos',       '2011-11-14', 3, 5, 1),
            ('Mariana Santos',     '2011-02-03', 3, 6, 1)
    """)

    # matrículas: 20260001..20260018
    op.execute("""
        UPDATE alunos SET matricula = '2026' || printf('%04d', id)
        WHERE matricula IS NULL
    """)

    # ------------------------------------------------------------------
    # Professor × Turma × Disciplina
    # (prof ids: João=1 Maria=2 Carlos=3 Ana=4 — na tabela professores)
    # (disc ids: Mat=1 Por=2 Cie=3 His=4 Geo=5 Ing=6)
    # ------------------------------------------------------------------
    op.execute("""
        INSERT INTO professor_turma (professor_id, turma_id, disciplina_id) VALUES
            -- 6º Ano A
            (1, 1, 1), (2, 1, 2), (3, 1, 3), (3, 1, 4), (4, 1, 5), (4, 1, 6),
            -- 7º Ano B
            (1, 2, 1), (2, 2, 2), (3, 2, 3), (3, 2, 4), (4, 2, 5), (4, 2, 6),
            -- 8º Ano C
            (1, 3, 1), (2, 3, 2), (3, 3, 4), (4, 3, 5), (4, 3, 6)
    """)

    # ------------------------------------------------------------------
    # Chamadas + Presenças — seg-sex de 16/02 a 11/04/2026
    # Gerado com seed fixo para resultado determinístico.
    # ------------------------------------------------------------------
    _insert_chamadas_presencas()

    # ------------------------------------------------------------------
    # Avaliações + Notas — bimestres 1 e 2
    # ------------------------------------------------------------------
    _insert_avaliacoes_notas()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _insert_chamadas_presencas() -> None:
    import random
    from datetime import date, timedelta

    rng = random.Random(42)

    # Dias úteis fev-abr 2026
    start, end = date(2026, 2, 16), date(2026, 4, 11)
    dias: list[date] = []
    d = start
    while d <= end:
        if d.weekday() < 5:
            dias.append(d)
        d += timedelta(days=1)

    # turma_id → [(disc_id, prof_id), ...]  (cycling)
    disc_ciclo = {
        1: [(1, 1), (2, 2), (3, 3), (4, 3)],   # 6A: Mat/João, Por/Maria, Cie/Carlos, His/Carlos
        2: [(1, 1), (2, 2), (3, 3), (5, 4)],   # 7B: Mat, Por, Cie, Geo/Ana
        3: [(1, 1), (2, 2), (4, 3), (6, 4)],   # 8C: Mat, Por, His, Ing/Ana
    }

    # aluno_id 1..18 → probabilidade de presença
    presenca_prob: dict[int, float] = {}
    for aid in range(1, 19):
        roll = rng.random()
        if roll < 0.10:
            presenca_prob[aid] = 0.55
        elif roll < 0.25:
            presenca_prob[aid] = 0.75
        else:
            presenca_prob[aid] = 0.92

    # alunos por turma (1-indexed, matching INSERT order above)
    alunos_turma = {1: list(range(1, 7)), 2: list(range(7, 13)), 3: list(range(13, 19))}

    chamada_rows: list[str] = []
    presenca_rows: list[str] = []

    chamada_id = 0
    for turma_id in (1, 2, 3):
        ciclo = disc_ciclo[turma_id]
        for idx, dt in enumerate(dias):
            disc_id, prof_id = ciclo[idx % len(ciclo)]
            chamada_id += 1
            chamada_rows.append(
                f"({chamada_id}, {turma_id}, {disc_id}, {prof_id}, '{dt}')"
            )
            for aid in alunos_turma[turma_id]:
                presente = 1 if rng.random() < presenca_prob[aid] else 0
                just = 'NULL'
                if not presente and rng.random() < 0.4:
                    just = "'" + rng.choice(['Atestado médico', 'Viagem em família', 'Consulta médica']) + "'"
                presenca_rows.append(f"({chamada_id}, {aid}, {presente}, {just})")

    # Batch inserts (SQLite has a 500-row UNION limit; chunk safely at 200)
    _batch_insert(
        "INSERT INTO chamadas (id, turma_id, disciplina_id, professor_id, data) VALUES",
        chamada_rows,
    )
    _batch_insert(
        "INSERT INTO presencas (chamada_id, aluno_id, presente, justificativa) VALUES",
        presenca_rows,
    )


def _insert_avaliacoes_notas() -> None:
    import random

    rng = random.Random(42)

    # (turma_id, disc_id, prof_id, titulo, bimestre, data)
    avaliacoes = [
        # Bimestre 1
        (1,1,1,"Prova 1 — Números e Operações",    1,"2026-03-10"),
        (1,2,2,"Prova 1 — Interpretação de Texto", 1,"2026-03-12"),
        (1,3,3,"Prova 1 — Seres Vivos",            1,"2026-03-14"),
        (1,4,3,"Prova 1 — Antiguidade",            1,"2026-03-17"),
        (2,1,1,"Prova 1 — Frações e Decimais",     1,"2026-03-10"),
        (2,2,2,"Prova 1 — Gramática",              1,"2026-03-12"),
        (2,3,3,"Prova 1 — Ecossistemas",           1,"2026-03-14"),
        (2,5,4,"Prova 1 — Geografia Física",       1,"2026-03-17"),
        (3,1,1,"Prova 1 — Álgebra Básica",         1,"2026-03-10"),
        (3,2,2,"Prova 1 — Produção Textual",       1,"2026-03-12"),
        (3,4,3,"Prova 1 — Brasil Colonial",        1,"2026-03-14"),
        (3,6,4,"Prova 1 — Present Simple",         1,"2026-03-17"),
        # Bimestre 2
        (1,1,1,"Prova 2 — Geometria",              2,"2026-04-07"),
        (1,2,2,"Prova 2 — Redação",                2,"2026-04-09"),
        (1,3,3,"Prova 2 — Corpo Humano",           2,"2026-04-11"),
        (1,4,3,"Prova 2 — Grécia Antiga",          2,"2026-04-14"),
        (2,1,1,"Prova 2 — Equações",               2,"2026-04-07"),
        (2,2,2,"Prova 2 — Literatura",             2,"2026-04-09"),
        (2,3,3,"Prova 2 — Fotossíntese",           2,"2026-04-11"),
        (2,5,4,"Prova 2 — Climas do Mundo",        2,"2026-04-14"),
        (3,1,1,"Prova 2 — Funções do 1º Grau",     2,"2026-04-07"),
        (3,2,2,"Prova 2 — Análise Sintática",      2,"2026-04-09"),
        (3,4,3,"Prova 2 — Independência do Brasil",2,"2026-04-14"),
        (3,6,4,"Prova 2 — Past Simple",            2,"2026-04-14"),
    ]

    alunos_turma = {1: list(range(1, 7)), 2: list(range(7, 13)), 3: list(range(13, 19))}

    # perfil de nota fixo por aluno
    nota_perfil: dict[int, tuple[float, float]] = {}
    for aid in range(1, 19):
        roll = rng.random()
        if roll < 0.08:
            nota_perfil[aid] = (3.0, 5.5)
        elif roll < 0.20:
            nota_perfil[aid] = (5.0, 7.0)
        elif roll < 0.85:
            nota_perfil[aid] = (6.5, 9.0)
        else:
            nota_perfil[aid] = (8.5, 10.0)

    aval_rows: list[str] = []
    nota_rows: list[str] = []

    for av_id, (turma_id, disc_id, prof_id, titulo, bimestre, dt) in enumerate(avaliacoes, start=1):
        titulo_esc = titulo.replace("'", "''")
        aval_rows.append(
            f"({av_id},{turma_id},{disc_id},{prof_id},'{titulo_esc}',{bimestre},10.0,'{dt}')"
        )
        for aid in alunos_turma[turma_id]:
            lo, hi = nota_perfil[aid]
            valor = round(min(10.0, max(0.0, rng.uniform(lo, hi))), 1)
            nota_rows.append(f"({av_id},{aid},{valor})")

    _batch_insert(
        "INSERT INTO avaliacoes (id,turma_id,disciplina_id,professor_id,titulo,bimestre,valor_maximo,data) VALUES",
        aval_rows,
    )
    _batch_insert(
        "INSERT INTO notas (avaliacao_id,aluno_id,valor) VALUES",
        nota_rows,
    )


def _batch_insert(header: str, rows: list[str], chunk: int = 200) -> None:
    for i in range(0, len(rows), chunk):
        op.execute(header + " " + ",".join(rows[i : i + chunk]))


def downgrade() -> None:
    # Remove tudo em ordem inversa de FK
    op.execute("DELETE FROM notas")
    op.execute("DELETE FROM avaliacoes")
    op.execute("DELETE FROM presencas")
    op.execute("DELETE FROM chamadas")
    op.execute("DELETE FROM professor_turma")
    op.execute("DELETE FROM alunos")
    op.execute("DELETE FROM responsaveis")
    op.execute("DELETE FROM professores")
    op.execute("DELETE FROM disciplinas")
    op.execute("DELETE FROM turmas")
    # Remove usuários de professores e responsáveis (admin fica)
    op.execute("DELETE FROM usuarios WHERE id > 1")
