import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture
def client():
    """Return a synchronous TestClient for the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities():
    """Autouse fixture that snapshots and restores `src.app.activities` between tests.

    Uses deep copies so tests are isolated and deterministic.
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = copy.deepcopy(original)
