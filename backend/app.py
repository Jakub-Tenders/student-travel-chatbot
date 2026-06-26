from flask import Flask, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from routes.chat import chat_bp
from routes.search import search_bp
from routes.hostels import hostels_bp

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=[])
CORS(app, origins=["http://localhost:5500", "http://127.0.0.1:5500"])
app.register_blueprint(chat_bp)
limiter.limit("20 per minute")(app.view_functions["chat.chat"])
app.register_blueprint(search_bp)
app.register_blueprint(hostels_bp)


@app.route("/")
def health_check():
    return jsonify({"status": "ok", "message": "Backend is running"})


if __name__ == "__main__":
    app.run(debug=False, port=5001)
