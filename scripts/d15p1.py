import re

EXAMPLE_DATA = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


def X_(point):
    return point[0]


def Y_(point):
    return point[1]


def parse(inp):
    pat = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    return [list(map(int, pat.search(line).groups())) for line in inp.split("\n")]


def manhatten(p1, p2):
    return abs(X_(p1) - X_(p2)) + abs(Y_(p1) - Y_(p2))


# def covered_cells(records, Y):
#     covered = set()
#     known_Xs = set()

#     for sX, sY, bX, bY in records:
#         d = manhatten((sX, sY), (bX, bY))
#         dy = abs(sY - Y)
#         dx = d - dy
#         x_min, x_max = sX - dx, sX + dx
#         for i in range(x_min, x_max + 1):
#             covered.add(i)

#         if bY == Y:
#             known_Xs.add(bX)
#         elif sY == Y:
#             known_Xs.add(sX)

#     return covered - known_Xs


def covered_cells(records):
    coverings = dict()

    for sX, sY, bX, bY in records:
        d = manhatten((sX, sY), (bX, bY))

        for dy in range(-d, d + 1):
            dx = d - abs(dy)
            x_min = sX - dx
            x_max = sX + dx
            y = sY + dy

            if y not in coverings:
                coverings[y] = []

            # Find first and last ranges which overlap with target
            overlapping = [
                i
                for i, (ox_min, ox_max) in enumerate(coverings[y])
                if not any((x_max < ox_min, ox_max < x_min))
            ]
            if overlapping:
                min_i = overlapping[0]
                max_i = overlapping[-1]

                new_range = (
                    min(x_min, coverings[y][min_i][0]),
                    max(x_max, coverings[y][max_i][1]),
                )
                coverings[y] = (
                    coverings[y][:min_i] + [new_range] + coverings[y][max_i + 1 :]
                )
            else:
                coverings[y].append((x_min, x_max))

    return coverings


def main():
    Y = 10
    data = EXAMPLE_DATA

    Y = 2000000
    with open("data/d15.txt", "r") as f:
        data = f.read()

    records = parse(data)
    coverings = covered_cells(records)

    beacon_Xs = {bX for *_, bX, bY in records if bY == Y}
    # eliminated_ranges = set(coverings[Y]) - beacon_Xs
    print(sum(x_max - x_min for x_min, x_max in coverings[Y]))
    # print(len(covered_cells(records, Y)))


if __name__ == "__main__":
    main()
