def find_consecutive(numbers):
    max_consecutive = []
    current_consecutive = []
    for i in range(len(numbers) - 1):
        if numbers[i] + 1 == numbers[i + 1]:
            current_consecutive.append(numbers[i])
        else:
            if current_consecutive:
                current_consecutive.append(numbers[i])
                max_consecutive = max(max_consecutive, current_consecutive, key=len)
            current_consecutive = []
    return max_consecutive

if __name__ == "__main__":
    numbers = list(map(int, input()[1:-1].split(',')))
    print(f"{find_consecutive(numbers)}")
