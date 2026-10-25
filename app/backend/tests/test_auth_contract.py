import unittest
from datetime import timedelta
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth.jwt_handler import create_access_token
from app.auth.jwt_handler import hash_password
from app.main import app


class AuthContractTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_me_requires_bearer_token(self):
        response = self.client.get("/api/auth/me")

        self.assertEqual(response.status_code, 401)

    def test_me_returns_authenticated_user_claims(self):
        token = create_access_token(
            {
                "sub": "user-123",
                "email": "mr@example.com",
                "role": "mr",
                "name": "Demo MR",
                "mr_id": "mr-123",
            },
            expires_delta=timedelta(minutes=5),
        )

        response = self.client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "user": {
                    "id": "user-123",
                    "email": "mr@example.com",
                    "role": "mr",
                    "name": "Demo MR",
                    "mr_id": "mr-123",
                }
            },
        )

    def test_me_rejects_malformed_token(self):
        response = self.client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer not-a-jwt"},
        )

        self.assertEqual(response.status_code, 401)

    def test_demo_token_is_not_a_valid_authentication_token(self):
        response = self.client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer demo-manager"},
        )

        self.assertEqual(response.status_code, 401)

    def test_me_rejects_expired_token(self):
        token = create_access_token(
            {"sub": "user-123", "role": "mr"},
            expires_delta=timedelta(minutes=-1),
        )

        response = self.client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 401)

    @patch("app.routes.auth.get_supabase")
    def test_login_returns_token_and_mr_id(self, get_supabase):
        get_supabase.return_value = FakeSupabase(
            {
                "users": [
                    {
                        "id": "user-123",
                        "email": "mr@example.com",
                        "password_hash": hash_password("correct-password"),
                        "name": "Demo MR",
                        "role": "mr",
                    }
                ],
                "medical_representatives": [
                    {"id": "mr-123", "user_id": "user-123"}
                ],
            }
        )

        response = self.client.post(
            "/api/auth/login",
            json={"email": "mr@example.com", "password": "correct-password"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["access_token"])
        self.assertEqual(response.json()["user"]["mr_id"], "mr-123")

    @patch("app.routes.auth.get_supabase")
    def test_login_rejects_invalid_password(self, get_supabase):
        get_supabase.return_value = FakeSupabase(
            {
                "users": [
                    {
                        "id": "user-123",
                        "email": "mr@example.com",
                        "password_hash": hash_password("correct-password"),
                        "name": "Demo MR",
                        "role": "mr",
                    }
                ]
            }
        )

        response = self.client.post(
            "/api/auth/login",
            json={"email": "mr@example.com", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)

    @patch("app.routes.auth.get_supabase")
    def test_register_mr_creates_user_and_profile(self, get_supabase):
        database = FakeSupabase({"users": [], "medical_representatives": []})
        get_supabase.return_value = database

        response = self.client.post(
            "/api/auth/register",
            json={
                "email": "new-mr@example.com",
                "password": "secure-password",
                "name": "New MR",
                "role": "mr",
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(database.tables["users"]), 1)
        self.assertEqual(len(database.tables["medical_representatives"]), 1)
        self.assertEqual(
            database.tables["medical_representatives"][0]["user_id"],
            database.tables["users"][0]["id"],
        )

    @patch("app.routes.auth.get_supabase")
    def test_register_rejects_duplicate_email(self, get_supabase):
        get_supabase.return_value = FakeSupabase(
            {"users": [{"id": "user-123", "email": "existing@example.com"}]}
        )

        response = self.client.post(
            "/api/auth/register",
            json={
                "email": "existing@example.com",
                "password": "secure-password",
                "name": "Duplicate",
                "role": "mr",
            },
        )

        self.assertEqual(response.status_code, 400)


class FakeSupabase:
    def __init__(self, tables):
        self.tables = tables

    def table(self, name):
        return FakeQuery(self.tables.get(name, []))


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows
        self.filters = {}

    def select(self, _columns):
        return self

    def eq(self, column, value):
        self.filters[column] = value
        return self

    def insert(self, row):
        row = dict(row)
        row.setdefault("id", f"generated-{len(self.rows) + 1}")
        self.rows.append(row)
        self.inserted = row
        return self

    def execute(self):
        data = [
            row for row in self.rows
            if all(row.get(column) == value for column, value in self.filters.items())
        ]
        return FakeResponse(data)


class FakeResponse:
    def __init__(self, data):
        self.data = data


if __name__ == "__main__":
    unittest.main()