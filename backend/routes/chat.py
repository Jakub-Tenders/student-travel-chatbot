from flask import Blueprint, request, jsonify
from services.llm import get_ai_response

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

    reply = get_ai_response(user_message, history)

    return jsonify({
        "reply": reply,
        "flights": []  # will be filled once Amadeus is wired up
    })