import math

EXAMPLE_DATA = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""


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

    def proj_plus_one(self, other):
        # print(other.unit())
        shadow_mag = self * other.unit()
        # print(shadow_mag)
        dim = int(other.vec[0] == 0)
        dir = 1 if other[dim] > 0 else -1
        proj = Vector(0, 0)
        proj[dim] += dir * shadow_mag
        # print(proj)

        # If we haven't reached the end of the vector, add the remaining 1
        if len(proj) < len(other):
            proj[dim] += dir

        return proj

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

        # # shadow_mag_plus_one = shadow_mag + 1
        # shadow_vec = Vector(0, 0)

        # # Add the shadow of the self vector
        # shadow_vec.vec[dim] += shadow_mag * dir
        # if len(shadow_vec) == len(other):
        #     return shadow_vec, Vector(0, 0)

        # # Add 1
        # shadow_vec.vec[dim] += dir
        # if len(shadow_vec) == len(other):
        #     return shadow_vec, Vector(0, 0)

        # rest_of_vec = other - shadow_vec
        # return shadow_vec, rest_of_vec

        # # If we haven't reached the end of the vector, add one (for the max dist one)
        # if len(shadow_vec) ==
        # shadow_vec.vec[dim] += dir * shadow_mag_plus_one

        # first = shadow_vec
        # second = other - first

        # return first, second

    def __str__(self):
        return f"< {self.vec[0]}, {self.vec[1]} >"


class Rope:
    def __init__(self):
        self.H = Vector(0, 0)
        self.T = Vector(0, 0)
        self.seen = set(((0, 0),))

    def move(self, shift):
        # Splt move into two parts, the first is the move that can be done without the
        # tail moving, and the second is the part that moves the tail

        # Subtract head from tail
        # Find projection of tail onto shift vector
        # Add 1
        # This givs us the portion of the movement vector for which the tail doesn't move
        rT = self.T - self.H
        # first = rT.proj_plus_one(shift)
        # if first == shift:
        #     second = Vector(0, 0)
        # else:
        #     second = shift - first
        first, second = rT.split_vector(shift)

        print(f"Shift: {shift}")
        print(f"First part: {first}")
        print(f"Second part: {second}")
        print()

        # Move head by the full amount
        new_H = self.H + shift

        # Move tail by the second amount
        # Check first if we need to shift tail to a neighboring column or row
        if len(second) != 0:
            shift_dim = int(second[0] == 0)
            non_shift_dim = (1 - shift_dim) % 2

            second_start = self.H + first
            # start = self.T[shift_dim] + first[shift_dim]
            start = second_start[shift_dim]
            end = new_H[shift_dim]
            dir = 1 if second[shift_dim] > 0 else -1
            for i in range(start, end, dir):
                pos = [0, 0]
                pos[non_shift_dim] = new_H[non_shift_dim]
                pos[shift_dim] = i
                self.seen.add(tuple(pos))
                print(f"tail -> {pos}")

            new_T = second_start + (second - second.unit())
        else:
            new_T = self.T

        self.H = new_H
        self.T = new_T

        print()


def main():
    data = EXAMPLE_DATA
    lines = data.split("\n")
    with open("data/d9.txt", "r") as f:
        lines = f.readlines()

    rope = Rope()

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
        print(f"Head: {rope.H}")
        print(f"Tail: {rope.T}")
        print(f"Move: {dir} {mag}")

        rope.move(shift)
        print(f"New Head: {rope.H}")
        print(f"New Tail: {rope.T}")
        print()

    print(sorted(rope.seen))
    print(len(rope.seen))


if __name__ == "__main__":
    main()
