-- MR Route Optimization - Database integrity migration v3
-- Safe to run repeatedly in Supabase SQL Editor.

-- Identity and relationship uniqueness.
ALTER TABLE medical_representatives
    ADD COLUMN IF NOT EXISTS avg_visit_time INTEGER DEFAULT 15;

CREATE UNIQUE INDEX IF NOT EXISTS users_email_lower_key
    ON users (lower(email));

CREATE UNIQUE INDEX IF NOT EXISTS medical_representatives_user_id_key
    ON medical_representatives (user_id);

CREATE UNIQUE INDEX IF NOT EXISTS visits_unique_assignment_key
    ON visits (doctor_id, mr_id, visit_date);

CREATE UNIQUE INDEX IF NOT EXISTS route_stops_unique_sequence_key
    ON route_stops (route_id, sequence_number);

-- Coordinates and service durations must be usable by the optimizer.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'doctors_coordinates_check'
    ) THEN
        ALTER TABLE doctors ADD CONSTRAINT doctors_coordinates_check
        CHECK (
            latitude BETWEEN -90 AND 90
            AND longitude BETWEEN -180 AND 180
        );
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'doctors_visit_duration_check'
    ) THEN
        ALTER TABLE doctors ADD CONSTRAINT doctors_visit_duration_check
        CHECK (typical_visit_duration BETWEEN 1 AND 240);
    END IF;
END $$;

-- Common dashboard and route query paths.
CREATE INDEX IF NOT EXISTS idx_visits_status_date
    ON visits (status, visit_date);

CREATE INDEX IF NOT EXISTS idx_doctors_specialization
    ON doctors (specialization);
