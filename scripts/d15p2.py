import math
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


def check_row_for_gaps(row, _minx, _maxx):
    row = sorted([x for x in row if x is not None], key=lambda x: (x[0], -x[1]))

    if row[0][0] > _minx:
        return _minx

    max_seen = row[0][1]

    for start, end, _ in row[1:]:
        if start > max_seen + 1:
            return max_seen + 1
        max_seen = max(max_seen, end)
        if max_seen >= _maxx or end >= _maxx:
            break

    return None


def find_unknown_cell(sensor_beacon_pairs, _max=20):
    d = [manhatten((sX, sY), (bX, bY)) for (sX, sY, bX, bY) in sensor_beacon_pairs]
    reach = [
        (
            sY - d[i],
            sY + d[i],
        )
        for i, (_, sY, *_) in enumerate(sensor_beacon_pairs)
    ]

    prev_row = [None] * len(sensor_beacon_pairs)

    for row_index in range(_max + 1):

        for i, (sX, sY, *_) in enumerate(sensor_beacon_pairs):
            if not (reach[i][0] <= row_index <= reach[i][1]):
                prev_row[i] = None
                continue

            if prev_row[i] is None:
                dy = abs(row_index - sY)
                dx = d[i] - dy
                prev_row[i] = [sX - dx, sX + dx, 1]

            else:
                start, end, w = prev_row[i]
                prev_row[i][0] = start - w
                prev_row[i][1] = end + w
                if sY == row_index:
                    prev_row[i][2] = -1

        if cell_x := check_row_for_gaps(prev_row, 0, _max):
            return (cell_x, row_index)


def main():
    data = EXAMPLE_DATA

    with open("data/d15.txt", "r") as f:
        data = f.read()

    records = parse(data)
    records = sorted(records, key=lambda x: (x[1], x[3]))
    for (sX, sY, bX, bY) in records:
        print(f"S({sX}, {sY}), B({bX}, {bY}), d={manhatten((sX, sY), (bX, bY))}")
    x, y = find_unknown_cell(records, _max=int(4e6))
    print(x * 4e6 + y)


if __name__ == "__main__":
    main()
