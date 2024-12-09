import os
import subprocess
import sys
from argparse import ArgumentParser
import re
import time
import json
from rich.console import Console
from rich.table import Table
from rich.progress import track

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

def run_test_case(script_path, test_case, timeout=5, debug=False):
    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, script_path],
            input=test_case["input"],
            text=True,
            capture_output=True,
            timeout=timeout
        )
        elapsed_time = time.time() - start_time
        actual = extract_numbers(result.stdout)
        expected = extract_numbers(test_case["expected_output"])
        if debug:
            print(f"Test Input: {test_case['input']} | Expected: {expected} | Actual: {actual} | Time: {elapsed_time:.2f}s")
        return actual == expected, elapsed_time
    except subprocess.TimeoutExpired:
        if debug:
            print("Test case timed out!")
        return False, timeout
    except Exception as e:
        if debug:
            print(f"Error running test case: {e}")
        return False, 0

def check_syntax(script_path, debug=False):
    try:
        subprocess.check_output([sys.executable, "-m", "py_compile", script_path])
        return True
    except subprocess.CalledProcessError as e:
        if debug:
            print(f"Syntax check failed: {e}")
        return False

def evaluate_style(script, debug=False):
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

    if debug:
        print(f"Style Score: {score} | Issues: {issues}")
    return score, issues

def fix_style(script_path, debug=False):
    try:
        subprocess.run(["autopep8", "--in-place", script_path], check=True)
        if debug:
            print(f"Style issues fixed successfully in {script_path}.")
    except Exception as e:
        print(f"Failed to fix style issues: {e}")

def judge_code(script_path, debug=False):
    with open(script_path, 'r') as f:
        script = f.read()

    correctness_details = [
        run_test_case(script_path, tc, debug=debug)
        for tc in TEST_CASES
    ]
    correctness_score = sum(1 for result, _ in correctness_details if result) / len(TEST_CASES) * 100
    execution_times = [time for _, time in correctness_details]
    style_score, style_issues = evaluate_style(script, debug)
    syntax_score = 100 if check_syntax(script_path, debug) else 0

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
        "Execution Times": execution_times,
        "Style Issues": style_issues,
        "Finalized": final_score >= FINALIZATION_THRESHOLD
    }
    if debug:
        print(f"Final Feedback: {feedback}")
    return feedback

def show_loading():
    console = Console()
    with console.status("Running test cases...") as status:
        time.sleep(10)  

def get_color(score):
    if score >= 80:
        return "bold green"
    elif score >= 50:
        return "bold yellow"
    else:
        return "bold red"

def show_results(feedback):
    console = Console()

    final_msg = "Your code is ACCEPTED ✅ for final judgment!" if feedback["Finalized"] else "Your code is REJECTED ❌"

  
    table = Table(show_header=True, header_style="bold green")
    table.add_column("Category", style="dim")
    table.add_column("Score/Feedback", style="bold white")


    table.add_row("Correctness", f"[{get_color(feedback['Correctness'])}]{feedback['Correctness']}%[/{get_color(feedback['Correctness'])}]")
    table.add_row("Style", f"[{get_color(feedback['Style'])}]{feedback['Style']}%[/{get_color(feedback['Style'])}]")
    table.add_row("Syntax", f"[{get_color(feedback['Syntax'])}]{feedback['Syntax']}%[/{get_color(feedback['Syntax'])}]")
    table.add_row("Final Score", f"[{get_color(feedback['Final Score'])}]{feedback['Final Score']}%[/{get_color(feedback['Final Score'])}]")

    table.add_row("Execution Times", "\n".join([f"[bold blue]Test {i+1}: {time:.2f}s[/bold blue]" for i, time in enumerate(feedback['Execution Times'])]))


    style_issues = "\n".join(feedback["Style Issues"]) if feedback["Style Issues"] else "No style issues found"
    table.add_row("Style Issues", f"[{get_color(feedback['Final Score'])}]{style_issues}[/{get_color(feedback['Final Score'])}]")


    console.print(table)
    console.print(final_msg)



def save_feedback_text(feedback, output_path):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("Code Evaluation Report\n")
            f.write("-----------------------\n")
            f.write("Scores:\n")
            f.write(f"  Correctness: {feedback['Correctness']}%\n")
            f.write(f"  Style: {feedback['Style']}%\n")
            f.write(f"  Syntax: {feedback['Syntax']}%\n")
            f.write(f"  Final Score: {feedback['Final Score']}%\n\n")

            f.write("Execution Times:\n")
            for i, time in enumerate(feedback["Execution Times"]):
                f.write(f"  Test {i + 1}: {time:.2f}s\n")

            f.write("\n")
            f.write("Style Issues:\n")
            if feedback["Style Issues"]:
                for issue in feedback["Style Issues"]:
                    f.write(f"  - {issue}\n")
            else:
                f.write("  No style issues found\n")

            f.write("\n")
            final_msg = (
                "Your code is ACCEPTED ✅\n"
                if feedback["Finalized"]
                else "Your code is REJECTED ❌\n"
            )
            f.write(final_msg)

        print(f"Feedback saved successfully to {output_path}!")
    except Exception as e:
        print(f"Failed to save feedback: {e}")


def main():
    parser = ArgumentParser(description="A simple Python code evaluation tool.")
    parser.add_argument("-f", "--file", help="Path to the Python file to evaluate.", required=True)
    parser.add_argument("-o", "--output", help="Path to save the detailed feedback.", default=None)
    parser.add_argument("--fix", action="store_true", help="Automatically fix style issues.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()

    script_path = args.file

    if not os.path.exists(script_path):
        print(f"{Colors.FAIL}Error: File '{script_path}' does not exist.{Colors.ENDC}")
        sys.exit(1)

    if args.fix:
        fix_style(script_path, args.debug)

    show_loading()

    feedback = judge_code(script_path, args.debug)
    show_results(feedback)

    if args.output:
        save_feedback_text(feedback, args.output)

if __name__ == "__main__":
    main()
