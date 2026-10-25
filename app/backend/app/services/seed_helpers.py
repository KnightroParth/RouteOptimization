"""Pure helpers used to make demo data seeding repeatable."""


def visit_identity(visit: dict) -> tuple:
    return visit["doctor_id"], visit["mr_id"], visit["visit_date"]


def filter_new_visits(existing: list[dict], candidates: list[dict]) -> list[dict]:
    known = {visit_identity(visit) for visit in existing}
    new_visits = []

    for candidate in candidates:
        identity = visit_identity(candidate)
        if identity in known:
            continue
        known.add(identity)
        new_visits.append(candidate)

    return new_visits