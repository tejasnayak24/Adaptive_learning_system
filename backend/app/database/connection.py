import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# SQL statement logging is opt-in via SQL_ECHO (not DEBUG): echoed SQL
# includes bound parameters such as e-mail addresses and password hashes,
# so it must never be switched on implicitly.
SQL_ECHO = os.getenv("SQL_ECHO", "False").lower() == "true"

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=SQL_ECHO,
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

        