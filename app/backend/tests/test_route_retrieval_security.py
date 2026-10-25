import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth.jwt_handler import create_access_token
from app.main import app


class RouteRetrievalSecurityTests(unittest.TestCase):
    @patch("app.routes.routes.get_supabase")
    def test_mr_cannot_retrieve_another_mrs_route(self, get_supabase):
        get_supabase.return_value = FakeSupabase(
            {"id": "route-2", "mr_id": "mr-2", "plan_date": "2026-10-25"}
        )
        token = create_access_token({"sub": "user-1", "role": "mr", "mr_id": "mr-1"})

        response = TestClient(app).get(
            "/api/routes/route-2",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 403)


class FakeSupabase:
    def __init__(self, route):
        self.route = route
        self.calls = 0

    def table(self, name):
        self.calls += 1
        return FakeQuery(self.route if name == "routes" else None)


class FakeQuery:
    def __init__(self, route):
        self.route = route

    def select(self, _columns):
        return self

    def eq(self, _column, _value):
        return self

    def order(self, _column, **_kwargs):
        return self

    def execute(self):
        data = [self.route] if self.route else []
        return type("FakeResponse", (), {"data": data})()


if __name__ == "__main__":
    unittest.main()