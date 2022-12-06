from functools import reduce

EXAMPLE_DATA = [
    """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg""",
    """wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""",
]


def p(c):
    # Conditional on case, prio is index of letter, starting at 1
    # Upper-case letters start from 27.
    base_prio = (ord(c.lower()) - ord("a")) + 1
    return base_prio + 26 * (c.upper() == c)


def key(group):
    # Make a set of each rucksack's elements, reduce using set intersection
    return reduce(set.__and__, map(set, group)).pop()


def main():
    # groups = [g.split("\n") for g in EXAMPLE_DATA]
    with open("data/d3.txt", "r") as f:
        lines = f.read().split("\n")
        groups = [lines[i : i + 3] for i in range(0, len(lines), 3)]

    sum_total = sum([p(key(group)) for group in groups])

    print(sum_total)


if __name__ == "__main__":
    main()
