def count_odd(numbers):
    return len([n for n in numbers if n % 2 != 0])

if __name__ == "__main__":
    numbers = list(map(int, input().split()))
    print(count_odd(numbers))
