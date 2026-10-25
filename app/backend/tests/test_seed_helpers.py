import unittest

from app.services.seed_helpers import filter_new_visits, visit_identity


class SeedHelperTests(unittest.TestCase):
    def test_visit_identity_is_stable(self):
        visit = {"doctor_id": "doctor-1", "mr_id": "mr-1", "visit_date": "2026-10-25"}

        self.assertEqual(visit_identity(visit), ("doctor-1", "mr-1", "2026-10-25"))

    def test_filter_new_visits_removes_existing_and_duplicate_candidates(self):
        existing = [
            {"doctor_id": "doctor-1", "mr_id": "mr-1", "visit_date": "2026-10-25"}
        ]
        candidates = [
            {"doctor_id": "doctor-1", "mr_id": "mr-1", "visit_date": "2026-10-25"},
            {"doctor_id": "doctor-2", "mr_id": "mr-1", "visit_date": "2026-10-25"},
            {"doctor_id": "doctor-2", "mr_id": "mr-1", "visit_date": "2026-10-25"},
        ]

        self.assertEqual(filter_new_visits(existing, candidates), [candidates[1]])


if __name__ == "__main__":
    unittest.main()