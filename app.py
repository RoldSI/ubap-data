from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import os
import pytz

load_dotenv()

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection string
MONGO_URL = os.getenv('MONGO_URL')
MONGO_AUTH = os.getenv('MONGO_AUTH')
client = MongoClient(f"mongodb+srv://{MONGO_AUTH}@{MONGO_URL}/?retryWrites=true&w=majority&appName=ubap")
client.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")

# Select the database and collection
db = client['ubap']
collection = db['data']

@app.route('/')
def hello():
    return 'Hello, World! This is the UBAP interface to interact with autonomous vehicles.'

@app.route('/submit/report', methods=['POST'])
def submit_report():
    # Get the JSON data from the request
    data = request.get_json()
    if not data or 'text' not in data or 'latitude' not in data or 'longitude' not in data or 'source' not in data:
        return jsonify({"error": "Not all fields provided"}), 400
    
    # Get the text from the JSON data
    text = data['text']
    longitude = data['longitude']
    latitude = data['latitude']
    source = data['source']
    
    # Create the document
    document = {
        "type": "report",
        "source": source,
        "timestamp": datetime.now(pytz.utc),
        "location": {
            "longitude": longitude,
            "latitude": latitude,
        },
        "text": text,
    }

    # Insert the document into the collection
    result = collection.insert_one(document)
    
    # Return a success response
    return jsonify({"message": "Text stored successfully", "id": str(result.inserted_id)}), 201

@app.route('/submit/uxv', methods=['POST'])
def submit_uxv():
    # Get the JSON data from the request
    data = request.get_json()
    if not data or 'latitude' not in data or 'longitude' not in data or 'goal_latitude' not in data or 'goal_longitude' not in data or 'uxv_id' not in data:
        return jsonify({"error": "Not all fields provided"}), 400
    
    # Get the text from the JSON data
    longitude = data['longitude']
    latitude = data['latitude']
    goal_longitude = data['goal_longitude']
    goal_latitude = data['goal_latitude']
    uxv_id = data['uxv_id']
    
    # Create the document
    document = {
        "type": "uxv",
        "uxv_id": uxv_id,
        "timestamp": datetime.now(pytz.utc),
        "location": {
            "longitude": longitude,
            "latitude": latitude
        },
        "goal": {
            "longitude": goal_longitude,
            "latitude": goal_latitude
        },
    }

    # Insert the document into the collection
    result = collection.insert_one(document)
    
    # Return a success response
    return jsonify({"message": "Text stored successfully", "id": str(result.inserted_id)}), 201

@app.route('/submit/image', methods=['POST'])
def submit_image():
    # Get the JSON data from the request
    data = request.get_json()
    if not data or 'latitude' not in data or 'longitude' not in data or 'url' not in data or 'uxv_id' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    # Get the text from the JSON data
    text = data['url']
    longitude = data['longitude']
    latitude = data['latitude']
    url = data['url']
    uxv_id = data['uxv_id']
    
    # Create the document
    document = {
        "type": "image",
        "uxv_id": uxv_id,
        "timestamp": datetime.now(pytz.utc),
        "location": {
            "longitude": longitude,
            "latitude": latitude
        },
        "url": url,
    }

    # Insert the document into the collection
    result = collection.insert_one(document)
    
    # Return a success response
    return jsonify({"message": "Text stored successfully", "id": str(result.inserted_id)}), 201

@app.route('/submit/landmark', methods=['POST'])
def submit_landmark():
    # Get the JSON data from the request
    data = request.get_json()
    if not data or 'latitude' not in data or 'longitude' not in data or 'uxv_id' not in data or 'detected_object' not in data:
        return jsonify({"error": "Not all fields provided"}), 400
    
    # Get the text from the JSON data
    longitude = data['longitude']
    latitude = data['latitude']
    uxv_id = data['uxv_id']
    detected_object = data['detected_object']
    
    # Create the document
    document = {
        "type": "landmark",
        "uxv_id": uxv_id,
        "timestamp": datetime.now(pytz.utc),
        "location": {
            "longitude": longitude,
            "latitude": latitude
        },
        "detected_object": detected_object
    }

    # Insert the document into the collection
    result = collection.insert_one(document)
    
    # Return a success response
    return jsonify({"message": "Text stored successfully", "id": str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)
