import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_NAME = "database.db"

def get_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

init_db()

# ---------- HELLO ----------
@app.route("/api/hello", methods=["GET"])
def hello():
    return jsonify({"message": "Hello World"})

# ---------- CREATE ----------
@app.route("/api/items", methods=["POST"])
def create_item():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO items (name) VALUES (?)",
            (data["name"],)
        )
        item_id = cursor.lastrowid

    return jsonify({"id": item_id, "name": data["name"]}), 201

# ---------- READ ALL ----------
@app.route("/api/items", methods=["GET"])
def get_items():
    with get_db() as conn:
        cursor = conn.execute("SELECT id, name FROM items")
        items = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]

    return jsonify(items)

# ---------- READ ONE ----------
@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, name FROM items WHERE id = ?",
            (item_id,)
        )
        row = cursor.fetchone()

    if row is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"id": row[0], "name": row[1]})

# ---------- UPDATE ----------
@app.route("/api/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400

    with get_db() as conn:
        cursor = conn.execute(
            "UPDATE items SET name = ? WHERE id = ?",
            (data["name"], item_id)
        )

    if cursor.rowcount == 0:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"id": item_id, "name": data["name"]})

# ---------- DELETE ----------
@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    with get_db() as conn:
        cursor = conn.execute(
            "DELETE FROM items WHERE id = ?",
            (item_id,)
        )

    if cursor.rowcount == 0:
        return jsonify({"error": "Item not found"}), 404

    return jsonify({"message": "Item deleted"})
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
