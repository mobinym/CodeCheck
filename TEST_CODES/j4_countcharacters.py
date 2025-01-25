from collections import Counter

def count_characters(s):
    counts = Counter(s)
    return ', '.join(f"{char}:{count}" for char, count in counts.items())

if __name__ == "__main__":
    s = input()
    print(count_characters(s))
