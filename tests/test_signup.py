import pytest


class TestSignup:
    def test_successful_signup(self, client):
        """Test successful student signup for an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            json={}
        )

        # Assert
        assert response.status_code == 200
        assert f"Signed up {email}" in response.json()["message"]
        
        # Verify participant was added
        final_response = client.get("/activities")
        final_participants = final_response.json()[activity_name]["participants"]
        assert len(final_participants) == len(initial_participants) + 1
        assert email in final_participants

    def test_duplicate_signup_returns_400(self, client):
        """Test that duplicate signup returns 400 error"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            json={}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_invalid_activity_returns_404(self, client):
        """Test that signup for non-existent activity returns 404"""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            json={}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    @pytest.mark.parametrize("email", [
        "alice@mergington.edu",
        "bob@mergington.edu",
        "charlie@mergington.edu"
    ])
    def test_multiple_signups(self, client, email):
        """Test multiple different students can sign up"""
        # Arrange
        activity_name = "Art Club"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            json={}
        )

        # Assert
        assert response.status_code == 200
        assert email in client.get("/activities").json()[activity_name]["participants"]
