import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth.jwt_handler import create_access_token
from app.main import app


class DashboardContractTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def headers(self, mr_id):
        token = create_access_token({"sub": "user-1", "role": "mr", "mr_id": mr_id})
        return {"Authorization": f"Bearer {token}"}

    @patch("app.routes.dashboard.get_supabase")
    def test_mr_can_read_own_dashboard(self, get_supabase):
        get_supabase.return_value = FakeSupabase([])

        response = self.client.get(
            "/api/dashboard/mr",
            params={"mr_id": "mr-1"},
            headers=self.headers("mr-1"),
        )

        self.assertEqual(response.status_code, 200)

    @patch("app.routes.dashboard.get_supabase")
    def test_mr_cannot_read_another_mr_dashboard(self, get_supabase):
        response = self.client.get(
            "/api/dashboard/mr",
            params={"mr_id": "mr-2"},
            headers=self.headers("mr-1"),
        )

        self.assertEqual(response.status_code, 403)
        get_supabase.assert_not_called()


class FakeSupabase:
    def __init__(self, rows):
        self.rows = rows

    def table(self, _name):
        return FakeQuery(self.rows)


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows

    def select(self, _columns):
        return self

    def eq(self, _column, _value):
        return self

    def execute(self):
        return type("FakeResponse", (), {"data": self.rows})()


if __name__ == "__main__":
    unittest.main()