EXAMPLE_DATA = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def p(c):
    # Conditional on case, prio is index of letter, starting at 1
    # Upper-case letters start from 27.
    base_prio = (ord(c.lower()) - ord("a")) + 1
    return base_prio + 26 * (c.upper() == c)


def main():
    # rows = EXAMPLE_DATA.split("\n")
    with open("data/d3.txt", "r") as f:
        rows = f.readlines()

    rucksacks = [(row[: int(len(row) / 2)], row[int(len(row) / 2) :]) for row in rows]

    sum_total = sum(
        [sum((p(c) for c in (set(first) & set(second)))) for first, second in rucksacks]
    )

    print(sum_total)


if __name__ == "__main__":
    main()
