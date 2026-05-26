#!/usr/bin/env python3
"""
Database Population Script
Populates the database with 1000+ sample problems from LeetCode and HackerRank
"""

import json
import random
from datetime import datetime
from enhanced_app import app, db, Question, User

# Sample problem data
SAMPLE_PROBLEMS = [
    # Python Problems
    {
        "title": "Two Sum",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "difficulty": "Easy",
        "category": "Array",
        "language": "python",
        "developer_track": "general",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
            {"input": "[3,2,4]\n6", "output": "[1,2]"},
            {"input": "[3,3]\n6", "output": "[0,1]"}
        ],
        "solution_template": {
            "python": "def twoSum(nums, target):\n    # Your solution here\n    pass\n\nnums = list(map(int, input().strip('[]').split(',')))\ntarget = int(input())\nresult = twoSum(nums, target)\nprint(result)"
        }
    },
    {
        "title": "Valid Parentheses",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "difficulty": "Easy",
        "category": "Stack",
        "language": "python",
        "developer_track": "backend",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": "()", "output": "True"},
            {"input": "()[]{}", "output": "True"},
            {"input": "(]", "output": "False"}
        ],
        "solution_template": {
            "python": "def isValid(s):\n    # Your solution here\n    pass\n\ns = input()\nresult = isValid(s)\nprint(result)"
        }
    },
    {
        "title": "Climbing Stairs",
        "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps.",
        "difficulty": "Easy",
        "category": "Dynamic Programming",
        "language": "python",
        "developer_track": "data",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": "2", "output": "2"},
            {"input": "3", "output": "3"},
            {"input": "4", "output": "5"}
        ],
        "solution_template": {
            "python": "def climbStairs(n):\n    # Your solution here\n    pass\n\nn = int(input())\nresult = climbStairs(n)\nprint(result)"
        }
    },
    {
        "title": "Reverse String",
        "description": "Write a function that reverses a string. The input string is given as an array of characters s.",
        "difficulty": "Easy",
        "category": "String",
        "language": "python",
        "developer_track": "frontend",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": '["h","e","l","l","o"]', "output": '["o","l","l","e","h"]'},
            {"input": '["H","a","n","n","a","h"]', "output": '["h","a","n","n","a","H"]'}
        ],
        "solution_template": {
            "python": "def reverseString(s):\n    # Your solution here\n    pass\n\ns = json.loads(input())\nreverseString(s)\nprint(json.dumps(s))"
        }
    },
    # Java Problems
    {
        "title": "Two Sum (Java)",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "difficulty": "Easy",
        "category": "Array",
        "language": "java",
        "developer_track": "backend",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
            {"input": "[3,2,4]\n6", "output": "[1,2]"}
        ],
        "solution_template": {
            "java": "import java.util.*;\n\npublic class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Your solution here\n        return new int[]{0, 1};\n    }\n}"
        }
    },
    {
        "title": "Valid Parentheses (Java)",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "difficulty": "Easy",
        "category": "Stack",
        "language": "java",
        "developer_track": "backend",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": "()", "output": "true"},
            {"input": "()[]{}", "output": "true"},
            {"input": "(]", "output": "false"}
        ],
        "solution_template": {
            "java": "import java.util.*;\n\npublic class Solution {\n    public boolean isValid(String s) {\n        // Your solution here\n        return true;\n    }\n}"
        }
    },
    # JavaScript Problems
    {
        "title": "Two Sum (JavaScript)",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "difficulty": "Easy",
        "category": "Array",
        "language": "javascript",
        "developer_track": "frontend",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
            {"input": "[3,2,4]\n6", "output": "[1,2]"}
        ],
        "solution_template": {
            "javascript": "function twoSum(nums, target) {\n    // Your solution here\n}\n\nconst nums = JSON.parse(input());\nconst target = parseInt(input());\nconsole.log(JSON.stringify(twoSum(nums, target)));"
        }
    },
    {
        "title": "Reverse String (JavaScript)",
        "description": "Write a function that reverses a string. The input string is given as an array of characters s.",
        "difficulty": "Easy",
        "category": "String",
        "language": "javascript",
        "developer_track": "frontend",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": '["h","e","l","l","o"]', "output": '["o","l","l","e","h"]'},
            {"input": '["H","a","n","n","a","h"]', "output": '["h","a","n","n","a","H"]'}
        ],
        "solution_template": {
            "javascript": "function reverseString(s) {\n    // Your solution here\n}\n\nconst s = JSON.parse(input());\nreverseString(s);\nconsole.log(JSON.stringify(s));"
        }
    },
    # C++ Problems
    {
        "title": "Two Sum (C++)",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "difficulty": "Easy",
        "category": "Array",
        "language": "cpp",
        "developer_track": "devops",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
            {"input": "[3,2,4]\n6", "output": "[1,2]"}
        ],
        "solution_template": {
            "cpp": "#include <iostream>\n#include <vector>\n#include <unordered_map>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Your solution here\n        return {0, 1};\n    }\n};\n\nint main() {\n    // Your main function here\n    return 0;\n}"
        }
    },
    # C# Problems
    {
        "title": "Two Sum (C#)",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "difficulty": "Easy",
        "category": "Array",
        "language": "csharp",
        "developer_track": "backend",
        "source": "leetcode",
        "time_limit": 1000,
        "memory_limit": 128,
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
            {"input": "[3,2,4]\n6", "output": "[1,2]"}
        ],
        "solution_template": {
            "csharp": "using System;\nusing System.Collections.Generic;\n\npublic class Solution {\n    public int[] TwoSum(int[] nums, int target) {\n        // Your solution here\n        return new int[]{0, 1};\n    }\n}"
        }
    }
]

# Generate more problems
def generate_problems():
    """Generate 1000+ problems with variations"""
    problems = []
    
    # Base problem templates
    base_problems = [
        {
            "title": "Maximum Subarray",
            "description": "Given an integer array nums, find the contiguous subarray with the largest sum.",
            "difficulty": "Medium",
            "category": "Dynamic Programming",
            "test_cases": [
                {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "output": "6"},
                {"input": "[1]", "output": "1"}
            ]
        },
        {
            "title": "Valid Anagram",
            "description": "Given two strings s and t, return true if t is an anagram of s, and false otherwise.",
            "difficulty": "Easy",
            "category": "String",
            "test_cases": [
                {"input": "anagram\nnagaram", "output": "true"},
                {"input": "rat\ncar", "output": "false"}
            ]
        },
        {
            "title": "Binary Tree Inorder Traversal",
            "description": "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
            "difficulty": "Easy",
            "category": "Tree",
            "test_cases": [
                {"input": "[1,null,2,3]", "output": "[1,3,2]"},
                {"input": "[]", "output": "[]"}
            ]
        },
        {
            "title": "Merge Two Sorted Lists",
            "description": "Merge two sorted linked lists and return it as a sorted list.",
            "difficulty": "Easy",
            "category": "Linked List",
            "test_cases": [
                {"input": "[1,2,4]\n[1,3,4]", "output": "[1,1,2,3,4,4]"},
                {"input": "[]\n[]", "output": "[]"}
            ]
        }
    ]
    
    # Languages and their templates
    languages = {
        "python": {
            "template": "def {function_name}({params}):\n    # Your solution here\n    pass\n\n{input_code}\nresult = {function_name}({args})\nprint(result)",
            "function_names": ["solve", "process", "calculate", "compute", "evaluate"]
        },
        "java": {
            "template": "import java.util.*;\n\npublic class Solution {{\n    public {return_type} {function_name}({params}) {{\n        // Your solution here\n        return {default_return};\n    }}\n}}",
            "function_names": ["solve", "process", "calculate", "compute", "evaluate"]
        },
        "javascript": {
            "template": "function {function_name}({params}) {{\n    // Your solution here\n}}\n\n{input_code}\nconsole.log(JSON.stringify({function_name}({args})));",
            "function_names": ["solve", "process", "calculate", "compute", "evaluate"]
        },
        "cpp": {
            "template": "#include <iostream>\n#include <vector>\nusing namespace std;\n\nclass Solution {{\npublic:\n    {return_type} {function_name}({params}) {{\n        // Your solution here\n        return {default_return};\n    }}\n}};\n\nint main() {{\n    // Your main function here\n    return 0;\n}}",
            "function_names": ["solve", "process", "calculate", "compute", "evaluate"]
        },
        "csharp": {
            "template": "using System;\nusing System.Collections.Generic;\n\npublic class Solution {{\n    public {return_type} {function_name}({params}) {{\n        // Your solution here\n        return {default_return};\n    }}\n}}",
            "function_names": ["solve", "process", "calculate", "compute", "evaluate"]
        }
    }
    
    # Developer tracks
    tracks = ["frontend", "backend", "data", "devops", "mobile", "fullstack"]
    
    # Sources
    sources = ["leetcode", "hackerrank"]
    
    # Categories
    categories = ["Array", "String", "Tree", "Graph", "Dynamic Programming", "Greedy", "Backtracking", "Binary Search", "Two Pointers", "Sliding Window", "Stack", "Queue", "Heap", "Hash Table", "Math", "Bit Manipulation", "Design", "SQL"]
    
    # Generate problems
    problem_id = 1
    for base_problem in base_problems:
        for language in languages.keys():
            for track in tracks:
                for source in sources:
                    for category in categories:
                        # Create problem variation
                        problem = {
                            "id": problem_id,
                            "title": f"{base_problem['title']} ({language.upper()})",
                            "description": base_problem['description'],
                            "difficulty": base_problem['difficulty'],
                            "category": category,
                            "language": language,
                            "developer_track": track,
                            "source": source,
                            "time_limit": random.randint(1000, 3000),
                            "memory_limit": random.randint(128, 512),
                            "test_cases": base_problem['test_cases'],
                            "solution_template": {
                                language: languages[language]["template"].format(
                                    function_name=random.choice(languages[language]["function_names"]),
                                    params="param1, param2",
                                    return_type="int" if language in ["java", "cpp", "csharp"] else "",
                                    default_return="0" if language in ["java", "cpp", "csharp"] else "",
                                    input_code="param1 = input()\nparam2 = input()",
                                    args="param1, param2"
                                )
                            }
                        }
                        problems.append(problem)
                        problem_id += 1
                        
                        # Limit to 1000 problems
                        if problem_id > 1000:
                            return problems
    
    return problems

def populate_database():
    """Populate the database with problems"""
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Check if problems already exist
        # if Question.query.count() > 0:
        #     print("Database already populated with problems.")
        #     return
        
        # Add sample problems
        print("Adding sample problems...")
        for problem_data in SAMPLE_PROBLEMS:
            question = Question(
                title=problem_data['title'],
                description=problem_data['description'],
                difficulty=problem_data['difficulty'],
                category=problem_data['category'],
                language=problem_data['language'],
                developer_track=problem_data['developer_track'],
                source=problem_data['source'],
                time_limit=problem_data['time_limit'],
                memory_limit=problem_data['memory_limit'],
                test_cases=json.dumps(problem_data['test_cases']),
                solution_template=json.dumps(problem_data['solution_template'])
            )
            db.session.add(question)
        
        # Generate additional problems
        print("Generating additional problems...")
        additional_problems = generate_problems()
        for problem_data in additional_problems:
            question = Question(
                title=problem_data['title'],
                description=problem_data['description'],
                difficulty=problem_data['difficulty'],
                category=problem_data['category'],
                language=problem_data['language'],
                developer_track=problem_data['developer_track'],
                source=problem_data['source'],
                time_limit=problem_data['time_limit'],
                memory_limit=problem_data['memory_limit'],
                test_cases=json.dumps(problem_data['test_cases']),
                solution_template=json.dumps(problem_data['solution_template'])
            )
            db.session.add(question)
        
        # Commit all changes
        db.session.commit()
        
        print(f"Successfully added {Question.query.count()} problems to the database!")
        
        # Print statistics
        print("\nDatabase Statistics:")
        print(f"Total problems: {Question.query.count()}")
        print(f"Python problems: {Question.query.filter_by(language='python').count()}")
        print(f"Java problems: {Question.query.filter_by(language='java').count()}")
        print(f"JavaScript problems: {Question.query.filter_by(language='javascript').count()}")
        print(f"C++ problems: {Question.query.filter_by(language='cpp').count()}")
        print(f"C# problems: {Question.query.filter_by(language='csharp').count()}")
        
        print(f"\nBy difficulty:")
        print(f"Easy: {Question.query.filter_by(difficulty='Easy').count()}")
        print(f"Medium: {Question.query.filter_by(difficulty='Medium').count()}")
        print(f"Hard: {Question.query.filter_by(difficulty='Hard').count()}")
        
        print(f"\nBy developer track:")
        for track in ['frontend', 'backend', 'data', 'devops', 'mobile', 'fullstack']:
            count = Question.query.filter_by(developer_track=track).count()
            print(f"{track.capitalize()}: {count}")

if __name__ == "__main__":
    populate_database() 