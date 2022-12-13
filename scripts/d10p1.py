from queue import Queue

EXAMPLE_DATA_1 = """noop
addx 3
addx -5"""

EXAMPLE_DATA_2 = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


cycle = 0
register = None


def add_op(value, state):
    completion_cycle = state["cycle"] + 2
    while state["cycle"] != completion_cycle:
        state = yield
    state["X"] += value
    return


def no_op(state):
    completion_cycle = state["cycle"] + 1
    while state["cycle"] != completion_cycle:
        state = yield
    return


def main():
    instructions = EXAMPLE_DATA_2.split("\n")
    with open("data/d10.txt", "r") as f:
        instructions = f.readlines()

    queue = Queue()
    for line in instructions:
        match line.split():
            case [_, value]:
                queue.put((add_op, int(value)))
            case [_]:
                queue.put((no_op,))
            case _:
                raise RuntimeError

    sum_signal_strength = 0
    state = {"X": 1, "cycle": 1}
    task = None

    while not queue.empty() or task is not None:
        print("*" * 30)
        print(f"State(cycle={state['cycle']}, X={state['X']})")
        if task is None:
            command, *args = queue.get()
            print(f"Starting task: {command.__name__}{tuple(args)}")
            task = command(*args, state=state)
            next(task)

        if (state["cycle"] - 20) % 40 == 0:
            sum_signal_strength += state["cycle"] * state["X"]

        state["cycle"] += 1

        try:
            task.send(state)
        except StopIteration:
            print("Task finished.")
            task = None

        print()

    print("_" * 30)
    print(f"State(cycle={state['cycle']}, X={state['X']})")
    print(f"Summed signal strength: {sum_signal_strength}")


if __name__ == "__main__":
    main()
