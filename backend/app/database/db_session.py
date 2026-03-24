from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Default to a local SQLite DB for development if DATABASE_URL not provided.
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    sqlite_path = os.path.join(os.path.dirname(__file__), '..', '..', 'dev.db')
    DATABASE_URL = f"sqlite:///{sqlite_path}"

engine = create_engine(DATABASE_URL, future=True, connect_args={"check_same_thread": False} if DATABASE_URL.startswith('sqlite') else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class DBSession:
    def get_session(self):
        return SessionLocal()


db_session = DBSession()
