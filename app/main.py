from flask import Flask, jsonify, request
from db import get_all_customers, create_customer

app = Flask(__name__)

@app.route("/")
def root():
    return jsonify(message= "Python + Docker + PostgreSQL is running")

@app.route("/customers", methods=["GET"])
def list_customers():
    customers = get_all_customers()
    return jsonify(customers)

@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify(error="Name and email are required"), 400
    
    try:
        new_customer = create_customer(name,email)
        return jsonify(new_customer), 201
    except Exception as e:
        return jsonify(error=str(e)), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)