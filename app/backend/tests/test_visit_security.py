import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth.jwt_handler import create_access_token
from app.main import app


class VisitSecurityTests(unittest.TestCase):
    def setUp(self):
        token = create_access_token({"sub": "user-1", "role": "mr", "mr_id": "mr-1"})
        self.headers = {"Authorization": f"Bearer {token}"}
        self.client = TestClient(app)

    @patch("app.routes.visits.get_supabase")
    def test_daily_visits_reject_another_mr(self, get_supabase):
        response = self.client.get(
            "/api/visits/daily",
            params={"mr_id": "mr-2", "date": "2026-10-25"},
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 403)
        get_supabase.assert_not_called()

    @patch("app.routes.visits.get_supabase")
    def test_visit_list_without_mr_filter_is_scoped_to_current_mr(self, get_supabase):
        get_supabase.return_value = FakeSupabase()

        response = self.client.get("/api/visits", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(get_supabase.return_value.query.filters["mr_id"], "mr-1")

    @patch("app.routes.visits.get_supabase")
    def test_mr_cannot_create_visit_for_another_mr(self, get_supabase):
        response = self.client.post(
            "/api/visits/",
            headers=self.headers,
            json={
                "doctor_id": "doctor-1",
                "mr_id": "mr-2",
                "visit_date": "2026-10-25",
            },
        )

        self.assertEqual(response.status_code, 403)
        get_supabase.assert_not_called()


class FakeSupabase:
    def __init__(self):
        self.query = FakeQuery()

    def table(self, _name):
        return self.query


class FakeQuery:
    def __init__(self):
        self.filters = {}

    def select(self, _columns, **_kwargs):
        return self

    def eq(self, column, value):
        self.filters[column] = value
        return self

    def order(self, *_args, **_kwargs):
        return self

    def range(self, *_args, **_kwargs):
        return self

    def execute(self):
        return type("FakeResponse", (), {"data": [], "count": 0})()


if __name__ == "__main__":
    unittest.main()