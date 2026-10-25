import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth.jwt_handler import create_access_token
from app.main import app


class SettingsContractTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def auth_headers(self, user_id="user-123", role="mr"):
        token = create_access_token(
            {"sub": user_id, "email": "user@example.com", "role": role, "name": "Demo User"}
        )
        return {"Authorization": f"Bearer {token}"}

    @patch("app.routes.settings.get_supabase")
    def test_profile_reads_authenticated_representative(self, get_supabase):
        get_supabase.return_value = FakeSupabase(
            [
                {
                    "id": "mr-123",
                    "user_id": "user-123",
                    "territory": "Pune Central",
                    "vehicle_type": "two_wheeler",
                    "start_location": "home",
                    "working_start": "09:00",
                    "working_end": "18:00",
                    "target_visits_per_day": 8,
                    "preferences": {"traffic_reroute": True},
                }
            ]
        )

        response = self.client.get("/api/settings/profile", headers=self.auth_headers())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["preferences"]["rep_id"], "mr-123")
        self.assertEqual(response.json()["preferences"]["territory"], "Pune Central")

    @patch("app.routes.settings.get_supabase")
    def test_profile_update_persists_only_for_authenticated_representative(self, get_supabase):
        database = FakeSupabase(
            [{"id": "mr-123", "user_id": "user-123", "territory": "Pune Central"}]
        )
        get_supabase.return_value = database

        response = self.client.patch(
            "/api/settings/profile",
            headers=self.auth_headers(),
            json={"territory": "Pune West"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(database.rows[0]["territory"], "Pune West")

    def test_manager_cannot_update_representative_settings(self):
        response = self.client.patch(
            "/api/settings/profile",
            headers=self.auth_headers(user_id="manager-1", role="manager"),
            json={"territory": "Restricted"},
        )

        self.assertEqual(response.status_code, 403)


class FakeSupabase:
    def __init__(self, rows):
        self.rows = rows

    def table(self, _name):
        return FakeQuery(self.rows)


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows
        self.filters = {}
        self.update_data = None

    def select(self, _columns):
        return self

    def eq(self, column, value):
        self.filters[column] = value
        return self

    def update(self, data):
        self.update_data = data
        return self

    def execute(self):
        matching = [
            row for row in self.rows
            if all(row.get(column) == value for column, value in self.filters.items())
        ]
        if self.update_data:
            for row in matching:
                row.update(self.update_data)
        return FakeResponse(matching)


class FakeResponse:
    def __init__(self, data):
        self.data = data


if __name__ == "__main__":
    unittest.main()