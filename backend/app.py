from flask import Flask, jsonify
from flask_cors import CORS

from routes.chat import chat_bp
from routes.search import search_bp
from routes.hostels import hostels_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(chat_bp)
app.register_blueprint(search_bp)
app.register_blueprint(hostels_bp)


@app.route("/")
def health_check():
    return jsonify({"status": "ok", "message": "Backend is running"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
