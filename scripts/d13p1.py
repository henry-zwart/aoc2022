import json

EXAMPLE_DATA = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


def right_order(p1, p2):
    print(f"Comparing {p1} and {p2}")
    for left, right in zip(p1, p2):
        print(f"Checking pairs {left} and {right}")
        # If both are ints, compare directly
        # Otherwise make sure both are lists and recurse
        if any((isinstance(left, list), isinstance(right, list))):
            if type(left) != type(right):
                if isinstance(left, int):
                    left = [left]
                else:
                    right = [right]

            print("Recursing...")
            recursed_result = right_order(left, right)
            if recursed_result is not None:
                return recursed_result

        if left < right:
            return True
        elif left > right:
            return False
        else:
            continue

    # If we haven't returned yet then we got to the end of at least one of the packets
    # If p1 was shorter, return True, if p2, return False, otherwise None
    if len(p1) < len(p2):
        return True
    elif len(p2) < len(p1):
        return False
    else:
        return None


def main():
    data = EXAMPLE_DATA

    with open("data/d13.txt", "r") as f:
        data = f.read()

    str_pairs = data.split("\n\n")
    pairs = [[json.loads(line) for line in pair.split("\n")] for pair in str_pairs]

    correct = [i for i, (p1, p2) in enumerate(pairs, start=1) if right_order(p1, p2)]

    print(correct)
    print(sum(correct))


if __name__ == "__main__":
    main()
