from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
TOR_PROXY = os.getenv("TOR_PROXY", "socks5h://127.0.0.1:9050")
proxies = {"http": TOR_PROXY, "https": TOR_PROXY}

RANDOMUSER_API = "https://randomuser.me/api/?results=5"

@app.route("/users")
def get_users():
    try:
        response = requests.get(RANDOMUSER_API, proxies=proxies, timeout=10)
        response.raise_for_status()
        data = response.json()
        users = []
        for u in data.get("results", []):
            users.append({
                "name": f"{u['name']['first']} {u['name']['last']}",
                "photo": u['picture']['medium']
            })
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
