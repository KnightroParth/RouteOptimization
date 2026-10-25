import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


class HealthContractTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch("app.main.get_supabase")
    def test_ready_reports_database_ready(self, get_supabase):
        get_supabase.return_value = FakeSupabase()

        response = self.client.get("/api/ready")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ready", "database": "ready"})

    @patch("app.main.get_supabase", side_effect=RuntimeError("database unavailable"))
    def test_ready_reports_dependency_failure(self, _get_supabase):
        response = self.client.get("/api/ready")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["status"], "not_ready")


class FakeSupabase:
    def table(self, _name):
        return self

    def select(self, _columns):
        return self

    def limit(self, _count):
        return self

    def execute(self):
        return type("FakeResponse", (), {"data": []})()


if __name__ == "__main__":
    unittest.main()