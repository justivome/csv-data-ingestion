import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.db import get_session
from app.main import app

TEST_DATABASE_URL = "sqlite:///./tests/test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})


def get_test_session():
    with Session(engine) as session:
        yield session


@pytest.fixture(autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_session] = get_test_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
