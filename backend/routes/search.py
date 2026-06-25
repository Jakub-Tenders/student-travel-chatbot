from flask import Blueprint, request, jsonify
from services.blablacar import search_rides

search_bp = Blueprint("search", __name__)


@search_bp.route("/api/search/flights", methods=["GET"])
def search_flights():
    """
    GET /api/search/flights?origin=CDG&destination=BCN&date=2025-07-15

    Will call services/amadeus.py once that's ready.
    """
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    date = request.args.get("date")

    if not all([origin, destination, date]):
        return jsonify({"error": "origin, destination and date are required"}), 400

    # ── TODO once amadeus.py exists: ─────────────────────────────────
    # from backend.services.amadeus import search_cheap_flights
    # flights = search_cheap_flights(origin, destination, date)

    flights = []  # placeholder

    return jsonify({"flights": flights})


@search_bp.route("/api/search/rides", methods=["GET"])
def search_rides_route():
    """
    GET /api/search/rides?origin=Paris&destination=Lyon&date=2026-09-15
    """
    origin = request.args.get("origin")
    destination = request.args.get("destination")
    date = request.args.get("date")

    if not all([origin, destination, date]):
        return jsonify({"error": "origin, destination and date are required"}), 400

    rides = search_rides(origin, destination, date)
    return jsonify({"rides": rides})
