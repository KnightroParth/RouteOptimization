import unittest
from pathlib import Path


MIGRATION = (
    Path(__file__).resolve().parents[1] / "scripts" / "migration_v3.sql"
).read_text(encoding="utf-8")


class DatabaseContractTests(unittest.TestCase):
    def test_email_uniqueness_is_case_insensitive(self):
        self.assertIn("CREATE UNIQUE INDEX", MIGRATION)
        self.assertIn("lower(email)", MIGRATION)

    def test_relationships_have_duplicate_protection(self):
        self.assertIn("medical_representatives_user_id_key", MIGRATION)
        self.assertIn("visits_unique_assignment_key", MIGRATION)
        self.assertIn("route_stops_unique_sequence_key", MIGRATION)

    def test_business_fields_have_range_constraints(self):
        self.assertIn("doctors_coordinates_check", MIGRATION)
        self.assertIn("doctors_visit_duration_check", MIGRATION)

    def test_settings_fields_exist_for_persistence(self):
        self.assertIn("avg_visit_time", MIGRATION)


if __name__ == "__main__":
    unittest.main()