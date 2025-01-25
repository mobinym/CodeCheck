def is_prime(n):
    if n < 2:
        return "Not prime"
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return "Not prime"
    return "Prime"

if __name__ == "__main__":
    n = int(input())
    print(is_prime(n))
