import pytest


class TestGetActivities:
    def test_get_all_activities(self, client):
        """Test retrieving all activities"""
        # Arrange - no setup needed, using fixture

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0
        assert "Chess Club" in activities
        assert "Programming Class" in activities

    def test_activities_have_required_fields(self, client):
        """Test that each activity has all required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_activities_contain_correct_participant_data(self, client):
        """Test that activities have correct participant emails"""
        # Arrange
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert activities["Chess Club"]["participants"] == expected_chess_participants
