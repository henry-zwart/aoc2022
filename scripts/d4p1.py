import re

EXAMPLE_DATA = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def main():
    # rows = EXAMPLE_DATA

    with open("data/d4.txt", "r") as f:
        rows = f.read()

    pattern = r"(\d+)-(\d+),(\d+)-(\d+)"
    matches = [tuple(map(int, m)) for m in re.findall(pattern, rows)]

    count = sum((s1 - s2) * (e1 - e2) <= 0 for (s1, e1, s2, e2) in matches)

    print(count)


if __name__ == "__main__":
    main()
