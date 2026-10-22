-- ============================================================
-- MR Route Optimization — Schema Migration v2
-- Applies newly introduced fields for Mock & Phase 1-10 parity.
-- Execute in Supabase SQL Editor: https://supabase.com/dashboard/project/_/sql
-- ============================================================

-- 1. Doctors Enhancements (Prescription Volume, Status, Clinic Code)
ALTER TABLE doctors 
ADD COLUMN IF NOT EXISTS prescription_volume TEXT DEFAULT 'medium',
ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'active',
ADD COLUMN IF NOT EXISTS doc_code TEXT,
ADD COLUMN IF NOT EXISTS last_visit_date DATE;

-- Add check constraints safely if not already present
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'doctors_status_check'
    ) THEN
        ALTER TABLE doctors ADD CONSTRAINT doctors_status_check 
        CHECK (status IN ('active', 'on_leave', 'inactive'));
    END IF;
END $$;

-- 2. Medical Representatives Enhancements (Transit Vehicle, Working Hours & Heuristics)
ALTER TABLE medical_representatives 
ADD COLUMN IF NOT EXISTS vehicle_type TEXT DEFAULT 'two_wheeler',
ADD COLUMN IF NOT EXISTS start_location TEXT DEFAULT 'home',
ADD COLUMN IF NOT EXISTS lunch_start TEXT DEFAULT '13:30',
ADD COLUMN IF NOT EXISTS lunch_end TEXT DEFAULT '14:30',
ADD COLUMN IF NOT EXISTS target_visits_per_day INTEGER DEFAULT 8,
ADD COLUMN IF NOT EXISTS opt_strategy TEXT DEFAULT 'balanced',
ADD COLUMN IF NOT EXISTS preferences JSONB DEFAULT '{"auto_carryover": true, "traffic_reroute": true, "whatsapp_alerts": true}'::jsonb;

-- 3. Routes Table Enhancements (Fuel Estimates & Algorithm Tag)
ALTER TABLE routes
ADD COLUMN IF NOT EXISTS fuel_estimate_liters DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS total_distance_km DOUBLE PRECISION,
ADD COLUMN IF NOT EXISTS algorithm TEXT DEFAULT 'Google OR-Tools VRPTW + Random Forest ML Priority';

-- 4. Visits Table Outcome Enhancement
ALTER TABLE visits
ADD COLUMN IF NOT EXISTS field_notes TEXT;

-- Verify migration
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name IN ('doctors', 'medical_representatives', 'routes')
ORDER BY table_name, ordinal_position;
