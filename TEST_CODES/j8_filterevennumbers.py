def filter_even(numbers):
    return [n for n in numbers if n % 2 == 0]

if __name__ == "__main__":
    numbers = list(map(int, input().split()))
    print(" ".join(map(str, filter_even(numbers))))
