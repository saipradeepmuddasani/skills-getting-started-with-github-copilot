import pytest


class TestUnregister:
    def test_successful_unregister(self, client):
        """Test successful student unregister from an activity"""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        initial_response = client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}",
            json={}
        )

        # Assert
        assert response.status_code == 200
        assert f"Unregistered {email}" in response.json()["message"]
        
        # Verify participant was removed
        final_response = client.get("/activities")
        final_count = len(final_response.json()[activity_name]["participants"])
        assert final_count == initial_count - 1
        assert email not in final_response.json()[activity_name]["participants"]

    def test_unregister_non_signed_up_student_returns_400(self, client):
        """Test that unregistering a student not signed up returns 400"""
        # Arrange
        activity_name = "Chess Club"
        email = "notthere@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}",
            json={}
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_invalid_activity_returns_404(self, client):
        """Test that unregister from non-existent activity returns 404"""
        # Arrange
        activity_name = "Fake Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}",
            json={}
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_then_signup_again(self, client):
        """Test that a student can unregister and then sign up again"""
        # Arrange
        activity_name = "Programming Class"
        email = "student@mergington.edu"

        # Act - signup
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            json={}
        )
        assert signup_response.status_code == 200

        # Act - unregister
        unregister_response = client.post(
            f"/activities/{activity_name}/unregister?email={email}",
            json={}
        )
        assert unregister_response.status_code == 200

        # Act - signup again
        signup_again_response = client.post(
            f"/activities/{activity_name}/signup?email={email}",
            json={}
        )

        # Assert
        assert signup_again_response.status_code == 200
        assert email in client.get("/activities").json()[activity_name]["participants"]
