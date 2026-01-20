from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = '/data/crud.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('/data'):
        os.makedirs('/data')
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Create all items
@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return jsonify([dict(item) for item in items])

# Create a new item
@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    conn = get_db_connection()
    conn.execute('INSERT INTO items (title, description) VALUES (?, ?)',
                 (data['title'], data.get('description', '')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item created'}), 201

# Read a single item
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    conn.close()
    
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(dict(item))

# Update an item
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    conn = get_db_connection()
    
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if item is None:
        conn.close()
        return jsonify({'error': 'Item not found'}), 404
    
    title = data.get('title', item['title'])
    description = data.get('description', item['description'])
    completed = data.get('completed', item['completed'])
    
    conn.execute('UPDATE items SET title = ?, description = ?, completed = ? WHERE id = ?',
                 (title, description, completed, item_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item updated'})

# Delete an item
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    conn = get_db_connection()
    
    item = conn.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if item is None:
        conn.close()
        return jsonify({'error': 'Item not found'}), 404
    
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Item deleted'})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
