def average(numbers):
    return sum(numbers) / len(numbers)

if __name__ == "__main__":
    numbers = list(map(int, input().split()))
    print(f"{average(numbers):.2f}")
