from collections import defaultdict
from functools import reduce

EXAMPLE_DATA = """30373
25512
65332
33549
35390"""


def main():
    """
    Dynamic programming. A tree's
    """
    data = EXAMPLE_DATA
    with open("data/d8.txt", "r") as f:
        data = f.read()
    grid = [[int(height) for height in list(row)] for row in data.split("\n")]
    grid_width, grid_height = len(grid[0]), len(grid)

    visible_trees = {
        (row, col): 1 for row in range(grid_height) for col in range(grid_width)
    }

    # Top
    for col in range(grid_width):
        last_seen = {i: 0 for i in range(10)}
        for row in range(grid_height):
            tree_height = grid[row][col]
            visible_trees[(row, col)] *= row - last_seen[tree_height]
            for i in range(tree_height + 1):
                last_seen[i] = row

    # Bottom
    for col in range(grid_width):
        last_seen = {i: grid_height - 1 for i in range(10)}
        for row in range(grid_height - 1, -1, -1):
            tree_height = grid[row][col]
            visible_trees[(row, col)] *= last_seen[tree_height] - row
            for i in range(tree_height + 1):
                last_seen[i] = row

    # Left
    for row in range(grid_height):
        last_seen = {i: 0 for i in range(10)}
        for col in range(grid_width):
            tree_height = grid[row][col]
            visible_trees[(row, col)] *= col - last_seen[tree_height]
            for i in range(tree_height + 1):
                last_seen[i] = col

    # Right
    for row in range(grid_height):
        last_seen = {i: grid_width - 1 for i in range(10)}
        for col in range(grid_width - 1, -1, -1):
            tree_height = grid[row][col]
            visible_trees[(row, col)] *= last_seen[tree_height] - col
            for i in range(tree_height + 1):
                last_seen[i] = col

    # Compute max scenic score
    print(max(x for x in visible_trees.values()))


if __name__ == "__main__":
    main()
