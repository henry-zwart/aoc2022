EXAMPLE_DATA = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def main():
    with open("data/d1p1.txt") as f:
        contents = f.read()

    total_elf_calories = sorted(
        [
            sum(int(x) for x in elf_calories.split("\n"))
            for elf_calories in contents.split("\n\n")
        ],
        reverse=True,
    )

    print(total_elf_calories[0])
    print(sum(total_elf_calories[:3]))


if __name__ == "__main__":
    main()
