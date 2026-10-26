from uuid import uuid4

import jaydebeapi
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from auth.auth_dependency import get_current_user
from utils.database import Base, H2_JAR_PATH, get_db


@pytest.fixture
def isolated_database():
    database_name = f"test_{uuid4().hex}"

    def connect_to_test_database():
        return jaydebeapi.connect(
            "org.h2.Driver",
            f"jdbc:h2:mem:{database_name}",
            jars=[str(H2_JAR_PATH)],
        )

    test_engine = create_engine(
        "h2:///isolated_test",
        creator=connect_to_test_database,
    )
    Base.metadata.create_all(bind=test_engine)
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine,
    )

    def override_get_db():
        with TestSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = lambda: "test-user"
    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        test_engine.dispose()
