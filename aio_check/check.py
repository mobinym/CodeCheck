import os
import subprocess
import sys
from argparse import ArgumentParser
import re
import time
import json

TEST_CASES = [
    {"input": "2\n", "expected_output": "4\n"},
    {"input": "3\n", "expected_output": "9\n"},
    {"input": "5\n", "expected_output": "25\n"}
]


CORRECTNESS_WEIGHT = 0.7
STYLE_WEIGHT = 0.2
SYNTAX_WEIGHT = 0.1
FINALIZATION_THRESHOLD = 90


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def extract_numbers(text):
    return list(map(int, re.findall(r'\d+', text)))

def run_test_case(script_path, test_case):
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            input=test_case["input"],
            text=True,
            capture_output=True
        )
        actual = extract_numbers(result.stdout)
        expected = extract_numbers(test_case["expected_output"])
        return actual == expected
    except Exception:
        return False


def check_syntax(script_path):
    try:
        subprocess.check_output([sys.executable, "-m", "py_compile", script_path])
        return True
    except subprocess.CalledProcessError:
        return False


def evaluate_style(script):
    issues = []
    score = 100

    
    variables = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', script)
    non_snake_case = [var for var in variables if not re.match(r'^[a-z_][a-z0-9_]*$', var)]
    if non_snake_case:
        score -= 20
        for var in non_snake_case:
            issues.append(f"Variable '{var}' is not in snake_case.")

    
    lines = script.splitlines()
    for i, line in enumerate(lines):
        if len(line) > 79:
            score -= 2  
            issues.append(f"Line {i + 1} exceeds 79 characters.")

    return score, issues


def judge_code(script_path):
    
    with open(script_path, 'r') as f:
        script = f.read()

    
    correctness_score = sum(run_test_case(script_path, tc) for tc in TEST_CASES) / len(TEST_CASES) * 100

    
    style_score, style_issues = evaluate_style(script)

   
    syntax_score = 100 if check_syntax(script_path) else 0

    
    final_score = (
        correctness_score * CORRECTNESS_WEIGHT +
        style_score * STYLE_WEIGHT +
        syntax_score * SYNTAX_WEIGHT
    )

    
    feedback = {
        "Correctness": round(correctness_score, 2),
        "Style": round(style_score, 2),
        "Syntax": syntax_score,
        "Final Score": round(final_score, 2),
        "Style Issues": style_issues,
        "Finalized": final_score >= FINALIZATION_THRESHOLD
    }
    return feedback


def show_loading(message, duration=3):
    print(message, end="", flush=True)
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(1)
    print()


def save_feedback_text(feedback, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"{'=' * 40}\n")
        f.write("Code Evaluation Report\n")
        f.write(f"{'=' * 40}\n\n")

        f.write("Scores:\n")
        f.write(f"- Correctness: {feedback['Correctness']}%\n")
        f.write(f"- Style: {feedback['Style']}%\n")
        f.write(f"- Syntax: {feedback['Syntax']}%\n")
        f.write(f"- Final Score: {feedback['Final Score']}%\n\n")

        f.write("Evaluation Summary:\n")
        if feedback["Finalized"]:
            f.write("Your code is ACCEPTED ✅\n\n")
        else:
            f.write("Your code is REJECTED ❌\n\n")

        if feedback["Style Issues"]:
            f.write("Style Issues:\n")
            for issue in feedback["Style Issues"]:
                f.write(f"  - {issue}\n")
        else:
            f.write("No style issues detected.\n")

        f.write(f"\n{'=' * 40}\n")
        f.write("Detailed Feedback:\n")
        for issue in feedback["Style Issues"]:
            f.write(f"- {issue}\n")

def main():
    parser = ArgumentParser(description="A simple Python code evaluation tool.")
    parser.add_argument("-f", "--file", help="Path to the Python file to evaluate.", required=True)
    parser.add_argument("-o", "--output", help="Path to save the detailed feedback (TXT).", default=None)
    args = parser.parse_args()

    script_path = args.file

    if not os.path.exists(script_path):
        print(f"{Colors.FAIL}Error: File '{script_path}' does not exist.{Colors.ENDC}")
        sys.exit(1)

    
    show_loading("Evaluating your code", duration=3)

    
    feedback = judge_code(script_path)

    
    print("\nSummary:")
    print(f"Correctness: {feedback['Correctness']}%")
    print(f"Style: {feedback['Style']}%")
    print(f"Syntax: {feedback['Syntax']}%")
    print(f"Final Score: {feedback['Final Score']}%")
    if feedback["Finalized"]:
        print(f"{Colors.OKGREEN}Result: Your code passed the evaluation ✅{Colors.ENDC}")
    else:
        print(f"{Colors.FAIL}Result: Your code failed the evaluation ❌{Colors.ENDC}")

    
    if feedback["Style Issues"]:
        print("\nStyle Issues (Summary):")
        for issue in feedback["Style Issues"]:
            print(f"- {Colors.WARNING}{issue}{Colors.ENDC}")

    
    if args.output:
        try:
            save_feedback_text(feedback, args.output)
            print(f"\n{Colors.OKBLUE}Detailed feedback has been saved to '{args.output}'.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}Error saving TXT file: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()
#all in main