from flask import Blueprint, request, jsonify

hostels_bp = Blueprint("hostels", __name__)


@hostels_bp.route("/api/search/hostels", methods=["GET"])
def search_hostels():
    """
    GET /api/search/hostels?city=Amsterdam&max_price=30

    Will call services/hostels.py once that's ready.
    """
    city = request.args.get("city")
    max_price = request.args.get("max_price", type=float)

    if not city:
        return jsonify({"error": "city is required"}), 400

    # ── TODO once services/hostels.py exists ─────────────────────────
    hostels = []  # placeholder

    return jsonify({"hostels": hostels})