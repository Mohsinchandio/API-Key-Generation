"""Task 2 - Text-processing API protected by API keys (X-API-Key header).
Run:  python generate_keys.py   (once)
      python app.py             ->  http://127.0.0.1:5001
"""
import hashlib
import hmac
import json
import os
from functools import wraps

from flask import Flask, g, jsonify, request

app = Flask(__name__)
KEYS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api_keys.json")


def load_key_hashes():
    if not os.path.exists(KEYS_FILE):
        raise SystemExit("api_keys.json not found. Run: python generate_keys.py")
    with open(KEYS_FILE) as f:
        return json.load(f)           # {sha256_hash: consumer_name}


KEY_HASHES = load_key_hashes()


def require_api_key(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        supplied = request.headers.get("X-API-Key")
        if not supplied:
            return jsonify({"error": "Missing API key. Send it in the X-API-Key header."}), 401

        supplied_hash = hashlib.sha256(supplied.encode()).hexdigest()
        for stored_hash, consumer in KEY_HASHES.items():
            if hmac.compare_digest(supplied_hash, stored_hash):   # constant-time compare
                g.consumer = consumer
                return view(*args, **kwargs)
        return jsonify({"error": "Invalid API key."}), 401
    return wrapper


@app.post("/process")
@require_api_key
def process():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not isinstance(data.get("text"), str):
        return jsonify({"error": "JSON body with a string field 'text' is required"}), 400
    text = data["text"]
    return jsonify({
        "consumer": g.consumer,
        "original": text,
        "processed": text.upper(),
        "length": len(text),
        "word_count": len(text.split()),
    }), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)
