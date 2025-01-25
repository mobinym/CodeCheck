def is_strange_number(n):
    return n % 3 == 0 and n % 6 != 0

if __name__ == "__main__":
    n = int(input())
    print(is_strange_number(n))
