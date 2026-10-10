-- ============================================================
-- MR Route Optimization — Database Schema
-- Run this in Supabase SQL Editor (supabase.com/dashboard → SQL Editor)
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ── Users ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'mr' CHECK (role IN ('mr', 'manager', 'admin')),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Medical Representatives ───────────────────────────────────
CREATE TABLE IF NOT EXISTS medical_representatives (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    territory TEXT NOT NULL DEFAULT 'Pune',
    working_start TEXT DEFAULT '09:00',
    working_end TEXT DEFAULT '18:00',
    start_lat DOUBLE PRECISION DEFAULT 18.5204,
    start_lng DOUBLE PRECISION DEFAULT 73.8567,
    end_lat DOUBLE PRECISION,
    end_lng DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Doctors ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS doctors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    specialization TEXT,
    territory TEXT DEFAULT 'Pune',
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    availability_start TEXT DEFAULT '09:00',
    availability_end TEXT DEFAULT '17:00',
    typical_visit_duration INTEGER DEFAULT 30,
    priority_category TEXT CHECK (priority_category IN ('high', 'medium', 'low')),
    phone TEXT,
    address TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Visits ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS visits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doctor_id UUID REFERENCES doctors(id) ON DELETE CASCADE,
    mr_id UUID REFERENCES medical_representatives(id) ON DELETE CASCADE,
    visit_date DATE NOT NULL,
    planned_time TEXT,
    actual_arrival TEXT,
    actual_departure TEXT,
    status TEXT DEFAULT 'planned' CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled', 'missed')),
    outcome TEXT,
    follow_up_required BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Appointments ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doctor_id UUID REFERENCES doctors(id) ON DELETE CASCADE,
    mr_id UUID REFERENCES medical_representatives(id) ON DELETE CASCADE,
    appointment_date DATE NOT NULL,
    window_start TEXT,
    window_end TEXT,
    duration INTEGER DEFAULT 30,
    status TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'confirmed', 'cancelled', 'completed')),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Priority Predictions ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS priority_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    visit_id UUID REFERENCES visits(id) ON DELETE CASCADE,
    priority_class TEXT CHECK (priority_class IN ('high', 'medium', 'low')),
    priority_score DOUBLE PRECISION,
    model_version TEXT DEFAULT 'rule-based-v1',
    predicted_at TIMESTAMPTZ DEFAULT now()
);

-- ── Routes ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS routes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    mr_id UUID REFERENCES medical_representatives(id) ON DELETE CASCADE,
    plan_date DATE NOT NULL,
    solver_status TEXT CHECK (solver_status IN ('success', 'infeasible', 'timeout', 'error')),
    total_travel_time DOUBLE PRECISION,
    total_distance DOUBLE PRECISION,
    generated_at TIMESTAMPTZ DEFAULT now()
);

-- ── Route Stops ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS route_stops (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    route_id UUID REFERENCES routes(id) ON DELETE CASCADE,
    doctor_id UUID REFERENCES doctors(id),
    sequence_number INTEGER NOT NULL,
    estimated_arrival TEXT,
    estimated_departure TEXT,
    travel_time DOUBLE PRECISION,
    service_duration INTEGER DEFAULT 30,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- ── Indexes ───────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_visits_mr_date ON visits(mr_id, visit_date);
CREATE INDEX IF NOT EXISTS idx_visits_doctor ON visits(doctor_id);
CREATE INDEX IF NOT EXISTS idx_routes_mr_date ON routes(mr_id, plan_date);
CREATE INDEX IF NOT EXISTS idx_predictions_visit ON priority_predictions(visit_id);
CREATE INDEX IF NOT EXISTS idx_route_stops_route ON route_stops(route_id);
CREATE INDEX IF NOT EXISTS idx_doctors_territory ON doctors(territory);

-- ── Disable RLS for prototype (re-enable for production) ─────
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE medical_representatives ENABLE ROW LEVEL SECURITY;
ALTER TABLE doctors ENABLE ROW LEVEL SECURITY;
ALTER TABLE visits ENABLE ROW LEVEL SECURITY;
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE priority_predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE routes ENABLE ROW LEVEL SECURITY;
ALTER TABLE route_stops ENABLE ROW LEVEL SECURITY;

-- Allow service_role full access (backend uses service key)
CREATE POLICY "service_role_all" ON users FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON medical_representatives FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON doctors FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON visits FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON appointments FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON priority_predictions FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON routes FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON route_stops FOR ALL USING (true) WITH CHECK (true);
