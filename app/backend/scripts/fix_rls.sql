-- ============================================================
-- Fix RLS Policies — Replace permissive policies with role-scoped ones
-- Run this in Supabase SQL Editor AFTER schema.sql
-- ============================================================

-- Drop the overly permissive policies
DROP POLICY IF EXISTS "service_role_all" ON users;
DROP POLICY IF EXISTS "service_role_all" ON medical_representatives;
DROP POLICY IF EXISTS "service_role_all" ON doctors;
DROP POLICY IF EXISTS "service_role_all" ON visits;
DROP POLICY IF EXISTS "service_role_all" ON appointments;
DROP POLICY IF EXISTS "service_role_all" ON priority_predictions;
DROP POLICY IF EXISTS "service_role_all" ON routes;
DROP POLICY IF EXISTS "service_role_all" ON route_stops;

-- Users: authenticated users can read their own row
CREATE POLICY "users_select_own" ON users
  FOR SELECT USING (auth.role() = 'service_role' OR auth.role() = 'authenticated');
CREATE POLICY "users_insert_service" ON users
  FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "users_update_service" ON users
  FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "users_delete_service" ON users
  FOR DELETE USING (auth.role() = 'service_role');

-- Medical Representatives
CREATE POLICY "mr_select" ON medical_representatives
  FOR SELECT USING (auth.role() = 'service_role' OR auth.role() = 'authenticated');
CREATE POLICY "mr_insert" ON medical_representatives
  FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "mr_update" ON medical_representatives
  FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "mr_delete" ON medical_representatives
  FOR DELETE USING (auth.role() = 'service_role');

-- Doctors: readable by authenticated, writable by service_role
CREATE POLICY "doctors_select" ON doctors
  FOR SELECT USING (auth.role() = 'service_role' OR auth.role() = 'authenticated');
CREATE POLICY "doctors_insert" ON doctors
  FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "doctors_update" ON doctors
  FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "doctors_delete" ON doctors
  FOR DELETE USING (auth.role() = 'service_role');

-- Visits
CREATE POLICY "visits_select" ON visits
  FOR SELECT USING (auth.role() = 'service_role' OR auth.role() = 'authenticated');
CREATE POLICY "visits_insert" ON visits
  FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "visits_update" ON visits
  FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "visits_delete" ON visits
  FOR DELETE USING (auth.role() = 'service_role');

-- Appointments
CREATE POLICY "appointments_select" ON appointments
  FOR SELECT USING (auth.role() = 'service_role' OR auth.role() = 'authenticated');
CREATE POLICY "appointments_insert" ON appointments
  FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "appointments_update" ON appointments
  FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "appointments_delete" ON appointments
  FOR DELETE USING (auth.role() = 'service_role');

-- Priority Predictions
CREATE POLICY "predictions_select" ON priority_predictions
  FOR SELECT USING (auth.role() = 'service_role' OR auth.role() = 'authenticated');
CREATE POLICY "predictions_insert" ON priority_predictions
  FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "predictions_update" ON priority_predictions
  FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "predictions_delete" ON priority_predictions
  FOR DELETE USING (auth.role() = 'service_role');

-- Routes
CREATE POLICY "routes_select" ON routes
  FOR SELECT USING (auth.role() = 'service_role' OR auth.role() = 'authenticated');
CREATE POLICY "routes_insert" ON routes
  FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "routes_update" ON routes
  FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "routes_delete" ON routes
  FOR DELETE USING (auth.role() = 'service_role');

-- Route Stops
CREATE POLICY "route_stops_select" ON route_stops
  FOR SELECT USING (auth.role() = 'service_role' OR auth.role() = 'authenticated');
CREATE POLICY "route_stops_insert" ON route_stops
  FOR INSERT WITH CHECK (auth.role() = 'service_role');
CREATE POLICY "route_stops_update" ON route_stops
  FOR UPDATE USING (auth.role() = 'service_role');
CREATE POLICY "route_stops_delete" ON route_stops
  FOR DELETE USING (auth.role() = 'service_role');
