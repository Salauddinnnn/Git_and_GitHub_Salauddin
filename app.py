from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Connect to MongoDB Atlas
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("MONGO_DB")]
collection = db[os.getenv("MONGO_COLLECTION")]


# Read data from backend JSON file
def load_data():
    with open("data.json", "r") as file:
        return json.load(file)


# Task 1: JSON API route
@app.route("/api")
def api():
    data = load_data()
    return jsonify(data)


# Display the frontend form
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    item_name = request.form.get("itemName")
    item_description = request.form.get("itemDescription")

    todo_item = {
        "itemName": item_name,
        "itemDescription": item_description
    }

    db["todo_items"].insert_one(todo_item)

    return redirect(url_for("success"))

# Task 2: Submit form data to MongoDB Atlas
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form["name"]
        email = request.form["email"]
        course = request.form["course"]

        # Store submitted values in variables and create a document
        student_data = {
            "name": name,
            "email": email,
            "course": course
        }

        # Insert data into MongoDB
        collection.insert_one(student_data)

        # Success: redirect to another page
        return redirect(url_for("success"))

    except Exception as error:
        # Error: stay on the same page and display the error
        return render_template("index.html", error=str(error))


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
