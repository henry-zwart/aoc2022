import heapq
import math

EXAMPLE_DATA = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

ALPHA = "abcdefghijklmnopqrstuvwxyz"


class State:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val
        if val == "S":
            val = "a"
        elif val == "E":
            val = "z"
        self.height = ALPHA.find(val.lower())

    def __hash__(self):
        return hash((self.row, self.col, self.val))

    def __str__(self):
        return f"State(({self.row}, {self.col}), Val={self.val}, Height={self.height})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.val == other.val


class Node:
    def __init__(self, state, dist, parent=None):
        self.state = state
        self.dist = dist
        self.parent = parent

    def __hash__(self):
        return hash(self.state)

    def neighbors(self, map):
        n = []
        row, col = self.state.row, self.state.col

        for i in range(0, 360, 90):
            new_row = row + int(math.sin(i * math.pi / 180))
            new_col = col + int(math.cos(i * math.pi / 180))

            # If we're out of bounds, skip
            if any((new_row < 0, new_col < 0)):
                continue
            elif any((new_row == len(map), new_col == len(map[0]))):
                continue

            new_state = State(new_row, new_col, map[new_row][new_col])

            # If the new state has height more than 1 greater than current, skip
            if new_state.height - 1 > self.state.height:
                continue

            # Otherwise add to list of neighbors
            n.append(new_state)

        return n

    def __str__(self):
        return f"Node(State={self.state}, Dist={self.dist}"

    def __repr__(self):
        return str(self)


def find_terminals(map):
    start = end = None
    for row_idx, row in enumerate(map):
        for col_idx, val in enumerate(row):
            if val == "S":
                start = State(row_idx, col_idx, val)
            elif val == "E":
                end = State(row_idx, col_idx, val)

    return start, end


def main():
    data = EXAMPLE_DATA
    with open("data/d12.txt", "r") as f:
        data = f.read()

    map = data.split("\n")

    start_pos, end_pos = find_terminals(map)
    I = Node(start_pos, 0)

    closed = set()
    openlist = {I.state: I}

    counter = 0

    while openlist:
        # Find node with minimum distance
        min_dist = math.inf

        for state, node in openlist.items():
            if node.dist < min_dist:
                min_dist_state = state
                min_dist = node.dist

        # Pop the node
        node = openlist.pop(min_dist_state)

        print(f"Popped node {node}.")

        # Compute neighbors
        neighbors = node.neighbors(map)
        print(f"Found neighbors {neighbors}")
        for state in neighbors:
            if state in closed:
                print(f"State already in closed list: {state}")
                continue

            neighbor_node = Node(state, node.dist + 1, parent=node)
            if state in openlist:
                print(f"State found in open list: {state}")
                if openlist[state].dist <= neighbor_node.dist:
                    print(
                        f"New node distance not better ({openlist[state].dist} vs. {neighbor_node.dist})"
                    )
                    continue

            print(f"Adding node to open list: {neighbor_node}")
            openlist[state] = neighbor_node

        closed.add(node.state)

        print(openlist)

        print()

        if node.state == end_pos:
            goal_node = node
            break

        counter += 1

        # if counter == 3:
        #     break

    print(goal_node.dist)
    path = []
    cur = goal_node
    while cur is not None:
        path.append(cur.state)
        cur = cur.parent
    path = reversed(path)
    for state in path:
        print(state)


if __name__ == "__main__":
    main()
