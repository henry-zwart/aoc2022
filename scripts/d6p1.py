EXAMPLE_DATA = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]


def main(stream, n):
    cycle = list(stream[:n])
    cycle_chars = dict()
    for c in cycle:
        cycle_chars[c] = cycle_chars.get(c, 0) + 1

    for i, char in enumerate(stream[n:], start=n):
        if len(cycle_chars) == n:
            break
        cycle_idx = i % n

        # Remove oldest elt
        oldest_elt = cycle[cycle_idx]
        cycle_chars[oldest_elt] -= 1
        if cycle_chars[oldest_elt] == 0:
            del cycle_chars[oldest_elt]

        # Add new elt
        cycle[cycle_idx] = char
        cycle_chars[char] = cycle_chars.get(char, 0) + 1

    print(i)


if __name__ == "__main__":
    # for stream in EXAMPLE_DATA:
    #     main(stream, 4)
    # print()
    # for stream in EXAMPLE_DATA:
    #     main(stream, 14)
    with open("data/d6.txt", "r") as f:
        stream = f.read()
    main(stream, n=4)
    main(stream, n=14)
