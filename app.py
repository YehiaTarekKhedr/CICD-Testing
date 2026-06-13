import os
from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(os.environ["MONGO_URI"])
db = client["yehiadb"]
collection = db["items"]

@app.route("/")
def home():
    return {"message": "Flask + MongoDB + Docker Volumes", "status": "ok"}

@app.route("/items", methods=["POST"])
def add_item():
    data = request.get_json()
    result = collection.insert_one({"name": data["name"]})
    return {"inserted_id": str(result.inserted_id)}, 201

@app.route("/items", methods=["GET"])
def get_items():
    items = list(collection.find({}, {"_id": 0}))
    return jsonify(items)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)