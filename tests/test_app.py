import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = copy.deepcopy(original)


def test_unregister_participant_removes_them_from_activity():
    client = TestClient(app_module.app)

    signup_response = client.post(
        "/activities/Chess Club/signup?email=student@example.com"
    )
    assert signup_response.status_code == 200

    remove_response = client.delete(
        "/activities/Chess Club/participants/student@example.com"
    )
    assert remove_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert "student@example.com" not in activities_response.json()["Chess Club"]["participants"]
