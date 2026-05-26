from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import time
import json
import os
import tempfile
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leetuser:leetpassword@localhost/leetcode_clone'
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    solved_questions = db.Column(db.Text, default='[]')
    submissions = db.Column(db.Text, default='[]')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_solved_questions(self):
        return json.loads(self.solved_questions)

    def add_solved_question(self, question_id):
        solved = self.get_solved_questions()
        if question_id not in solved:
            solved.append(question_id)
            self.solved_questions = json.dumps(solved)

    def get_submissions(self):
        return json.loads(self.submissions)

    def add_submission(self, submission_data):
        submissions = self.get_submissions()
        submissions.append(submission_data)
        self.submissions = json.dumps(submissions)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    time_limit = db.Column(db.Integer, default=1000)  # milliseconds
    memory_limit = db.Column(db.Integer, default=128)  # MB
    test_cases = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def get_test_cases(self):
        return json.loads(self.test_cases)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # Accepted, Wrong Answer, Time Limit Exceeded, Runtime Error
    runtime = db.Column(db.Float)  # milliseconds
    memory = db.Column(db.Float)  # MB
    submitted_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Code Execution Engine
class CodeExecutor:
    @staticmethod
    def run_code(code, test_cases, time_limit, memory_limit):
        results = []
        
        for i, test_case in enumerate(test_cases):
            try:
                # Create temporary file for user code
                with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                    f.write(code)
                    temp_file = f.name

                # Prepare input
                input_data = test_case['input'].encode()

                # Run the code
                start_time = time.time()
                result = subprocess.run(
                    ['python', temp_file],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=time_limit/1000  # Convert to seconds
                )
                end_time = time.time()

                runtime = (end_time - start_time) * 1000  # Convert to milliseconds

                # Check if output matches expected
                expected_output = test_case['output'].strip()
                actual_output = result.stdout.strip()

                if result.returncode == 0 and actual_output == expected_output:
                    status = "Accepted"
                else:
                    status = "Wrong Answer"

                results.append({
                    'test_case': i + 1,
                    'status': status,
                    'runtime': runtime,
                    'expected': expected_output,
                    'actual': actual_output,
                    'error': result.stderr if result.stderr else None
                })

            except subprocess.TimeoutExpired:
                results.append({
                    'test_case': i + 1,
                    'status': "Time Limit Exceeded",
                    'runtime': time_limit,
                    'expected': test_case['output'],
                    'actual': None,
                    'error': "Time limit exceeded"
                })
            except Exception as e:
                results.append({
                    'test_case': i + 1,
                    'status': "Runtime Error",
                    'runtime': 0,
                    'expected': test_case['output'],
                    'actual': None,
                    'error': str(e)
                })
            finally:
                # Clean up temporary file
                if 'temp_file' in locals():
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

        return results

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Registration successful'}), 201

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'message': 'Login successful'}), 200

        return jsonify({'error': 'Invalid username or password'}), 401

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    stats = {
        'solved_questions': len(user.get_solved_questions()),
        'total_submissions': len(user.get_submissions()),
        'accepted_submissions': sum(1 for s in user.get_submissions() if s.get('status') == 'Accepted')
    }
    
    return render_template('dashboard.html', user=user, stats=stats)

@app.route('/problems')
def problems():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    difficulty = request.args.get('difficulty', 'all')
    category = request.args.get('category', 'all')
    
    query = Question.query
    
    if difficulty != 'all':
        query = query.filter_by(difficulty=difficulty)
    if category != 'all':
        query = query.filter_by(category=category)
    
    questions = query.all()
    return render_template('problems.html', questions=questions)

@app.route('/problem/<int:question_id>')
def problem(question_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    question = Question.query.get_or_404(question_id)
    return render_template('problem.html', question=question)

@app.route('/api/submit', methods=['POST'])
def submit_solution():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    question_id = data.get('question_id')
    code = data.get('code')
    
    question = Question.query.get_or_404(question_id)
    test_cases = question.get_test_cases()
    
    # Execute code
    results = CodeExecutor.run_code(code, test_cases, question.time_limit, question.memory_limit)
    
    # Determine overall status
    all_accepted = all(r['status'] == 'Accepted' for r in results)
    overall_status = 'Accepted' if all_accepted else 'Failed'
    
    # Calculate average runtime
    valid_runtimes = [r['runtime'] for r in results if r['runtime'] is not None]
    avg_runtime = sum(valid_runtimes) / len(valid_runtimes) if valid_runtimes else 0
    
    # Save submission
    user = User.query.get(session['user_id'])
    submission_data = {
        'question_id': question_id,
        'code': code,
        'status': overall_status,
        'runtime': avg_runtime,
        'timestamp': time.time()
    }
    user.add_submission(submission_data)
    
    if overall_status == 'Accepted':
        user.add_solved_question(question_id)
    
    db.session.commit()
    
    return jsonify({
        'status': overall_status,
        'runtime': avg_runtime,
        'results': results
    })

@app.route('/api/questions')
def get_questions():
    difficulty = request.args.get('difficulty', 'all')
    category = request.args.get('category', 'all')
    
    query = Question.query
    
    if difficulty != 'all':
        query = query.filter_by(difficulty=difficulty)
    if category != 'all':
        query = query.filter_by(category=category)
    
    questions = query.all()
    return jsonify([{
        'id': q.id,
        'title': q.title,
        'difficulty': q.difficulty,
        'category': q.category
    } for q in questions])

@app.route('/api/stats')
def get_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = User.query.get(session['user_id'])
    return jsonify({
        'solved_questions': len(user.get_solved_questions()),
        'total_submissions': len(user.get_submissions()),
        'accepted_submissions': sum(1 for s in user.get_submissions() if s.get('status') == 'Accepted')
    })

# Admin routes for adding questions
@app.route('/admin/add_question', methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        data = request.get_json()
        
        question = Question(
            title=data['title'],
            description=data['description'],
            difficulty=data['difficulty'],
            category=data['category'],
            time_limit=data['time_limit'],
            memory_limit=data['memory_limit'],
            test_cases=json.dumps(data['test_cases'])
        )
        
        db.session.add(question)
        db.session.commit()
        
        return jsonify({'message': 'Question added successfully'}), 201
    
    return render_template('admin_add_question.html')

# Initialize database and add sample questions
def init_db():
    with app.app_context():
        db.create_all()
        
        # Add sample questions if database is empty
        if Question.query.count() == 0:
            sample_questions = [
                {
                    'title': 'Two Sum',
                    'description': '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]''',
                    'difficulty': 'Easy',
                    'category': 'Array',
                    'time_limit': 1000,
                    'memory_limit': 128,
                    'test_cases': [
                        {'input': '[2,7,11,15]\n9', 'output': '[0,1]'},
                        {'input': '[3,2,4]\n6', 'output': '[1,2]'},
                        {'input': '[3,3]\n6', 'output': '[0,1]'}
                    ]
                },
                {
                    'title': 'Palindrome Number',
                    'description': '''Given an integer x, return true if x is a palindrome, and false otherwise.

Example 1:
Input: x = 121
Output: true
Explanation: 121 reads as 121 from left to right and from right to left.

Example 2:
Input: x = -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.

Example 3:
Input: x = 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.''',
                    'difficulty': 'Easy',
                    'category': 'Math',
                    'time_limit': 1000,
                    'memory_limit': 128,
                    'test_cases': [
                        {'input': '121', 'output': 'True'},
                        {'input': '-121', 'output': 'False'},
                        {'input': '10', 'output': 'False'}
                    ]
                },
                {
                    'title': 'Valid Parentheses',
                    'description': '''Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Example 1:
Input: s = "()"
Output: true

Example 2:
Input: s = "()[]{}"
Output: true

Example 3:
Input: s = "(]"
Output: false''',
                    'difficulty': 'Easy',
                    'category': 'Stack',
                    'time_limit': 1000,
                    'memory_limit': 128,
                    'test_cases': [
                        {'input': '()', 'output': 'True'},
                        {'input': '()[]{}', 'output': 'True'},
                        {'input': '(]', 'output': 'False'}
                    ]
                }
            ]
            
            for q_data in sample_questions:
                question = Question(
                    title=q_data['title'],
                    description=q_data['description'],
                    difficulty=q_data['difficulty'],
                    category=q_data['category'],
                    time_limit=q_data['time_limit'],
                    memory_limit=q_data['memory_limit'],
                    test_cases=json.dumps(q_data['test_cases'])
                )
                db.session.add(question)
            
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 