import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.auth.jwt_handler import create_access_token
from app.main import app


class MlBatchContractTests(unittest.TestCase):
    def setUp(self):
        token = create_access_token({"sub": "user-1", "role": "manager"})
        self.client = TestClient(app)
        self.headers = {"Authorization": f"Bearer {token}"}

    @patch("app.routes.ml.predict_batch")
    @patch("app.routes.ml.get_supabase")
    def test_batch_scores_database_visits_and_persists_predictions(
        self, get_supabase, predict_batch
    ):
        database = FakeSupabase(
            [
                {"id": "visit-1", "doctor_id": "doctor-1", "follow_up_required": True},
                {"id": "visit-2", "doctor_id": "doctor-2", "follow_up_required": False},
            ]
        )
        get_supabase.return_value = database
        predict_batch.return_value = [
            {"priority_class": "high", "priority_score": 0.9, "model_version": "rule-based-v1"},
            {"priority_class": "medium", "priority_score": 0.5, "model_version": "rule-based-v1"},
        ]

        response = self.client.post("/api/ml/run-batch", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["counts"], {"high": 1, "medium": 1, "low": 0, "total": 2})
        self.assertEqual(len(database.predictions), 2)

    @patch("app.routes.ml.get_supabase")
    def test_batch_reports_empty_database_without_fake_counts(self, get_supabase):
        database = FakeSupabase([])
        get_supabase.return_value = database

        response = self.client.post("/api/ml/run-batch", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["counts"], {"high": 0, "medium": 0, "low": 0, "total": 0})
        self.assertEqual(database.predictions, [])


class FakeSupabase:
    def __init__(self, visits):
        self.visits = visits
        self.predictions = []

    def table(self, name):
        if name == "visits":
            return FakeQuery(self.visits)
        return FakeQuery(self.predictions)


class FakeQuery:
    def __init__(self, rows):
        self.rows = rows
        self.inserted = None

    def select(self, _columns):
        return self

    def insert(self, row):
        self.rows.append(row)
        self.inserted = row
        return self

    def execute(self):
        return type("FakeResponse", (), {"data": self.rows})()


if __name__ == "__main__":
    unittest.main()