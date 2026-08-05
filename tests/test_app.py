import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to their original state before and after each test."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities = copy.deepcopy(original)


def test_unregister_participant_removes_them_from_activity():
    """A participant can be signed up and then removed from an activity."""
    # Arrange
    client = TestClient(app_module.app)
    activity_name = "Chess Club"
    student_email = "student@example.com"

    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={student_email}"
    )

    # Act
    remove_response = client.delete(
        f"/activities/{activity_name}/participants/{student_email}"
    )
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200, "Signup should succeed"
    assert remove_response.status_code == 200, "Participant removal should succeed"
    assert activities_response.status_code == 200, "Fetching activities should succeed"

    activities_data = activities_response.json()
    participants = activities_data[activity_name]["participants"]
    assert student_email not in participants, "Removed participant should no longer appear in the activity"

