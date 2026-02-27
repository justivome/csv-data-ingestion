from collections.abc import Generator

from sqlmodel import Session, create_engine

from app.settings import db

db_engine = create_engine(db.postgres_url)


def get_session() -> Generator[Session, None, None]:
    with Session(db_engine) as session:
        yield session
