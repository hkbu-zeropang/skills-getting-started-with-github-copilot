from urllib.parse import quote

import src.app as app_module


def _signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name)}/signup"


def test_get_activities(client):
    # Arrange: nothing to set up (autouse fixture resets data)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "test.user@example.com"
    assert email not in app_module.activities[activity]["participants"]

    # Act
    resp = client.post(_signup_path(activity), params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity}"
    assert email in app_module.activities[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "duplicate.user@example.com"

    # Act: first signup succeeds
    resp1 = client.post(_signup_path(activity), params={"email": email})
    assert resp1.status_code == 200

    # Act: duplicate signup
    resp2 = client.post(_signup_path(activity), params={"email": email})

    # Assert
    assert resp2.status_code == 400
    detail = resp2.json().get("detail", "")
    assert "already signed up" in detail.lower()


def test_signup_activity_not_found_returns_404(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "someone@example.com"

    # Act
    resp = client.post(_signup_path(activity), params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Activity not found"


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    assert email in app_module.activities[activity]["participants"]

    # Act
    resp = client.delete(_signup_path(activity), params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_not_found_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "not.exists@example.com"
    assert email not in app_module.activities[activity]["participants"]

    # Act
    resp = client.delete(_signup_path(activity), params={"email": email})

    # Assert
    assert resp.status_code == 404
    assert resp.json().get("detail") == "Participant not found for this activity"
