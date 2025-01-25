def sum_positive(numbers):
    return sum(n for n in numbers if n > 0)

if __name__ == "__main__":
    numbers = list(map(int, input()[1:-1].split(',')))
    print(sum_positive(numbers))
