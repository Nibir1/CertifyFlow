import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def client():
    # UPDATE: We strictly manage the context manager
    with TestClient(app) as c:
        yield c