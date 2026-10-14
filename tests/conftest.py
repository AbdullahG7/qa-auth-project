import pytest
from fastapi.testclient import TestClient
from app import main


@pytest.fixture(autouse=True)
def clean_state():
    """Reset the in-memory data before every test so tests stay independent."""
    main.users.clear()
    main.tokens.clear()
    main.failed.clear()
    yield


@pytest.fixture
def client():
    return TestClient(main.app)


@pytest.fixture
def register(client):
    def _register(username="alice_1", password="Passw0rd123"):
        return client.post("/register", json={"username": username, "password": password})
    return _register


@pytest.fixture
def login(client):
    def _login(username="alice_1", password="Passw0rd123"):
        return client.post("/login", json={"username": username, "password": password})
    return _login
