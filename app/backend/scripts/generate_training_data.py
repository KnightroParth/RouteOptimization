"""
Synthetic Training Data Generator for MR Visit Priority Classification.

Generates realistic pharmaceutical MR visit records with 6 features and
3-class priority labels (high/medium/low) based on domain rules plus noise.

Usage: python -m scripts.generate_training_data
Output: app/backend/app/ml/training_data.csv
"""
import csv
import random
import os

random.seed(42)

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "app", "ml", "training_data.csv")

SPECIALTIES = [
    "Cardiology", "Orthopedics", "Pediatrics", "Neurology",
    "General Medicine", "Dermatology", "Oncology", "Diabetology",
    "Gastroenterology", "Pulmonology", "ENT", "Ophthalmology",
]

HIGH_VALUE_SPECIALTIES = {"Cardiology", "Oncology", "Neurology", "Orthopedics"}

TERRITORIES = [
    "Pune Central", "Pune East", "Pune North", "Pune West",
    "PCMC", "Pune South", "Nagpur Central", "Nashik East",
]


def generate_record() -> dict:
    """Generate a single synthetic MR visit record with realistic feature distributions."""
    specialty = random.choice(SPECIALTIES)
    territory = random.choice(TERRITORIES)

    # days_since_last_visit: weighted toward recent (1-14) with a fat tail up to 120
    if random.random() < 0.4:
        days_since = random.randint(1, 14)
    elif random.random() < 0.7:
        days_since = random.randint(15, 45)
    else:
        days_since = random.randint(46, 120)

    # visit_frequency: how many times visited in the last 90 days (0-12)
    visit_frequency = random.choices(
        population=list(range(0, 13)),
        weights=[5, 8, 12, 15, 14, 12, 10, 8, 6, 4, 3, 2, 1],
        k=1,
    )[0]

    # follow_up_required: 25% chance
    follow_up = random.random() < 0.25

    # prescription_volume: high/medium/low weighted
    rx_volume = random.choices(
        population=["high", "medium", "low"],
        weights=[25, 45, 30],
        k=1,
    )[0]

    # engagement_score: 0.0-1.0 continuous
    engagement = round(random.betavariate(2, 3), 3)

    # specialty_alignment: binary flag based on campaign drugs matching specialty
    spec_aligned = 1 if specialty in HIGH_VALUE_SPECIALTIES else 0

    # --- Compute ground truth priority based on domain rules + noise ---
    score = 0.0

    # Recency urgency (most important feature)
    if days_since > 60:
        score += 0.35
    elif days_since > 30:
        score += 0.20
    elif days_since > 14:
        score += 0.10

    # Prescription volume
    if rx_volume == "high":
        score += 0.25
    elif rx_volume == "medium":
        score += 0.12

    # Engagement history
    score += engagement * 0.15

    # Specialty alignment
    if spec_aligned:
        score += 0.10

    # Follow-up urgency
    if follow_up:
        score += 0.15

    # Visit frequency (inverse — low frequency = higher need)
    if visit_frequency <= 1:
        score += 0.10
    elif visit_frequency <= 3:
        score += 0.05

    # Add Gaussian noise (±0.08) to prevent perfect rules
    score += random.gauss(0, 0.08)
    score = max(0.0, min(1.0, score))

    # Classify
    if score >= 0.55:
        priority = "high"
    elif score >= 0.30:
        priority = "medium"
    else:
        priority = "low"

    return {
        "days_since_last_visit": days_since,
        "visit_frequency": visit_frequency,
        "follow_up_required": int(follow_up),
        "prescription_volume": rx_volume,
        "engagement_score": engagement,
        "specialty_alignment": spec_aligned,
        "priority_class": priority,
    }


def main():
    n_samples = 3000
    records = [generate_record() for _ in range(n_samples)]

    # Print class distribution
    from collections import Counter
    dist = Counter(r["priority_class"] for r in records)
    print(f"Generated {n_samples} synthetic training records")
    print(f"  Distribution: {dict(dist)}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    fieldnames = [
        "days_since_last_visit", "visit_frequency", "follow_up_required",
        "prescription_volume", "engagement_score", "specialty_alignment",
        "priority_class",
    ]
    with open(OUTPUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"  Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
