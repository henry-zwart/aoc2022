EXAMPLE_DATA = """30373
25512
65332
33549
35390"""


def main():
    data = EXAMPLE_DATA
    with open("data/d8.txt", "r") as f:
        data = f.read()
    grid = [[int(height) for height in list(row)] for row in data.split("\n")]
    grid_width, grid_height = len(grid[0]), len(grid)

    # Create a set of visible tree indexes. A tree is visible if in the set, assumed not if not.
    # For each direction and each row/column, scan over tree heights, maintaining max seen,
    # and only add trees if they are greater than the max seen.
    visible = set()

    # # Top

    for col in range(grid_width):
        max_seen = -1
        for row in range(grid_height):
            tree_height = grid[row][col]
            if tree_height > max_seen:
                visible.add((row, col))
                max_seen = tree_height

    # Bottom
    for col in range(grid_width):
        max_seen = -1
        for row in range(grid_height - 1, -1, -1):
            tree_height = grid[row][col]
            if tree_height > max_seen:
                visible.add((row, col))
                max_seen = tree_height

    # Left

    for row in range(grid_height):
        max_seen = -1
        for col in range(grid_width):
            tree_height = grid[row][col]
            if tree_height > max_seen:
                visible.add((row, col))
                max_seen = tree_height

    # Right
    for row in range(grid_height):
        max_seen = -1
        for col in range(grid_width - 1, -1, -1):
            tree_height = grid[row][col]
            if tree_height > max_seen:
                visible.add((row, col))
                max_seen = tree_height

    print(len(visible))


if __name__ == "__main__":
    main()
