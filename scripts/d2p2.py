EXAMPLE_DATA = """A Y
B X
C Z"""

SHAPES = list("ABC")
OUTCOMES = list("XYZ")


def score(yours, desired_outcome):
    mine = SHAPES[(SHAPES.index(yours) + (desired_outcome - 1)) % 3]

    # Calculate the score of the shape, which is the shape index mod 3 + 1
    shape_score = (SHAPES.index(mine) % 3) + 1

    # Calculate the score of the outcome
    # We can frame this as loss=0, draw=1, win=2 (multiplied by 3)
    # Then the outcome score is determined by the mod distance between indexes, + 1
    outcome_score = 3 * ((((SHAPES.index(mine) - SHAPES.index(yours)) + 1) % 3))

    return shape_score + outcome_score


def main():
    with open("data/d2.txt", "r") as f:
        content = f.read().split("\n")

    total_score = sum(score(row[0], OUTCOMES.index(row[2])) for row in content)

    print(total_score)


if __name__ == "__main__":
    main()
