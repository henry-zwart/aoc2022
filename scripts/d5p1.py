EXAMPLE_DATA = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def main():
    # Load data
    # data = EXAMPLE_DATA
    with open("data/d5.txt", "r") as f:
        data = f.read()

    # Split into initial configuration and moves
    init_config, moves = data.split("\n\n")
    init_config = init_config.split("\n")
    moves = moves.split("\n")

    # Create stacks with initial configuration
    cols = [
        "".join([row[col_idx] for row in init_config])
        for col_idx in range(len(init_config[0]))
    ]
    cols = [col[-2::-1].strip() for col in cols if any(x.isalpha() for x in col)]

    # Execute operations
    for row in moves:
        _, move, _, loc1, _, loc2 = row.split()
        idx1 = int(loc1) - 1
        idx2 = int(loc2) - 1
        move_amt = int(move)

        cols[idx2] += cols[idx1][-1 : -move_amt - 1 : -1]
        cols[idx1] = cols[idx1][:-move_amt]

    print("".join(col[-1] for col in cols))


if __name__ == "__main__":
    main()
