from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='db',
        database='crud_db',
        user='root',
        password='brey'
    )
    return connection

@app.route('/items', methods=['POST'])
def create_item():
    data = request.json
    name = data.get("name")
    precio = data.get("precio")

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "INSERT INTO item (name,precio) VALUES (%s , %s)"
    val = [
        ('peter', '15.5'),
        ('brey', '54.5'),
        ('ben', '45.02'),
        ('viola', '18.2')
    ]
    cursor.execute(query, val)
    connection.commit()

    print(cursor.rowcount, "record inserted  sucessfully"),201
    
@app.route('/items', methods=['GET'])
def get_items():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM item")
    items = cursor.fetchall()
    return jsonify(items), 200

@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM item WHERE id  = %s", (id,))
    item = cursor.fetchone()

    if item:
        return jsonify(item), 200
    else:
        return jsonify({'error': 'Item no encontrado'}), 404
    
@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.json
    name = data.get('name')
    precio = data.get('precio')

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("UPDATE item SET name = %s , precio = %s  WHERE id = %s", (name,precio,  id))
    connection.commit()

    if cursor.rowcount > 0:
        return jsonify({'id': id, 'name': name, 'precio':precio}), 200
    else:
        return jsonify({'error': 'item no actualizado '}), 404
    
@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM item WHERE id =%s", (id,))
    connection.commit()

    if cursor.rowcount > 0:
        return jsonify({'message': 'item eliminado'}), 200
    else:
        return jsonify({'error': 'Item no encontrado'}), 400
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    