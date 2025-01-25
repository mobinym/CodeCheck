def largest(numbers):
    return max(numbers)

if __name__ == "__main__":
    numbers = list(map(int, input().split()))
    print(largest(numbers))
