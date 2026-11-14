"""Run the real Alembic migrations against a fresh SQLite database."""

import os
import subprocess
import sys
from pathlib import Path

from sqlalchemy import create_engine, inspect, text

BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_DIR.parent


def _run(args, db_url):
    env = {**os.environ, "DATABASE_URL": db_url, "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run(
        [sys.executable, *args],
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_fresh_database_upgrade_check_and_seed(tmp_path):
    db_url = f"sqlite:///{(tmp_path / 'fresh.db').as_posix()}"

    upgrade = _run(["-m", "alembic", "upgrade", "head"], db_url)
    assert upgrade.returncode == 0, upgrade.stderr

    check = _run(["-m", "alembic", "check"], db_url)
    assert check.returncode == 0, check.stdout + check.stderr

    engine = create_engine(db_url)
    columns = {c["name"]: c for c in inspect(engine).get_columns("progress")}
    assert columns["attention_score"]["nullable"] is True
    assert {"yawning", "looking_away"} <= set(columns)

    # Seeding twice must not duplicate anything.
    for _ in range(2):
        seed = _run([str(BACKEND_DIR / "seed_science.py")], db_url)
        assert seed.returncode == 0, seed.stderr

    with engine.connect() as conn:
        assert conn.execute(text("select count(*) from lessons")).scalar() == 5
        assert conn.execute(text("select count(*) from quizzes")).scalar() == 15
        assert conn.execute(text("select count(*) from questions")).scalar() == 75
        difficulties = {r[0] for r in conn.execute(text("select distinct difficulty from quizzes"))}
    assert difficulties == {"EASY", "MEDIUM", "HARD"}
    engine.dispose()


def test_quiz_attempt_migration_upgrades_and_downgrades(tmp_path):
    db_url = f"sqlite:///{(tmp_path / 'attempts.db').as_posix()}"
    assert _run(["-m", "alembic", "upgrade", "head"], db_url).returncode == 0

    engine = create_engine(db_url)
    tables = set(inspect(engine).get_table_names())
    assert {"quiz_attempts", "quiz_attempt_events"} <= tables
    indexes = {i["name"]: i for i in inspect(engine).get_indexes("quiz_attempts")}
    assert indexes["uq_quiz_attempts_open"]["unique"]
    engine.dispose()

    down = _run(["-m", "alembic", "downgrade", "0006_curriculum"], db_url)
    assert down.returncode == 0, down.stderr
    engine = create_engine(db_url)
    assert "quiz_attempts" not in set(inspect(engine).get_table_names())
    assert "progress" in set(inspect(engine).get_table_names())
    engine.dispose()

    assert _run(["-m", "alembic", "upgrade", "head"], db_url).returncode == 0
