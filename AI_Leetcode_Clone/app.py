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
    try:
        # Check if API key is set
        if not os.getenv("OPENAI_API_KEY"):
            return jsonify({"error": "OpenAI API key not found. Please set OPENAI_API_KEY in your .env file"}), 500
        
        data = request.get_json()
        topic = data.get("topic", "Array")
        difficulty = data.get("difficulty", "Easy")

        # More specific prompt to ensure valid JSON response
        prompt = f"""Generate a {difficulty} level coding problem on the topic '{topic}'.
        
        Return ONLY a valid JSON object with these exact fields:
        {{
            "title": "Problem title",
            "description": "Detailed problem description",
            "category": "{topic}",
            "time_limit": 1000,
            "memory_limit": 128,
            "test_cases": [
                {{
                    "input": "sample input",
                    "output": "expected output"
                }}
            ]
        }}
        
        Make sure the response is valid JSON and includes at least 2 test cases."""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        return jsonify({"question": response.choices[0].message.content.strip()})
    
    except Exception as e:
        return jsonify({"error": f"Failed to generate question: {str(e)}"}), 500

@app.route("/add_question", methods=["POST"])
def add_question():
    data = request.get_json()
    required_fields = ["title", "description", "difficulty", "category", "time_limit", "memory_limit", "test_cases"]
    for field in required_fields:
        if field not in data or data[field] in (None, ""):
            return jsonify({"error": f"Missing or empty field: {field}"}), 400
    try:
        # Validate time_limit and memory_limit
        time_limit = int(data["time_limit"])
        memory_limit = int(data["memory_limit"])
        # Validate test_cases is a list
        test_cases = data["test_cases"]
        if isinstance(test_cases, str):
            test_cases = json.loads(test_cases)
        if not isinstance(test_cases, list):
            return jsonify({"error": "test_cases must be a list"}), 400
        # Save question
        question = Question(
            title=data["title"],
            description=data["description"],
            difficulty=data["difficulty"],
            category=data["category"],
            time_limit=time_limit,
            memory_limit=memory_limit,
            test_cases=json.dumps(test_cases)
        )
        db.session.add(question)
        db.session.commit()
        return jsonify({"message": "Question added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/generate")
def generate_page():
    return render_template("generate.html")

@app.route("/questions")
def view_questions():
    questions = Question.query.all()
    return render_template("questions.html", questions=questions)

@app.route("/api/questions")
def get_questions():
    questions = Question.query.all()
    return jsonify([{
        "id": q.id,
        "title": q.title,
        "description": q.description,
        "difficulty": q.difficulty,
        "category": q.category,
        "time_limit": q.time_limit,
        "memory_limit": q.memory_limit,
        "test_cases": json.loads(q.test_cases)
    } for q in questions])

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
