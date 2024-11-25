# aio_check/check.py

import os
import subprocess
import sys
import re
from argparse import ArgumentParser

# Define test cases for evaluation
TEST_CASES = [
    {"input": "2\n", "expected_output": "4\n"},
    {"input": "3\n", "expected_output": "9\n"},
    {"input": "5\n", "expected_output": "25\n"}
]

# Thresholds for scoring
CORRECTNESS_WEIGHT = 0.7
STYLE_WEIGHT = 0.2
SYNTAX_WEIGHT = 0.1
FINALIZATION_THRESHOLD = 90

def extract_numbers(text):
    """
    Extracts all numbers (integers) from a given text.
    """
    return list(map(int, re.findall(r'\d+', text)))

def run_test_case(script_path, test_case):
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            input=test_case["input"],
            text=True,
            capture_output=True
        )
        actual_numbers = extract_numbers(result.stdout)
        expected_numbers = extract_numbers(test_case["expected_output"])
        
        if actual_numbers != expected_numbers:
            print(f"Failed: Expected {expected_numbers}, but got {actual_numbers}")
        return actual_numbers == expected_numbers
    except Exception as e:
        print(f"Error running test case: {e}")
        return False

def check_syntax(script_path):
    try:
        subprocess.check_output([sys.executable, "-m", "py_compile", script_path])
        return True
    except subprocess.CalledProcessError:
        return False

def check_snake_case(name):
    return bool(re.match(r'^[a-z_][a-z0-9_]*$', name))

def check_docstrings(script):
    functions = re.findall(r"def\s+(\w+)\s*\(.*\):", script)
    missing_docstrings = 0

    for func in functions:
        if not re.search(f"def {func}.*\"\"\"", script):
            missing_docstrings += 1
    
    return missing_docstrings == 0

def check_line_length(script, max_length=79):
    lines = script.splitlines()
    return all(len(line) <= max_length for line in lines)

def check_indentation(script, spaces_per_indent=4):
    lines = script.splitlines()
    for line in lines:
        if line.startswith(' '):
            spaces = len(line) - len(line.lstrip(' '))
            if spaces % spaces_per_indent != 0:
                return False
    return True

def evaluate_code_style(script):
    score = 100

    variables = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', script)
    non_snake_case = [var for var in variables if not check_snake_case(var)]
    if non_snake_case:
        score -= 20

    if not check_docstrings(script):
        score -= 20

    if not check_line_length(script):
        score -= 10

    if not check_indentation(script):
        score -= 10

    return score

def judge_code(script_path):
    with open(script_path, 'r') as f:
        script = f.read()

    correct_tests = sum(run_test_case(script_path, tc) for tc in TEST_CASES)
    correctness_score = (correct_tests / len(TEST_CASES)) * 100

    style_score = evaluate_code_style(script)

    syntax_score = 100 if check_syntax(script_path) else 0

    final_score = (
        correctness_score * CORRECTNESS_WEIGHT +
        style_score * STYLE_WEIGHT +
        syntax_score * SYNTAX_WEIGHT
    )

    feedback = {
        "correctness": correctness_score,
        "style": style_score,
        "syntax": syntax_score,
        "final_score": final_score,
        "finalized": final_score >= FINALIZATION_THRESHOLD
    }
    return feedback

def main():
    parser = ArgumentParser(description="Judge student code submissions via CLI.")
    parser.add_argument(
        "-f", "--file",
        help="Path to the Python file to be evaluated.",
        required=True
    )
    args = parser.parse_args()

    script_path = args.file

    if not os.path.exists(script_path):
        print(f"Error: File '{script_path}' does not exist.")
        sys.exit(1)

    feedback = judge_code(script_path)
    print("\nFeedback:")
    print(f"Correctness Score: {feedback['correctness']:.2f}")
    print(f"Style Score: {feedback['style']:.2f}")
    print(f"Syntax Score: {feedback['syntax']:.2f}")
    print(f"Final Score: {feedback['final_score']:.2f}")
    if feedback["finalized"]:
        print("Your submission has been finalized!")
    else:
        print("Your submission did not meet the finalization threshold. Try again!")

if __name__ == "__main__":
    main()
