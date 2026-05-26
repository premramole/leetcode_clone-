from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import time
import json
import os
import tempfile
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leetuser:leetpassword@localhost/leetcode_clone'
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Enhanced Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    solved_questions = db.Column(db.Text, default='[]')
    submissions = db.Column(db.Text, default='[]')
    preferred_language = db.Column(db.String(20), default='python')
    developer_track = db.Column(db.String(50), default='general')
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
    language = db.Column(db.String(20), default='python')
    developer_track = db.Column(db.String(50), default='general')
    source = db.Column(db.String(20), default='leetcode')
    time_limit = db.Column(db.Integer, default=1000)
    memory_limit = db.Column(db.Integer, default=128)
    test_cases = db.Column(db.Text, nullable=False)
    solution_template = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def get_test_cases(self):
        return json.loads(self.test_cases)

    def get_solution_template(self):
        return json.loads(self.solution_template)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    runtime = db.Column(db.Float)
    memory = db.Column(db.Float)
    submitted_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Code Execution Engine
class CodeExecutor:
    @staticmethod
    def run_code(code, test_cases, time_limit, memory_limit, language='python'):
        results = []
        
        for i, test_case in enumerate(test_cases):
            try:
                # Create temporary file for user code
                file_extension = {
                    'python': '.py',
                    'java': '.java',
                    'javascript': '.js',
                    'cpp': '.cpp',
                    'csharp': '.cs'
                }.get(language, '.py')
                
                with tempfile.NamedTemporaryFile(mode='w', suffix=file_extension, delete=False) as f:
                    f.write(code)
                    temp_file = f.name

                # Prepare input
                input_data = test_case['input'].encode()

                # Run the code based on language
                if language == 'python':
                    cmd = ['python', temp_file]
                elif language == 'java':
                    # Compile and run Java
                    class_name = 'Solution'
                    compile_cmd = ['javac', temp_file]
                    run_cmd = ['java', '-cp', os.path.dirname(temp_file), class_name]
                    subprocess.run(compile_cmd, capture_output=True, text=True)
                    cmd = run_cmd
                elif language == 'javascript':
                    cmd = ['node', temp_file]
                elif language == 'cpp':
                    # Compile and run C++
                    output_file = temp_file.replace('.cpp', '.exe')
                    compile_cmd = ['g++', temp_file, '-o', output_file]
                    subprocess.run(compile_cmd, capture_output=True, text=True)
                    cmd = [output_file]
                else:
                    cmd = ['python', temp_file]  # Default to Python

                # Run the code
                start_time = time.time()
                result = subprocess.run(
                    cmd,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=time_limit/1000
                )
                end_time = time.time()

                runtime = (end_time - start_time) * 1000

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
                # Clean up temporary files
                if 'temp_file' in locals():
                    try:
                        os.unlink(temp_file)
                    except:
                        pass

        return results

# Developer Tracks Data
DEVELOPER_TRACKS = {
    "frontend": {
        "name": "Frontend Developer",
        "description": "Master HTML, CSS, JavaScript, React, Vue.js, and modern frontend technologies",
        "icon": "fas fa-palette",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "TypeScript", "SASS", "Webpack"],
        "problems": [201, 202, 203, 204, 205]
    },
    "backend": {
        "name": "Backend Developer", 
        "description": "Learn server-side development with Python, Java, Node.js, and databases",
        "icon": "fas fa-server",
        "skills": ["Python", "Java", "Node.js", "SQL", "MongoDB", "Redis", "Docker", "AWS"],
        "problems": [1, 2, 3, 4, 101, 102, 103, 104]
    },
    "data": {
        "name": "Data Analytics",
        "description": "Focus on data science, machine learning, and statistical analysis",
        "icon": "fas fa-chart-bar",
        "skills": ["Python", "Pandas", "NumPy", "Matplotlib", "SQL", "R", "Jupyter", "TensorFlow"],
        "problems": [1, 2, 3, 4, 5, 6, 7, 8]
    },
    "devops": {
        "name": "DevOps Engineer",
        "description": "Learn infrastructure, CI/CD, cloud platforms, and system administration",
        "icon": "fas fa-cloud",
        "skills": ["Docker", "Kubernetes", "AWS", "Azure", "Jenkins", "Terraform", "Linux", "Bash"],
        "problems": [301, 302, 303, 304]
    },
    "mobile": {
        "name": "Mobile Developer",
        "description": "Develop iOS and Android applications with modern frameworks",
        "icon": "fas fa-mobile-alt",
        "skills": ["Swift", "Kotlin", "React Native", "Flutter", "Xcode", "Android Studio"],
        "problems": [201, 202, 203, 204, 205]
    },
    "fullstack": {
        "name": "Full Stack Developer",
        "description": "Master both frontend and backend development for complete web applications",
        "icon": "fas fa-layer-group",
        "skills": ["HTML", "CSS", "JavaScript", "Python", "Java", "SQL", "React", "Node.js"],
        "problems": [1, 2, 3, 4, 201, 202, 203, 204]
    }
}

# Programming Languages Data
LANGUAGES = {
    "python": {
        "name": "Python",
        "icon": "fab fa-python"
    },
    "java": {
        "name": "Java", 
        "icon": "fab fa-java"
    },
    "javascript": {
        "name": "JavaScript",
        "icon": "fab fa-js-square"
    },
    "cpp": {
        "name": "C++",
        "icon": "fas fa-code"
    },
    "csharp": {
        "name": "C#",
        "icon": "fas fa-code"
    }
}

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            preferred_language = data.get('preferred_language', 'python')
            developer_track = data.get('developer_track', 'general')

            if User.query.filter_by(username=username).first():
                return jsonify({'error': 'Username already exists'}), 400

            if User.query.filter_by(email=email).first():
                return jsonify({'error': 'Email already exists'}), 400

            user = User(
                username=username, 
                email=email,
                preferred_language=preferred_language,
                developer_track=developer_track
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            return jsonify({'message': 'Registration successful'}), 201
        except Exception as e:
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
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
    language = request.args.get('language', 'all')
    track = request.args.get('track', 'all')
    source = request.args.get('source', 'all')
    
    query = Question.query
    
    if difficulty != 'all':
        query = query.filter_by(difficulty=difficulty)
    if category != 'all':
        query = query.filter_by(category=category)
    if language != 'all':
        query = query.filter_by(language=language)
    if track != 'all':
        query = query.filter_by(developer_track=track)
    if source != 'all':
        query = query.filter_by(source=source)
    
    questions = query.all()
    return render_template('problems.html', questions=questions)

@app.route('/problem/<int:question_id>')
def problem(question_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    question = Question.query.get_or_404(question_id)
    return render_template('problem.html', question=question)

@app.route('/tracks')
def tracks():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('tracks.html', tracks=DEVELOPER_TRACKS)

@app.route('/languages')
def languages():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('languages.html', languages=LANGUAGES)

@app.route('/api/submit', methods=['POST'])
def submit_solution():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json()
    question_id = data.get('question_id')
    code = data.get('code')
    language = data.get('language', 'python')
    
    question = Question.query.get_or_404(question_id)
    test_cases = question.get_test_cases()
    
    # Execute code
    results = CodeExecutor.run_code(code, test_cases, question.time_limit, question.memory_limit, language)
    
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
        'language': language,
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
    language = request.args.get('language', 'all')
    track = request.args.get('track', 'all')
    source = request.args.get('source', 'all')
    
    query = Question.query
    
    if difficulty != 'all':
        query = query.filter_by(difficulty=difficulty)
    if category != 'all':
        query = query.filter_by(category=category)
    if language != 'all':
        query = query.filter_by(language=language)
    if track != 'all':
        query = query.filter_by(developer_track=track)
    if source != 'all':
        query = query.filter_by(source=source)
    
    questions = query.all()
    return jsonify([{
        'id': q.id,
        'title': q.title,
        'difficulty': q.difficulty,
        'category': q.category,
        'language': q.language,
        'developer_track': q.developer_track,
        'source': q.source
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

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True) 