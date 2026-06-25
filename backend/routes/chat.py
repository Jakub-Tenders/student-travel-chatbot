from flask import Blueprint, request, jsonify
from services.llm import get_ai_response
from services.sky_scrapper import search_one_way
from utils.prompt_builder import build_travel_context

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    """
    POST /api/chat
    Body: { "message": "...", "history": [...] }
    """
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"]
    history = data.get("history", [])

    origin = data.get("origin")
    destination = data.get("destination")
    date = data.get("date")

    flights = search_one_way(origin, destination, date) if all([origin, destination, date]) else []
    context = build_travel_context(flights=flights)

    reply = get_ai_response(user_message, history, context)

    return jsonify({"reply": reply, "flights": flights})