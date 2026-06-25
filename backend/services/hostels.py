"""
Hostel search service

NOTE: Free hostel-specific APIs (Hostelworld, Hostelz) don't offer
self-serve public access. A general hotel API (Makcorps) exists but
requires a separate JWT auth flow and returns full hotels rather than
budget hostels specifically — filtering it down reliably would need more
time than we have before the deadline.

Like blablacar.py, this ships with realistic mock data by default.
"""

import os
import random

USE_MOCK = os.environ.get("HOSTEL_API_KEY") is None

# Mock hostel "database" — a handful of realistic European cities
HOSTEL_NAMES = [
    "The Flying Pig", "Generator", "Wombat's City Hostel", "St Christopher's Inn",
    "Hostel One", "Yellow Hostel", "Meininger", "U Hostel", "Clink Hostel",
    "Mad Monkey", "Safestay", "Pura Vida Sky Hostel",
]

AMENITIES_POOL = [
    "Free WiFi", "Breakfast included", "24h reception", "Lockers",
    "Bar on site", "Kitchen access", "Laundry", "Air conditioning",
    "Female-only dorms available", "Walking distance to center",
]


def search_hostels(city: str, max_price: float = None, max_results: int = 6) -> list[dict]:
    """
    Search for budget hostels in a city.

    Args:
        city:        City name, e.g. "Amsterdam"
        max_price:   Optional max price per night in EUR
        max_results: How many hostels to return

    Returns:
        List of hostel dicts, sorted by price.
    """
    
    hostels = _mock_hostels(city, max_results)

    if max_price:
        hostels = [h for h in hostels if h["price_per_night_eur"] <= max_price]

    return sorted(hostels, key=lambda x: x["price_per_night_eur"])


def _mock_hostels(city: str, max_results: int) -> list[dict]:
    """Realistic mock hostel data, consistent per city via seeding."""
    random.seed(city.lower())

    hostels = []
    used_names = random.sample(HOSTEL_NAMES, min(max_results, len(HOSTEL_NAMES)))

    for name in used_names:
        price = round(random.uniform(15, 38), 2)
        rating = round(random.uniform(7.5, 9.6), 1)
        amenities = random.sample(AMENITIES_POOL, k=4)

        hostels.append({
            "name": f"{name} {city}",
            "city": city,
            "price_per_night_eur": price,
            "rating": rating,    
            "reviews_count": random.randint(80, 3200),
            "amenities": amenities,
        })

    return hostels
