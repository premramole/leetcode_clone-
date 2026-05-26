from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Simple in-memory storage for demo
users = {}
questions = [
    {
        'id': 1,
        'title': 'Two Sum',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
        'difficulty': 'Easy',
        'category': 'Array',
        'time_limit': 1000,
        'memory_limit': 128,
        'test_cases': [
            {'input': '[2,7,11,15]\n9', 'output': '[0,1]'},
            {'input': '[3,2,4]\n6', 'output': '[1,2]'}
        ]
    },
    {
        'id': 2,
        'title': 'Palindrome Number',
        'description': 'Given an integer x, return true if x is a palindrome, and false otherwise.',
        'difficulty': 'Easy',
        'category': 'Math',
        'time_limit': 1000,
        'memory_limit': 128,
        'test_cases': [
            {'input': '121', 'output': 'True'},
            {'input': '-121', 'output': 'False'}
        ]
    }
]

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

        if username in users:
            return jsonify({'error': 'Username already exists'}), 400

        users[username] = {
            'username': username,
            'email': email,
            'password': password,  # In real app, hash this
            'solved_questions': [],
            'submissions': []
        }

        return jsonify({'message': 'Registration successful'}), 201

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username in users and users[username]['password'] == password:
            session['user_id'] = username
            session['username'] = username
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
    
    user = users.get(session['user_id'], {})
    stats = {
        'solved_questions': len(user.get('solved_questions', [])),
        'total_submissions': len(user.get('submissions', [])),
        'accepted_submissions': sum(1 for s in user.get('submissions', []) if s.get('status') == 'Accepted')
    }
    
    return render_template('dashboard.html', user=user, stats=stats)

@app.route('/problems')
def problems():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('problems.html', questions=questions)

@app.route('/problem/<int:question_id>')
def problem(question_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    question = next((q for q in questions if q['id'] == question_id), None)
    if not question:
        return "Question not found", 404
    
    return render_template('problem.html', question=question)

@app.route('/api/questions')
def get_questions():
    return jsonify([{
        'id': q['id'],
        'title': q['title'],
        'difficulty': q['difficulty'],
        'category': q['category']
    } for q in questions])

@app.route('/api/stats')
def get_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = users.get(session['user_id'], {})
    return jsonify({
        'solved_questions': len(user.get('solved_questions', [])),
        'total_submissions': len(user.get('submissions', [])),
        'accepted_submissions': sum(1 for s in user.get('submissions', []) if s.get('status') == 'Accepted')
    })

@app.route('/test')
def test():
    return 'Hello! Flask is working!'

if __name__ == '__main__':
    app.run(debug=True, port=5000) 