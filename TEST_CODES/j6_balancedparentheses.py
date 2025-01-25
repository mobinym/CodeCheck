def is_balanced(s):
    stack = []
    for char in s:
        if char == '(':
            stack.append('(')
        elif char == ')':
            if not stack:
                return "Not balanced"
            stack.pop()
    return "Balanced" if not stack else "Not balanced"

if __name__ == "__main__":
    s = input()
    print(is_balanced(s))
