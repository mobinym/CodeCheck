def is_palindromic(n):
    return str(n) == str(n)[::-1]

if __name__ == "__main__":
    n = int(input())
    print(is_palindromic(n))
