from flask import Blueprint, request, jsonify
from services.hostels import search_hostels

hostels_bp = Blueprint("hostels", __name__)


@hostels_bp.route("/api/search/hostels", methods=["GET"])
def search_hostels_route():
    """
    GET /api/search/hostels?city=Amsterdam&max_price=30
    """
    city = request.args.get("city")
    max_price = request.args.get("max_price", type=float)

    if not city:
        return jsonify({"error": "city is required"}), 400

    hostels = search_hostels(city, max_price=max_price)

    return jsonify({"hostels": hostels})