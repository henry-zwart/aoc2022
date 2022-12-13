from __future__ import annotations

import math

EXAMPLE_DATA_1 = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

EXAMPLE_DATA_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


class Vector:
    def __init__(self, x, y):
        self.vec = [x, y]

    def move(self, shift):
        self.vec[0] += shift.vec[0]
        self.vec[1] += shift.vec[1]

    def __add__(self, other):
        return Vector(self.vec[0] + other.vec[0], self.vec[1] + other.vec[1])

    def __sub__(self, other):
        return Vector(self.vec[0] - other.vec[0], self.vec[1] - other.vec[1])

    def __mul__(self, other):
        return self.vec[0] * other.vec[0] + self.vec[1] * other.vec[1]

    def __len__(self):
        a = self.vec[0] ** 2
        b = self.vec[1] ** 2
        c = a + b
        return int(math.sqrt(c))
        # return math.sqrt(self.vec[0] ** 2 + self.vec[1] ** 2)

    def __eq__(self, other):
        return all(a == b for a, b in zip(self.vec, other.vec))

    def __getitem__(self, index):
        return self.vec.__getitem__(index)

    def __setitem__(self, index, value):
        return self.vec.__setitem__(index, value)

    def unit(self):
        norm = self.__len__()
        return Vector(int(self.vec[0] / norm), int(self.vec[1] / norm))

    def split_vector(self, other):
        # Splits the vector into two parts such that the first part is the shadow of the vector on the shift, + 1
        dim = int(other.vec[0] == 0)
        dir = int(other.vec[dim] / abs(other.vec[dim]))
        shadow_mag_plus_1 = (self * other.unit()) + 1

        if shadow_mag_plus_1 >= len(other):
            first = other
            second = Vector(0, 0)
        else:
            first_mag = shadow_mag_plus_1
            second_mag = len(other) - first_mag
            first = Vector(0, 0)
            first.vec[dim] = dir * first_mag
            second = Vector(0, 0)
            second.vec[dim] = dir * second_mag

        return first, second

    def __str__(self):
        return f"[{self.vec[0]}, {self.vec[1]}]"


class Knot:
    def __init__(self, child: Knot, pos: Vector, knot_id: int):
        self.child = child
        self.pos = pos
        self.knot_id = knot_id
        self.seen = set(((0, 0),))

    def move_step_to(self, new_pos: Vector):
        shift_vector = new_pos - self.pos

        print(
            f"{self.knot_id}: Moving knot ({self.pos} -> {new_pos}) via {shift_vector}."
        )

        self.pos = new_pos
        self.seen.add(tuple(self.pos.vec))

        if self.child is None:
            print(f"{self.knot_id}: Knot is tail, bottoming out.")
            return

        print(f"{self.knot_id}: Knot not tail.")
        if len(self.child.pos - self.pos) < 2:
            print(f"{self.knot_id}: Child close enough.")
            return

        else:
            print(f"{self.knot_id}: Child too far, shifting...")
            diff = self.pos - self.child.pos
            signs = [int(x / abs(x)) if x != 0 else 0 for x in diff]

            # Either moving in line with child or off-line
            # If in-line, will have one dimension with diff = +-2, move 1 step in that dir
            # If off-line, will have one dim with diff = +-2 and another with diff = +-1
            child_shift = Vector(0, 0)
            for i, s in enumerate(signs):
                child_shift[i] = s

            new_child_pos = self.child.pos + child_shift
            self.child.move_step_to(new_child_pos)
            return


class Rope:
    def __init__(self, knots: int):
        self.T = Knot(child=None, pos=Vector(0, 0), knot_id=knots)

        current_knot = self.T
        for i in range(knots - 1, 0, -1):
            new_knot = Knot(child=current_knot, pos=Vector(0, 0), knot_id=i)
            current_knot = new_knot

        self.H = current_knot

    def move(self, shift):
        # Split into components of length 1 and apply iteratively
        dim = 0 if shift.vec[0] != 0 else 1
        dir = -1 if shift.vec[dim] < 0 else 1
        one_step_shift = Vector(0, 0)
        one_step_shift.vec[dim] = dir
        n_steps = len(shift)

        for _ in range(n_steps):
            new_head_pos = self.H.pos + one_step_shift
            self.H.move_step_to(new_head_pos)


def main():
    data = EXAMPLE_DATA_2
    lines = data.split("\n")
    with open("data/d9.txt", "r") as f:
        lines = f.readlines()

    rope = Rope(knots=10)

    for i, line in enumerate(lines):
        dir, mag = line.split(" ")
        mag = int(mag)
        match dir:
            case "U":
                shift = Vector(0, mag)
            case "D":
                shift = Vector(0, -mag)
            case "L":
                shift = Vector(-mag, 0)
            case "R":
                shift = Vector(mag, 0)

        print("*" * 10 + f" {i}")
        print(f"Head: {rope.H.pos}")
        print(f"Tail: {rope.T.pos}")
        print(f"Move: {dir} {mag}")

        rope.move(shift)
        print(f"New Head: {rope.H.pos}")
        print(f"New Tail: {rope.T.pos}")
        print()

    print(len(rope.T.seen))


if __name__ == "__main__":
    main()
