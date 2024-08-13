from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error
import json

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='db',
        user='root',
        password='brey',
        database='crud_db'    
        )
    
    return connection

 
@app.route('/products', methods=['POST'])
def create_products():
    connection = get_db_connection()
    cursor = connection.cursor()
    data = request.get_json()
    ids = []
    required_fields = ['name','price']

    # Verificar si data es un arreglo o un objeto
    if isinstance(data, dict) and 'products' in data and isinstance(data['products'], list):
        # Es un arreglo
        for i in data['products']:
            for field in required_fields:
                if field not in i or not i[field]:
                    return jsonify({'error': f'field "{field}" is required and cannot be empty'}), 400
            
            name = i['name']
            price = i['price']
            if not isinstance(price, (float, int)) or price < 0:
                return jsonify({'error': "The price cannot be negative"})
            
            query = "INSERT INTO products (name,price) VALUES (%s, %s)"
            cursor.execute(query, (name,price))
            ids.append(cursor.lastrowid)

    elif isinstance(data, dict):
        # Es un objeto
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'field "{field}" is required and cannot be empty'}), 400
        
        name = data['name']
        price = data['price']
        if not isinstance(price, (float, int)) or price < 0:
            return jsonify({'error': "The price cannot be negative"})
        
        query = "INSERT INTO products (name,price) VALUES (%s, %s)"
        cursor.execute(query, (name,price))
        ids.append(cursor.lastrowid)
        
    else:
        return jsonify({'error': 'Invalid data format'}), 400

    connection.commit()

    if ids:
        return jsonify({'id': ids}), 201
    else:
        return jsonify({'error': 'Products not found'}), 400
       

@app.route('/products', methods=['GET'])
def get_products_objeto():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    return jsonify(products), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_products(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
    products = cursor.fetchone()

    if products:
        return jsonify(products), 200
    else: 
        return jsonify({'error': 'products not found'}), 404  


@app.route('/products', methods=['PUT'])
def update_products():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    data = request.get_json()
    rows_update = 0
    required_fields = ['name', 'price', 'id']


    if isinstance(data, dict) and 'products' in data and isinstance(data['products'], list):
        # Es un arreglo
        for i in data['products']:
            for field in required_fields:
                if field not in i or not i[field]:
                    return jsonify({'error': f'field "{field}" is required and cannot be empty'}), 400

            products_id = i['id']
            name = i['name']
            price = i['price']

            if not isinstance(price, (float, int)) or price < 0:
                return jsonify({'error': 'You cannot insert negative prices'}), 400

            query = "UPDATE products SET name = %s, price = %s WHERE id = %s"
            cursor.execute(query, (name, price, products_id))
            rows_update += cursor.rowcount

    elif isinstance(data, dict):
        # Es un objeto
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'field "{field}" It is mandatory and cannot be empty'}), 400

        products_id = data['id']
        name = data['name']
        price = data['price']

        if not isinstance(price, (float, int)) or price < 0:
            return jsonify({'error': 'You cannot insert negative prices'}), 400

        query = "UPDATE products SET name = %s, price = %s WHERE id = %s"
        cursor.execute(query, (name, price, products_id))
        rows_update += cursor.rowcount

    else:
        return jsonify({'error': 'Invalid data format'}), 400

    connection.commit()

    if rows_update > 0:
        return jsonify({'message': f'{rows_update} products updated successfully'}), 200
    else:
        return jsonify({'error': 'Products not updated'}), 404


@app.route('/products/<int:id>', methods=['PUT'])
def update_products_id(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    data = request.get_json()
    rows_update = 0
    required_fields = ['name','price']
   
    for field in required_fields:
            if field not in data or not data[field]:
                 return jsonify({'error':f'field"{field}" It is mandatory and cannot be empty'}), 400 
            
    name = data['name']
    price = data['price']
    if not isinstance(price, (float) or price < 0):
            return jsonify({'error': 'You cannot enter negative data'})
    
    query = "UPDATE products  SET name= %s, price = %s WHERE id = %s"
    cursor.execute(query, (name,price,id))
    rows_update += cursor.rowcount

    connection.commit()

    if cursor.rowcount > 0:
          return jsonify({'message':f'{rows_update} products updated correctly'}), 200
    else:
        return jsonify({'error': 'products not updated '}), 404


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if id is None:

        data = request.get_json()    

        if 'id' not in data:
            return jsonify({'error': 'The "id" field is required if not provided in the URL'}), 400
        
        product_id = data['id']
    else:

        product_id = id

    cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
    connection.commit()


    if cursor.rowcount > 0:
        return jsonify({'message': 'Product disposed correctly'}), 200
    else:
        return jsonify({'error': 'Product disposed correctly'}), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)