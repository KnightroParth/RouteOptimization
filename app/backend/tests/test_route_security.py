import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth.jwt_handler import create_access_token
from app.main import app


class RouteSecurityTests(unittest.TestCase):
    @patch("app.routes.routes.get_supabase")
    def test_mr_cannot_generate_route_for_another_mr(self, get_supabase):
        token = create_access_token({"sub": "user-1", "role": "mr", "mr_id": "mr-1"})
        response = TestClient(app).post(
            "/api/routes/generate",
            headers={"Authorization": f"Bearer {token}"},
            json={"mr_id": "mr-2", "plan_date": "2026-10-25"},
        )

        self.assertEqual(response.status_code, 403)
        get_supabase.assert_not_called()


if __name__ == "__main__":
    unittest.main()