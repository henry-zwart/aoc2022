import numpy as np

EXAMPLE_DATA = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def make_cave(data):
    """Given a list of lines, create the cave layout as a matrix.

    Adjust the matrix so that the leftmost necessary column is zero rather than 4XX.
    """
    cave_lines = []
    for line in data:
        points = [
            [int(c) for c in str_point.split(",")] for str_point in line.split(" -> ")
        ]
        for s, t in zip(points[:-1], points[1:]):
            cave_lines.append(sorted((s, t)))

    points = set([tuple(point) for line in cave_lines for point in line])
    min_col, *_, max_col = sorted([col for col, _ in points])
    *_, max_row = sorted([row for _, row in points])

    # Allow 1 extra column for sand to fall off cliff
    min_col -= 1
    max_col += 1

    width = (max_col - min_col) + 1
    height = max_row + 1

    cave = np.zeros((height, width))

    # Add in the lines
    for (s_col, s_row), (e_col, e_row) in cave_lines:
        s_col -= min_col
        e_col -= min_col
        cave[s_row : e_row + 1, s_col : e_col + 1] = 1

    return cave, min_col


def drop_sand(cave, pos):
    col, row = pos

    print(f"Sand at: {(col, row)}")

    # If the sand has reached empty ground, return False
    if (cave[row:, col] == 0).all():
        print("Nothing beloowwww.")
        return False

    # Otherwise, compute the next fall position for the sand
    if cave[row + 1, col] == 0:
        print("Can fall straight.")
        new_pos = (col, row + 1)
    elif cave[row + 1, col - 1] == 0:
        print("Can fall left.")
        new_pos = (col - 1, row + 1)
    elif cave[row + 1, col + 1] == 0:
        print("Can fall right.")
        new_pos = (col + 1, row + 1)
    else:
        print("Nowhere to go.")
        new_pos = None

    # If there are no valid fall positions from here, set the current pos to 1 and return True
    if new_pos is None:
        print("Settling.")
        cave[row][col] = 1
        return True

    # Otherwise, recurse
    print("Recursing...", end="\n\n")
    return drop_sand(cave, np.array(new_pos))


def run_sim(cave, offset):
    """Drop sand for as long as it adds to the cave."""

    # Record the sum of the cave walls. We'll subtract this from the final value to figure
    # out how much sand dropped
    initial_sum = cave.sum()

    drop_pos = np.array([500 - offset, 0])

    running = True
    while running:
        # If drop position covered, can't drop sand
        if cave[drop_pos[1]][drop_pos[0]] == 1:
            break

        print(cave)
        print()
        print("Dropping new grain...")
        print()
        sand_rested = drop_sand(cave, drop_pos)
        print()

        if not sand_rested:
            running = False

    new_sum = cave.sum()

    print(new_sum - initial_sum)


def main():
    data = EXAMPLE_DATA.split("\n")

    with open("data/d14.txt", "r") as f:
        data = f.readlines()

    cave, offset = make_cave(data)

    run_sim(cave, offset)


if __name__ == "__main__":
    main()
