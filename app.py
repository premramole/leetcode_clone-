from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import openai
import json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leetcode_questions.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)
    memory_limit = db.Column(db.Integer, nullable=False)
    test_cases = db.Column(db.Text, nullable=False)

@app.route("/generate_question", methods=["POST"])
def generate_question():
    data = request.get_json()
    topic = data.get("topic", "Array")
    difficulty = data.get("difficulty", "Easy")

    prompt = f"Generate a {difficulty} level coding problem on the topic '{topic}' in JSON format with fields: title, description, category, time_limit, memory_limit, and test_cases (as a list of dicts with input and output)."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{{"role": "user", "content": prompt}}],
        temperature=0.7
    )

    return jsonify({{"question": response.choices[0].message.content.strip()}})

@app.route("/add_question", methods=["POST"])
def add_question():
    data = request.get_json()
    question = Question(
        title=data["title"],
        description=data["description"],
        difficulty=data["difficulty"],
        category=data["category"],
        time_limit=data["time_limit"],
        memory_limit=data["memory_limit"],
        test_cases=json.dumps(data["test_cases"])
    )
    db.session.add(question)
    db.session.commit()
    return jsonify({{"message": "Question added successfully"}})

@app.route("/generate")
def generate_page():
    return render_template("generate.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
