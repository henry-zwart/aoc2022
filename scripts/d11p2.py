import operator
import re
from queue import Queue

EXAMPLE_DATA = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""


operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


class Monkey:
    def __init__(self, id):
        self.id = id
        self.queue = Queue()
        self.throw_to = None
        self.inspected = 0
        self.mod = 9699690

    def has_items(self):
        return not self.queue.empty()

    def grab(self, x):
        print(self.mod)
        return self.queue.put(x % self.mod)

    def throw(self):
        x = self.queue.get()
        # print(f"Monkey inspects an item with a worry level of {x}.")
        initial_worry = self.op(x)
        # reduced_worry = self.reduce(initial_worry)
        # print(f"New worry level: {initial_worry}")
        # revised_worry = initial_worry // 3
        # print(f"Worry level divided by 3 to {revised_worry}")
        target_monkey = self.throw_to[self.test(initial_worry)]
        # print(
        #     f"Item with worry level {initial_worry} is thrown to monkey {target_monkey.id}"
        # )
        target_monkey.grab(initial_worry)
        self.inspected += 1
        return

    def add_op(self, x, op_str, y):
        op = operators[op_str]
        if op_str == "+":
            if x == y:
                self.op = lambda a: (a + a)
            else:
                self.op = lambda a: (a + int(y))

        else:
            if x == y:
                self.op = lambda a: (a * a)
            else:
                self.op = lambda a: (a * (int(y) % self.mod))

    def add_test(self, test_divide_num):
        self.test_divide_num = test_divide_num

    def op(self, old):
        ...

    def test(self, worry):
        return worry % self.test_divide_num == 0


def parse_data(data):
    items_pat = re.compile(r"Starting items: (.*)")
    op_pat = re.compile(r"Operation: (.*)")
    test_pat = re.compile(r"Test: divisible by (\d+)")
    throw_pat = re.compile(r"If (true|false): throw to monkey (\d+)")

    monkeys = []

    split_data = data.split("\n\n")
    for i, monkey_data in enumerate(split_data):
        monkeys.append(Monkey(i))

    for monkey_data, monkey in zip(split_data, monkeys):
        lines = [x.strip() for x in monkey_data.split("\n")]

        # Monkey-patch test
        test_divide_num = int(test_pat.search(lines[3]).group(1))
        monkey.add_test(test_divide_num)

        # Monkey-patch operator
        op_str = op_pat.search(lines[2]).group(1)
        (x, op_str, y) = op_str.split()[2:]
        monkey.add_op(x, op_str, y)

        # print(monkey.op(10))

        # Add throw_targets
        monkey.throw_to = {
            True: monkeys[int(throw_pat.search(lines[4]).group(2))],
            False: monkeys[int(throw_pat.search(lines[5]).group(2))],
        }

        # Extract items
        items = [
            int(x) for x in items_pat.search(lines[1]).group(1).strip().split(", ")
        ]
        for item in items:
            monkey.grab(item)

    # for monkey in monkeys:
    #     print(monkey.id)
    #     print(monkey.throw_to[True].id)
    #     print(monkey.throw_to[False].id)
    #     print()

    return monkeys


def main():
    data = EXAMPLE_DATA
    with open("data/d11.txt", "r") as f:
        data = f.read()
    monkeys = parse_data(data)

    for round in range(10000):
        # print("*" * 30)
        print(f"Round: {round}")
        throws = 0
        for monkey in monkeys:
            # print(f"Monkey: {monkey.id}")
            while monkey.has_items():
                # print("Throwing.")
                monkey.throw()
                throws += 1
            #     print()
            # print()
        print(f"Throws: {throws}")

        # print()

    for monkey in monkeys:
        print(f"Monkey: {monkey.id}, Inspected: {monkey.inspected}")

    sorted_inspected = sorted([m.inspected for m in monkeys], reverse=True)
    print(f"Monkeyness: {sorted_inspected[0] * sorted_inspected[1]}")


if __name__ == "__main__":
    main()
