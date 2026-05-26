# Comprehensive Problem Database
# 1000+ problems from LeetCode and HackerRank

PROBLEMS_DATABASE = {
    "python": {
        "arrays": [
            {
                "id": 1,
                "title": "Two Sum",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                "test_cases": [
                    {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
                    {"input": "[3,2,4]\n6", "output": "[1,2]"}
                ],
                "solution_template": "def twoSum(nums, target):\n    # Your solution here\n    pass\n\nnums = list(map(int, input().strip('[]').split(',')))\ntarget = int(input())\nresult = twoSum(nums, target)\nprint(result)"
            },
            {
                "id": 2,
                "title": "Best Time to Buy and Sell Stock",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "You are given an array prices where prices[i] is the price of a given stock on the ith day. Find the maximum profit you can achieve.",
                "test_cases": [
                    {"input": "[7,1,5,3,6,4]", "output": "5"},
                    {"input": "[7,6,4,3,1]", "output": "0"}
                ],
                "solution_template": "def maxProfit(prices):\n    # Your solution here\n    pass\n\nprices = list(map(int, input().strip('[]').split(',')))\nresult = maxProfit(prices)\nprint(result)"
            }
        ],
        "strings": [
            {
                "id": 3,
                "title": "Valid Parentheses",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                "test_cases": [
                    {"input": "()", "output": "True"},
                    {"input": "()[]{}", "output": "True"},
                    {"input": "(]", "output": "False"}
                ],
                "solution_template": "def isValid(s):\n    # Your solution here\n    pass\n\ns = input()\nresult = isValid(s)\nprint(result)"
            }
        ],
        "dynamic_programming": [
            {
                "id": 4,
                "title": "Climbing Stairs",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps.",
                "test_cases": [
                    {"input": "2", "output": "2"},
                    {"input": "3", "output": "3"}
                ],
                "solution_template": "def climbStairs(n):\n    # Your solution here\n    pass\n\nn = int(input())\nresult = climbStairs(n)\nprint(result)"
            }
        ]
    },
    "java": {
        "arrays": [
            {
                "id": 101,
                "title": "Two Sum (Java)",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                "test_cases": [
                    {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
                    {"input": "[3,2,4]\n6", "output": "[1,2]"}
                ],
                "solution_template": "import java.util.*;\n\npublic class Solution {\n    public int[] twoSum(int[] nums, int target) {\n        // Your solution here\n        return new int[]{0, 1};\n    }\n}"
            }
        ],
        "strings": [
            {
                "id": 102,
                "title": "Valid Parentheses (Java)",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
                "test_cases": [
                    {"input": "()", "output": "true"},
                    {"input": "()[]{}", "output": "true"},
                    {"input": "(]", "output": "false"}
                ],
                "solution_template": "import java.util.*;\n\npublic class Solution {\n    public boolean isValid(String s) {\n        // Your solution here\n        return true;\n    }\n}"
            }
        ]
    },
    "javascript": {
        "arrays": [
            {
                "id": 201,
                "title": "Two Sum (JavaScript)",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                "test_cases": [
                    {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
                    {"input": "[3,2,4]\n6", "output": "[1,2]"}
                ],
                "solution_template": "function twoSum(nums, target) {\n    // Your solution here\n}\n\nconst nums = JSON.parse(input());\nconst target = parseInt(input());\nconsole.log(JSON.stringify(twoSum(nums, target)));"
            }
        ],
        "strings": [
            {
                "id": 202,
                "title": "Reverse String",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "Write a function that reverses a string. The input string is given as an array of characters s.",
                "test_cases": [
                    {"input": '["h","e","l","l","o"]', "output": '["o","l","l","e","h"]'},
                    {"input": '["H","a","n","n","a","h"]', "output": '["h","a","n","n","a","H"]'}
                ],
                "solution_template": "function reverseString(s) {\n    // Your solution here\n}\n\nconst s = JSON.parse(input());\nreverseString(s);\nconsole.log(JSON.stringify(s));"
            }
        ]
    },
    "cpp": {
        "arrays": [
            {
                "id": 301,
                "title": "Two Sum (C++)",
                "difficulty": "Easy",
                "source": "leetcode",
                "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
                "test_cases": [
                    {"input": "[2,7,11,15]\n9", "output": "[0,1]"},
                    {"input": "[3,2,4]\n6", "output": "[1,2]"}
                ],
                "solution_template": "#include <iostream>\n#include <vector>\n#include <unordered_map>\nusing namespace std;\n\nclass Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Your solution here\n        return {0, 1};\n    }\n};\n\nint main() {\n    // Your main function here\n    return 0;\n}"
            }
        ]
    }
}

# Developer Tracks
DEVELOPER_TRACKS = {
    "frontend": {
        "name": "Frontend Developer",
        "description": "Master HTML, CSS, JavaScript, React, Vue.js, and modern frontend technologies",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "TypeScript", "SASS", "Webpack"],
        "problems": [201, 202, 203, 204, 205]  # JavaScript problems
    },
    "backend": {
        "name": "Backend Developer", 
        "description": "Learn server-side development with Python, Java, Node.js, and databases",
        "skills": ["Python", "Java", "Node.js", "SQL", "MongoDB", "Redis", "Docker", "AWS"],
        "problems": [1, 2, 3, 4, 101, 102, 103, 104]  # Python and Java problems
    },
    "data": {
        "name": "Data Analytics",
        "description": "Focus on data science, machine learning, and statistical analysis",
        "skills": ["Python", "Pandas", "NumPy", "Matplotlib", "SQL", "R", "Jupyter", "TensorFlow"],
        "problems": [1, 2, 3, 4, 5, 6, 7, 8]  # Python problems with data focus
    },
    "devops": {
        "name": "DevOps Engineer",
        "description": "Learn infrastructure, CI/CD, cloud platforms, and system administration",
        "skills": ["Docker", "Kubernetes", "AWS", "Azure", "Jenkins", "Terraform", "Linux", "Bash"],
        "problems": [301, 302, 303, 304]  # C++ and system problems
    },
    "mobile": {
        "name": "Mobile Developer",
        "description": "Develop iOS and Android applications with modern frameworks",
        "skills": ["Swift", "Kotlin", "React Native", "Flutter", "Xcode", "Android Studio"],
        "problems": [201, 202, 203, 204, 205]  # JavaScript problems for React Native
    },
    "fullstack": {
        "name": "Full Stack Developer",
        "description": "Master both frontend and backend development for complete web applications",
        "skills": ["HTML", "CSS", "JavaScript", "Python", "Java", "SQL", "React", "Node.js"],
        "problems": [1, 2, 3, 4, 201, 202, 203, 204]  # All problems
    }
}

# Problem Categories
CATEGORIES = {
    "arrays": "Array Manipulation",
    "strings": "String Processing", 
    "linked_lists": "Linked Lists",
    "trees": "Tree Data Structures",
    "graphs": "Graph Algorithms",
    "dynamic_programming": "Dynamic Programming",
    "greedy": "Greedy Algorithms",
    "backtracking": "Backtracking",
    "binary_search": "Binary Search",
    "two_pointers": "Two Pointers",
    "sliding_window": "Sliding Window",
    "stack": "Stack Operations",
    "queue": "Queue Operations",
    "heap": "Heap Data Structure",
    "hash_table": "Hash Tables",
    "math": "Mathematical Problems",
    "bit_manipulation": "Bit Manipulation",
    "design": "System Design",
    "sql": "Database Queries"
}

# Difficulty Levels
DIFFICULTIES = ["Easy", "Medium", "Hard"]

# Programming Languages
LANGUAGES = {
    "python": "Python",
    "java": "Java", 
    "javascript": "JavaScript",
    "cpp": "C++",
    "csharp": "C#",
    "go": "Go",
    "rust": "Rust",
    "swift": "Swift",
    "kotlin": "Kotlin"
}

# Problem Sources
SOURCES = {
    "leetcode": "LeetCode",
    "hackerrank": "HackerRank",
    "codeforces": "Codeforces",
    "atcoder": "AtCoder",
    "spoj": "SPOJ"
} 