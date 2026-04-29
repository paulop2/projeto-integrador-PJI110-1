"""
Seed script — popula o banco com dados de demonstração realistas.
Uso: cd backend && source venv/bin/activate && python seed.py
"""
import sys
import os
import random
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(__file__))

from passlib.context import CryptContext
from src.database import SessionLocal, engine
from src.models.usuario import Usuario
from src.models.professor import Professor
from src.models.responsavel import Responsavel
from src.models.turma import Turma
from src.models.disciplina import Disciplina
from src.models.aluno import Aluno
from src.models.professor_turma import ProfessorTurma
from src.models.chamada import Chamada
from src.models.presenca import Presenca
from src.models.avaliacao import Avaliacao
from src.models.nota import Nota

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pw(plain: str) -> str:
    return pwd_context.hash(plain)


def weekdays_in_range(start: date, end: date):
    """Retorna todos os dias úteis (seg-sex) entre start e end (inclusive)."""
    days = []
    d = start
    while d <= end:
        if d.weekday() < 5:
            days.append(d)
        d += timedelta(days=1)
    return days


def run():
    db = SessionLocal()
    try:
        # ------------------------------------------------------------------
        # Guarda. Não rodar duas vezes sem limpar o banco.
        # ------------------------------------------------------------------
        if db.query(Professor).count() > 0:
            print("Seed já foi executado. Rode `make migrate` com downgrade primeiro.")
            return

        # ------------------------------------------------------------------
        # Disciplinas
        # ------------------------------------------------------------------
        disc_data = [
            ("Matemática", 80),
            ("Português", 80),
            ("Ciências", 60),
            ("História", 60),
            ("Geografia", 60),
            ("Inglês", 40),
        ]
        disciplinas = []
        for nome, ch in disc_data:
            d = Disciplina(nome=nome, carga_horaria=ch)
            db.add(d)
            disciplinas.append(d)
        db.flush()

        mat, por, cie, his, geo, ing = disciplinas

        # ------------------------------------------------------------------
        # Turmas
        # ------------------------------------------------------------------
        turma_data = [
            ("6º Ano A", 2026, "6º Ano", "Manhã"),
            ("7º Ano B", 2026, "7º Ano", "Tarde"),
            ("8º Ano C", 2026, "8º Ano", "Manhã"),
        ]
        turmas = []
        for nome, ano, serie, turno in turma_data:
            t = Turma(nome=nome, ano=ano, serie=serie, turno=turno)
            db.add(t)
            turmas.append(t)
        db.flush()

        turma6a, turma7b, turma8c = turmas

        # ------------------------------------------------------------------
        # Professores (usuario + perfil)
        # ------------------------------------------------------------------
        profs_data = [
            ("João Silva", "prof.joao@escola.dev", "Prof@123", "123.456.789-00"),
            ("Maria Souza", "prof.maria@escola.dev", "Prof@123", "234.567.890-11"),
            ("Carlos Oliveira", "prof.carlos@escola.dev", "Prof@123", "345.678.901-22"),
            ("Ana Lima", "prof.ana@escola.dev", "Prof@123", "456.789.012-33"),
        ]
        professores = []
        for nome, email, senha, cpf in profs_data:
            u = Usuario(email=email, senha_hash=hash_pw(senha), tipo="professor", ativo=True)
            db.add(u)
            db.flush()
            p = Professor(usuario_id=u.id, nome=nome, cpf=cpf)
            db.add(p)
            db.flush()
            professores.append(p)

        joao, maria, carlos, ana = professores

        # ------------------------------------------------------------------
        # Responsáveis (usuario + perfil)
        # ------------------------------------------------------------------
        resps_data = [
            ("Pedro Almeida",    "resp.pedro@escola.dev",    "Resp@123", "111.222.333-44", "(11) 99001-0001"),
            ("Lúcia Ferreira",   "resp.lucia@escola.dev",    "Resp@123", "222.333.444-55", "(11) 99001-0002"),
            ("Roberto Costa",    "resp.roberto@escola.dev",  "Resp@123", "333.444.555-66", "(11) 99001-0003"),
            ("Fernanda Martins", "resp.fernanda@escola.dev", "Resp@123", "444.555.666-77", "(11) 99001-0004"),
            ("Marcos Rocha",     "resp.marcos@escola.dev",   "Resp@123", "555.666.777-88", "(21) 98002-0005"),
            ("Cláudia Nunes",    "resp.claudia@escola.dev",  "Resp@123", "666.777.888-99", "(21) 98002-0006"),
        ]
        responsaveis = []
        for nome, email, senha, cpf, tel in resps_data:
            u = Usuario(email=email, senha_hash=hash_pw(senha), tipo="responsavel", ativo=True)
            db.add(u)
            db.flush()
            r = Responsavel(usuario_id=u.id, nome=nome, cpf=cpf, telefone=tel)
            db.add(r)
            db.flush()
            responsaveis.append(r)

        pedro, lucia, roberto, fernanda, marcos, claudia = responsaveis

        # ------------------------------------------------------------------
        # Alunos — 6 por turma
        # ------------------------------------------------------------------
        ANO = 2026
        alunos_raw = [
            # Turma 6A
            ("Lucas Almeida",      date(2013, 3, 15),  turma6a.id, pedro.id),
            ("Sofia Almeida",      date(2013, 7, 22),  turma6a.id, pedro.id),
            ("Gabriel Ferreira",   date(2013, 11, 5),  turma6a.id, lucia.id),
            ("Isabela Ferreira",   date(2014, 1, 30),  turma6a.id, lucia.id),
            ("Mateus Costa",       date(2013, 5, 18),  turma6a.id, roberto.id),
            ("Laura Costa",        date(2013, 9, 12),  turma6a.id, roberto.id),
            # Turma 7B
            ("Rafael Martins",     date(2012, 2, 28),  turma7b.id, fernanda.id),
            ("Beatriz Martins",    date(2012, 6, 14),  turma7b.id, fernanda.id),
            ("Felipe Rocha",       date(2012, 8, 3),   turma7b.id, marcos.id),
            ("Julia Rocha",        date(2012, 12, 20), turma7b.id, marcos.id),
            ("Arthur Nunes",       date(2012, 4, 9),   turma7b.id, claudia.id),
            ("Valentina Nunes",    date(2012, 10, 17), turma7b.id, claudia.id),
            # Turma 8C
            ("Pedro Alves",        date(2011, 1, 7),   turma8c.id, pedro.id),
            ("Ana Alves",          date(2011, 3, 25),  turma8c.id, lucia.id),
            ("Bruno Lima",         date(2011, 6, 11),  turma8c.id, roberto.id),
            ("Camila Lima",        date(2011, 8, 29),  turma8c.id, fernanda.id),
            ("Diego Santos",       date(2011, 11, 14), turma8c.id, marcos.id),
            ("Mariana Santos",     date(2011, 2, 3),   turma8c.id, claudia.id),
        ]
        alunos = []
        for nome, nasc, turma_id, resp_id in alunos_raw:
            a = Aluno(nome=nome, data_nascimento=nasc, turma_id=turma_id, responsavel_id=resp_id, ativo=True)
            db.add(a)
            db.flush()
            a.matricula = f"{ANO}{a.id:04d}"
            alunos.append(a)
        db.flush()

        # ------------------------------------------------------------------
        # Professor × Turma × Disciplina
        # ------------------------------------------------------------------
        pt_links = [
            # 6A
            (joao.id,   turma6a.id, mat.id),
            (maria.id,  turma6a.id, por.id),
            (carlos.id, turma6a.id, cie.id),
            (carlos.id, turma6a.id, his.id),
            (ana.id,    turma6a.id, geo.id),
            (ana.id,    turma6a.id, ing.id),
            # 7B
            (joao.id,   turma7b.id, mat.id),
            (maria.id,  turma7b.id, por.id),
            (carlos.id, turma7b.id, cie.id),
            (carlos.id, turma7b.id, his.id),
            (ana.id,    turma7b.id, geo.id),
            (ana.id,    turma7b.id, ing.id),
            # 8C
            (joao.id,   turma8c.id, mat.id),
            (maria.id,  turma8c.id, por.id),
            (carlos.id, turma8c.id, his.id),
            (ana.id,    turma8c.id, geo.id),
            (ana.id,    turma8c.id, ing.id),
        ]
        for prof_id, turma_id, disc_id in pt_links:
            db.add(ProfessorTurma(professor_id=prof_id, turma_id=turma_id, disciplina_id=disc_id))
        db.flush()

        # ------------------------------------------------------------------
        # Chamadas + Presenças — 8 semanas de aulas (seg-sex)
        # ------------------------------------------------------------------
        seed_start = date(2026, 2, 16)
        seed_end   = date(2026, 4, 11)
        dias_uteis = weekdays_in_range(seed_start, seed_end)

        # Mapeamento turma → alunos
        alunos_por_turma = {
            turma6a.id: [a for a in alunos if a.turma_id == turma6a.id],
            turma7b.id: [a for a in alunos if a.turma_id == turma7b.id],
            turma8c.id: [a for a in alunos if a.turma_id == turma8c.id],
        }

        # Para cada turma, roda disciplinas nos dias da semana (2 discs/turma por dia)
        disc_por_turma = {
            turma6a.id: [(mat.id, joao.id), (por.id, maria.id), (cie.id, carlos.id), (his.id, carlos.id)],
            turma7b.id: [(mat.id, joao.id), (por.id, maria.id), (cie.id, carlos.id), (geo.id, ana.id)],
            turma8c.id: [(mat.id, joao.id), (por.id, maria.id), (his.id, carlos.id), (ing.id, ana.id)],
        }

        rng = random.Random(42)

        # Perfis de presença por aluno (alguns faltam mais)
        presenca_prob = {}
        for a in alunos:
            roll = rng.random()
            if roll < 0.1:
                presenca_prob[a.id] = 0.55   # aluno com muitas faltas
            elif roll < 0.25:
                presenca_prob[a.id] = 0.75
            else:
                presenca_prob[a.id] = 0.92   # maioria frequente

        for turma in turmas:
            discs = disc_por_turma[turma.id]
            alunos_t = alunos_por_turma[turma.id]

            for idx, d in enumerate(dias_uteis):
                disc_id, prof_id = discs[idx % len(discs)]
                chamada = Chamada(
                    turma_id=turma.id,
                    disciplina_id=disc_id,
                    professor_id=prof_id,
                    data=d,
                )
                db.add(chamada)
                db.flush()

                for aluno in alunos_t:
                    presente = rng.random() < presenca_prob[aluno.id]
                    justificativa = None
                    if not presente and rng.random() < 0.4:
                        justificativa = rng.choice([
                            "Atestado médico",
                            "Viagem em família",
                            "Consulta médica",
                        ])
                    db.add(Presenca(
                        chamada_id=chamada.id,
                        aluno_id=aluno.id,
                        presente=presente,
                        justificativa=justificativa,
                    ))
        db.flush()

        # ------------------------------------------------------------------
        # Avaliações + Notas — bimestres 1 e 2
        # ------------------------------------------------------------------
        aval_data = [
            # (turma, disc, prof, titulo, bimestre, data)
            # Bimestre 1
            (turma6a, mat, joao,   "Prova 1 — Números e Operações",   1, date(2026, 3, 10)),
            (turma6a, por, maria,  "Prova 1 — Interpretação de Texto", 1, date(2026, 3, 12)),
            (turma6a, cie, carlos, "Prova 1 — Seres Vivos",           1, date(2026, 3, 14)),
            (turma6a, his, carlos, "Prova 1 — Antiguidade",           1, date(2026, 3, 17)),
            (turma7b, mat, joao,   "Prova 1 — Frações e Decimais",    1, date(2026, 3, 10)),
            (turma7b, por, maria,  "Prova 1 — Gramática",             1, date(2026, 3, 12)),
            (turma7b, cie, carlos, "Prova 1 — Ecossistemas",          1, date(2026, 3, 14)),
            (turma7b, geo, ana,    "Prova 1 — Geografia Física",      1, date(2026, 3, 17)),
            (turma8c, mat, joao,   "Prova 1 — Álgebra Básica",        1, date(2026, 3, 10)),
            (turma8c, por, maria,  "Prova 1 — Produção Textual",      1, date(2026, 3, 12)),
            (turma8c, his, carlos, "Prova 1 — Brasil Colonial",       1, date(2026, 3, 14)),
            (turma8c, ing, ana,    "Prova 1 — Present Simple",        1, date(2026, 3, 17)),
            # Bimestre 2
            (turma6a, mat, joao,   "Prova 2 — Geometria",             2, date(2026, 4, 7)),
            (turma6a, por, maria,  "Prova 2 — Redação",               2, date(2026, 4, 9)),
            (turma6a, cie, carlos, "Prova 2 — Corpo Humano",          2, date(2026, 4, 11)),
            (turma6a, his, carlos, "Prova 2 — Grécia Antiga",         2, date(2026, 4, 14)),
            (turma7b, mat, joao,   "Prova 2 — Equações",              2, date(2026, 4, 7)),
            (turma7b, por, maria,  "Prova 2 — Literatura",            2, date(2026, 4, 9)),
            (turma7b, cie, carlos, "Prova 2 — Fotossíntese",          2, date(2026, 4, 11)),
            (turma7b, geo, ana,    "Prova 2 — Climas do Mundo",       2, date(2026, 4, 14)),
            (turma8c, mat, joao,   "Prova 2 — Funções do 1º Grau",    2, date(2026, 4, 7)),
            (turma8c, por, maria,  "Prova 2 — Análise Sintática",     2, date(2026, 4, 9)),
            (turma8c, his, carlos, "Prova 2 — Independência do Brasil", 2, date(2026, 4, 14)),
            (turma8c, ing, ana,    "Prova 2 — Past Simple",           2, date(2026, 4, 14)),
        ]

        # Perfis de nota por aluno
        nota_media = {}
        for a in alunos:
            roll = rng.random()
            if roll < 0.08:
                nota_media[a.id] = (3.0, 5.5)    # em risco
            elif roll < 0.20:
                nota_media[a.id] = (5.0, 7.0)    # mediano
            elif roll < 0.85:
                nota_media[a.id] = (6.5, 9.0)    # bom
            else:
                nota_media[a.id] = (8.5, 10.0)   # excelente

        alunos_por_turma_id = {
            turma6a.id: [a for a in alunos if a.turma_id == turma6a.id],
            turma7b.id: [a for a in alunos if a.turma_id == turma7b.id],
            turma8c.id: [a for a in alunos if a.turma_id == turma8c.id],
        }

        for turma, disc, prof, titulo, bimestre, dt in aval_data:
            av = Avaliacao(
                turma_id=turma.id,
                disciplina_id=disc.id,
                professor_id=prof.id,
                titulo=titulo,
                bimestre=bimestre,
                valor_maximo=10.0,
                data=dt,
            )
            db.add(av)
            db.flush()

            for aluno in alunos_por_turma_id[turma.id]:
                lo, hi = nota_media[aluno.id]
                valor = round(rng.uniform(lo, hi), 1)
                valor = min(10.0, max(0.0, valor))
                db.add(Nota(avaliacao_id=av.id, aluno_id=aluno.id, valor=valor))

        db.commit()
        print("✓ Seed concluído com sucesso!")
        print()
        print("Credenciais:")
        print("  Admin:       admin@escola.dev         / Admin@123")
        print("  Professores: prof.joao@escola.dev     / Prof@123")
        print("               prof.maria@escola.dev    / Prof@123")
        print("               prof.carlos@escola.dev   / Prof@123")
        print("               prof.ana@escola.dev      / Prof@123")
        print("  Responsáveis: resp.pedro@escola.dev   / Resp@123")
        print("                resp.lucia@escola.dev   / Resp@123")
        print("                resp.roberto@escola.dev / Resp@123")
        print("                resp.fernanda@escola.dev/ Resp@123")
        print("                resp.marcos@escola.dev  / Resp@123")
        print("                resp.claudia@escola.dev / Resp@123")

    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run()
