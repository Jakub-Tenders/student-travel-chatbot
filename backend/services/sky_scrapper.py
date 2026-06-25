import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://flights-sky.p.rapidapi.com/flights"
HEADERS = {
    "X-RapidAPI-Key": os.environ.get("RAPIDAPI_KEY"),
    "X-RapidAPI-Host": "flights-sky.p.rapidapi.com",
}


def _resolve_city(city_name):
    """
    Use flights/auto-complete to turn a city name into (skyId, entityId).
    Returns the first result's skyId and entityId, or (None, None) on failure.
    """
    print(f"[debug key] {os.environ.get('RAPIDAPI_KEY')}")
    response = requests.get(
        f"{BASE_URL}/auto-complete",
        headers=HEADERS,
        params={"query": city_name},
    )
    response.raise_for_status()
    print(f"[autocomplete raw] {response.json()}")
    results = response.json().get("data", [])
    if not results:
        return None, None
    airports = [r for r in results if r.get("navigation", {}).get("entityType") == "AIRPORT"]
    first = airports[0] if airports else results[0]
    return first.get("presentation", {}).get("skyId"), first.get("presentation", {}).get("id")


def _parse_itineraries(data):
    """
    Extract a flat list of flight offers from the response data block.
    Adjust field names here if the API response differs.
    """
    flights = []
    for item in data.get("itineraries", []):
        legs = item.get("legs", [])
        if not legs:
            continue
        leg = legs[0]
        price_info = item.get("price", {})
        flights.append({
            "price": price_info.get("raw"),
            "currency": price_info.get("currency", "EUR"),
            "duration": leg.get("durationInMinutes"),
            "stops": leg.get("stopCount"),
            "departure": leg.get("departure"),
            "arrival": leg.get("arrival"),
            "carrier": leg.get("carriers", {}).get("marketing", [{}])[0].get("name"),
        })
    return flights


def search_one_way(origin_city, destination_city, depart_date, adults=1, currency="EUR", cabin_class="economy", stops=None):
    """
    Search one-way flights between two city names.
    Handles the incomplete-status polling loop automatically.
    Returns a list of flight dicts sorted cheapest first.
    """
    try:
        origin_sky_id, origin_entity_id = _resolve_city(origin_city)
        dest_sky_id, dest_entity_id = _resolve_city(destination_city)

        if not all([origin_entity_id, dest_entity_id]):
            print(f"[sky_scrapper] Could not resolve cities: {origin_city}, {destination_city}")
            return []

        params = {
            "fromEntityId": origin_entity_id,
            "toEntityId": dest_entity_id,
            "departDate": depart_date,
            "adults": adults,
            "currency": currency,
            "cabinClass": cabin_class,
        }
        if stops is not None:
            params["stops"] = stops

        response = requests.get(f"{BASE_URL}/search-one-way", headers=HEADERS, params=params)
        response.raise_for_status()
        body = response.json()
        print(f"[search-one-way raw] {body}")

        context = body.get("data", {}).get("context", {})
        all_itineraries = body.get("data", {})
        session_id = context.get("sessionId")

        max_polls = 5
        polls = 0
        while context.get("status") == "incomplete" and session_id and polls < max_polls:
            time.sleep(1)
            poll_response = requests.get(
                f"{BASE_URL}/search-incomplete",
                headers=HEADERS,
                params={"sessionId": session_id},
            )
            poll_response.raise_for_status()
            poll_body = poll_response.json()
            context = poll_body.get("data", {}).get("context", {})
            # Merge new itineraries into our running set
            new_items = poll_body.get("data", {}).get("itineraries", [])
            all_itineraries.setdefault("itineraries", []).extend(new_items)
            polls += 1

        flights = _parse_itineraries(all_itineraries)
        flights.sort(key=lambda f: f["price"] or float("inf"))
        return flights

    except Exception as e:
        print(f"[sky_scrapper] Error: {e}")
        return []