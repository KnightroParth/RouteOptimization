"""
Seed script — populates the database with demo data for the prototype.
Pune-area doctors with real coordinates, demo MR, and sample visits.

Usage: python -m scripts.seed_data
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from app.db import get_supabase
from app.auth.jwt_handler import hash_password
from datetime import date, timedelta

sb = get_supabase()

# ── Demo Users ─────────────────────────────────────────────────
print("Seeding users...")
demo_users = [
    {
        "email": "mr@demo.com",
        "password_hash": hash_password("demo123"),
        "name": "Parth Lokhande",
        "role": "mr",
    },
    {
        "email": "mr2@demo.com",
        "password_hash": hash_password("demo123"),
        "name": "Bhakti Gundecha",
        "role": "mr",
    },
    {
        "email": "mr3@demo.com",
        "password_hash": hash_password("demo123"),
        "name": "Udaykiran Bitla",
        "role": "mr",
    },
    {
        "email": "manager@demo.com",
        "password_hash": hash_password("demo123"),
        "name": "Rajesh Mehta",
        "role": "manager",
    },
]

user_ids = {}
for u in demo_users:
    existing = sb.table("users").select("id").eq("email", u["email"]).execute()
    if existing.data:
        user_ids[u["email"]] = existing.data[0]["id"]
        print(f"  User {u['email']} already exists")
    else:
        result = sb.table("users").insert(u).execute()
        user_ids[u["email"]] = result.data[0]["id"]
        print(f"  Created user {u['email']}")

# ── MR Profiles ────────────────────────────────────────────────
print("Seeding MR profiles...")
mr_profiles = [
    {
        "user_id": user_ids["mr@demo.com"],
        "territory": "Pune Central",
        "working_start": "09:00",
        "working_end": "18:00",
        "start_lat": 18.5204,    # Pune center
        "start_lng": 73.8567,
        "end_lat": 18.5204,
        "end_lng": 73.8567,
    },
    {
        "user_id": user_ids["mr2@demo.com"],
        "territory": "Pune West",
        "working_start": "09:00",
        "working_end": "18:00",
        "start_lat": 18.5074,
        "start_lng": 73.8077,
        "end_lat": 18.5074,
        "end_lng": 73.8077,
    },
    {
        "user_id": user_ids["mr3@demo.com"],
        "territory": "Pune East",
        "working_start": "09:00",
        "working_end": "18:00",
        "start_lat": 18.5362,
        "start_lng": 73.8970,
        "end_lat": 18.5362,
        "end_lng": 73.8970,
    },
]

mr_ids = {}
for i, mp in enumerate(mr_profiles):
    existing = (
        sb.table("medical_representatives")
        .select("id")
        .eq("user_id", mp["user_id"])
        .execute()
    )
    if existing.data:
        mr_ids[i] = existing.data[0]["id"]
        print(f"  MR profile already exists for user {mp['user_id']}")
    else:
        result = sb.table("medical_representatives").insert(mp).execute()
        mr_ids[i] = result.data[0]["id"]
        print(f"  Created MR profile: {mp['territory']}")

# ── Doctors (Pune area with realistic coordinates) ─────────────
print("Seeding doctors...")
doctors = [
    {
        "name": "Dr. Anita Sharma",
        "specialization": "Cardiologist",
        "territory": "Pune Central",
        "latitude": 18.5314,
        "longitude": 73.8446,
        "availability_start": "09:00",
        "availability_end": "13:00",
        "typical_visit_duration": 30,
        "priority_category": "high",
        "address": "Shivajinagar, Pune",
    },
    {
        "name": "Dr. Rajesh Patil",
        "specialization": "General Physician",
        "territory": "Pune Central",
        "latitude": 18.5196,
        "longitude": 73.8553,
        "availability_start": "10:00",
        "availability_end": "16:00",
        "typical_visit_duration": 20,
        "priority_category": "medium",
        "address": "Sadashiv Peth, Pune",
    },
    {
        "name": "Dr. Priya Deshmukh",
        "specialization": "Dermatologist",
        "territory": "Pune Central",
        "latitude": 18.5089,
        "longitude": 73.8259,
        "availability_start": "11:00",
        "availability_end": "17:00",
        "typical_visit_duration": 25,
        "priority_category": "low",
        "address": "Parvati, Pune",
    },
    {
        "name": "Dr. Vikram Joshi",
        "specialization": "Orthopedic",
        "territory": "Pune Central",
        "latitude": 18.5362,
        "longitude": 73.8970,
        "availability_start": "09:30",
        "availability_end": "14:00",
        "typical_visit_duration": 35,
        "priority_category": "high",
        "address": "Koregaon Park, Pune",
    },
    {
        "name": "Dr. Sneha Kulkarni",
        "specialization": "Pediatrician",
        "territory": "Pune Central",
        "latitude": 18.5618,
        "longitude": 73.9169,
        "availability_start": "10:00",
        "availability_end": "15:00",
        "typical_visit_duration": 25,
        "priority_category": "medium",
        "address": "Viman Nagar, Pune",
    },
    {
        "name": "Dr. Anil Mehta",
        "specialization": "Neurologist",
        "territory": "Pune Central",
        "latitude": 18.4988,
        "longitude": 73.8678,
        "availability_start": "13:00",
        "availability_end": "18:00",
        "typical_visit_duration": 30,
        "priority_category": "high",
        "address": "Swargate, Pune",
    },
    {
        "name": "Dr. Kavita Rao",
        "specialization": "Gynecologist",
        "territory": "Pune West",
        "latitude": 18.5074,
        "longitude": 73.8077,
        "availability_start": "09:00",
        "availability_end": "14:00",
        "typical_visit_duration": 30,
        "priority_category": "medium",
        "address": "Kothrud, Pune",
    },
    {
        "name": "Dr. Mahesh Deshpande",
        "specialization": "ENT Specialist",
        "territory": "Pune Central",
        "latitude": 18.5485,
        "longitude": 73.8919,
        "availability_start": "10:00",
        "availability_end": "16:30",
        "typical_visit_duration": 20,
        "priority_category": "low",
        "address": "Kalyani Nagar, Pune",
    },
    {
        "name": "Dr. Suman Bhatt",
        "specialization": "Oncologist",
        "territory": "Pune Central",
        "latitude": 18.4625,
        "longitude": 73.8680,
        "availability_start": "09:00",
        "availability_end": "12:00",
        "typical_visit_duration": 40,
        "priority_category": "high",
        "address": "Bibwewadi, Pune",
    },
    {
        "name": "Dr. Ramesh Wagh",
        "specialization": "General Physician",
        "territory": "Pune East",
        "latitude": 18.5679,
        "longitude": 73.9143,
        "availability_start": "14:00",
        "availability_end": "18:00",
        "typical_visit_duration": 20,
        "priority_category": "medium",
        "address": "Kharadi, Pune",
    },
    {
        "name": "Dr. Pooja Naik",
        "specialization": "Cardiologist",
        "territory": "Pune West",
        "latitude": 18.5136,
        "longitude": 73.7869,
        "availability_start": "09:00",
        "availability_end": "13:30",
        "typical_visit_duration": 30,
        "priority_category": "high",
        "address": "Warje, Pune",
    },
    {
        "name": "Dr. Suresh Gaikwad",
        "specialization": "Psychiatrist",
        "territory": "Pune Central",
        "latitude": 18.5242,
        "longitude": 73.8478,
        "availability_start": "11:00",
        "availability_end": "17:00",
        "typical_visit_duration": 30,
        "priority_category": "low",
        "address": "Deccan Gymkhana, Pune",
    },
]

doctor_ids = []
for d in doctors:
    existing = sb.table("doctors").select("id").eq("name", d["name"]).execute()
    if existing.data:
        doctor_ids.append(existing.data[0]["id"])
        print(f"  Doctor {d['name']} already exists")
    else:
        result = sb.table("doctors").insert(d).execute()
        doctor_ids.append(result.data[0]["id"])
        print(f"  Created doctor: {d['name']} ({d['specialization']})")

# ── Sample Visits (today and tomorrow) ─────────────────────────
print("Seeding visits...")
today = date.today().isoformat()
tomorrow = (date.today() + timedelta(days=1)).isoformat()

visit_data = []
# MR 1 (Parth) — 6 visits today
for i, did in enumerate(doctor_ids[:6]):
    visit_data.append({
        "doctor_id": did,
        "mr_id": mr_ids[0],
        "visit_date": today,
        "status": "planned",
        "follow_up_required": i % 2 == 0,
    })

# MR 1 — 4 visits tomorrow
for i, did in enumerate(doctor_ids[2:6]):
    visit_data.append({
        "doctor_id": did,
        "mr_id": mr_ids[0],
        "visit_date": tomorrow,
        "status": "planned",
        "follow_up_required": i == 0,
    })

# MR 2 (Bhakti) — 4 visits today
for i, did in enumerate(doctor_ids[6:10]):
    visit_data.append({
        "doctor_id": did,
        "mr_id": mr_ids[1],
        "visit_date": today,
        "status": "completed" if i < 2 else "planned",
        "follow_up_required": i == 0,
    })

# MR 3 (Udaykiran) — 3 visits today
for i, did in enumerate(doctor_ids[9:12]):
    visit_data.append({
        "doctor_id": did,
        "mr_id": mr_ids[2],
        "visit_date": today,
        "status": "planned",
        "follow_up_required": i == 1,
    })

for v in visit_data:
    try:
        sb.table("visits").insert(v).execute()
    except Exception as e:
        print(f"  Visit insert error (may be duplicate): {e}")
        continue

print(f"  Created {len(visit_data)} visits")

print("\n[OK] Seed data complete!")
print("Demo credentials:")
print("  MR:      mr@demo.com / demo123")
print("  Manager: manager@demo.com / demo123")
