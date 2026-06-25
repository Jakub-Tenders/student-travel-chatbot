"""
BlaBlaCar carpooling service

NOTE: BlaBlaCar's official API (Daily rideshare + Bus) requires partner
approval and is not self-serve like Groq/Amadeus. We requested access but
can't guarantee approval before the deadline, so this service ships with
realistic mock data by default.

The function signatures and return shape are designed so that if real
API access is granted, only _fetch_real_rides() needs to change —
nothing in routes/ or the frontend would need to change.

This is a deliberate architecture decision worth mentioning in
B-conception.docx and C-privacy.docx (no real user data sent to a
third party while in mock mode).
"""

import random


def search_rides(origin: str, destination: str, date: str, max_results: int = 5) -> list[dict]:
    """
    Search for carpooling rides between two cities.

    Args:
        origin:      City name, e.g. "Paris"
        destination: City name, e.g. "Lyon"
        date:        "YYYY-MM-DD"
        max_results: How many rides to return

    Returns:
        List of ride dicts, sorted by price.
    """
    return _mock_rides(origin, destination, date, max_results)


def _mock_rides(origin: str, destination: str, date: str, max_results: int) -> list[dict]:
    """
    Realistic mock carpooling data.
    Prices and times are randomized within realistic ranges.
    """
    random.seed(f"{origin}{destination}{date}")  # consistent results per route

    drivers = ["Sophie", "Lucas", "Emma", "Thomas", "Chloé", "Hugo", "Léa", "Nathan"]
    cars = ["Renault Clio", "Peugeot 208", "Citroën C3", "VW Golf", "Toyota Yaris"]

    rides = []
    for i in range(max_results):
        hour = 6 + i * 3
        price = round(random.uniform(8, 35), 2)
        seats = random.randint(1, 4)

        rides.append({
            "driver_name": random.choice(drivers),
            "car_model": random.choice(cars),
            "price_eur": price,
            "origin": origin,
            "destination": destination,
            "departure_time": f"{date}T{hour:02d}:00:00",
            "seats_available": seats,
            "rating": round(random.uniform(4.2, 5.0), 1),
        })

    return sorted(rides, key=lambda x: x["price_eur"])
