from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

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
def submit_text():
    # Get the JSON data from the request
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    # Get the text from the JSON data
    text = data['text']
    
    # Create the document
    document = {
        "type": "report",
        "text": text
    }

    # Insert the document into the collection
    result = collection.insert_one(document)
    
    # Return a success response
    return jsonify({"message": "Text stored successfully", "id": str(result.inserted_id)}), 201

if __name__ == '__main__':
    app.run(debug=True)
