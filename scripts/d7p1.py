import re
from queue import Queue

EXAMPLE_DATA = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


class Directory:
    def __init__(self, name, parent=None, is_root=False):
        self.name = name
        self.parent = parent
        self.subdirectories = {}
        self.files = {}
        self.root = self if is_root else None

    def __getitem__(self, name):
        if name in self.subdirectories:
            return self.subdirectories[name]
        elif name in self.files:
            return self.files[name]
        else:
            raise KeyError(f"Item {name} not found in directory {self.path}")

    def add_file(self, file):
        if file.name in self.files:
            raise RuntimeError(
                f"File {file.name} already exists in directory {self.path}"
            )
        file.parent = self
        self.files[file.name] = file

    def mkdir(self, dir):
        if dir.name in self.subdirectories:
            raise RuntimeError(
                f"Subdirectory {dir.name} already exists in directory {self.path}"
            )
        dir.parent = self
        dir.root = self.root
        self.subdirectories[dir.name] = dir

    @property
    def path(self):
        p = []

        temp_dir = self
        while temp_dir.parent is not None:
            p.append(temp_dir.name)
            temp_dir = temp_dir.parent

        return "/" + "/".join(reversed(p))

    @property
    def size(self):
        files_size = sum(f.size for f in self.files.values())
        if self.subdirectories:
            dirs_size = sum(dir.size for dir in self.subdirectories.values())
        else:
            dirs_size = 0
        return files_size + dirs_size


class File:
    def __init__(self, name, size, parent=None):
        self.name = name
        self.size = size
        self.parent = parent


# Command pattern looks for a line starting with $, followed by either cd or ls, and
#   potentially an argument, then possibly followed by a number of lines with stdout
#   which do not contain a $.
command_pattern = re.compile(
    r"\$ (?P<command>cd|ls) ?(?P<arg>[^\n]+)?\n(?P<stdout>[^\$]+)?\n?"
)

# Stdout pattern looks for lines in the stdout capture group from command pattern,
#   which are split into two parts, either (size name) or (directory name), depending
#   on whether they are a file or a directory.
stdout_pattern = re.compile(r"(?:(?P<size>\d+)|(?P<directory>dir)) (?P<name>[^\n]+)")


def execute_cd(target, pwd):
    match target:
        case "/":
            pwd = pwd.root
        case "..":
            pwd = pwd.parent
        case _:
            pwd = pwd[target]

    return pwd


def execute_ls(stdout, pwd):
    stdout = stdout.split("\n")

    for line in stdout:
        m = stdout_pattern.match(line)
        if m is None:
            continue
        is_directory = m.group("directory") == "dir"
        size = int(m.group("size")) if not is_directory else None
        name = m.group("name")

        match is_directory:
            case True:
                pwd.mkdir(Directory(name))
            case False:
                pwd.add_file(File(name, size))

    return pwd


def process_command(command, arg, stdout, pwd):
    match command:
        case "cd":
            pwd = execute_cd(arg, pwd)
        case "ls":
            pwd = execute_ls(stdout, pwd)

    return pwd


def main():
    """
    Strategy:
        1. Split into commands
        2. Commands are either cd or ls
        3. If cd, either goes to home, parent, or child
        4. If ls, lists
    """

    data = EXAMPLE_DATA

    with open("data/d7.txt") as f:
        data = f.read()

    commands = command_pattern.finditer(data)

    root = Directory("/", parent=None, is_root=True)
    pwd = root

    # Create directory structure
    for m in commands:
        command = m.group("command")
        arg = m.group("arg")
        stdout = m.group("stdout")
        if stdout is None:
            stdout = ""
        pwd = process_command(command, arg, stdout, pwd)

    # Traverse directory structure and print directory size for each directory
    queue = Queue()
    queue.put(root)
    at_most_100k = []
    while not queue.empty():
        dir = queue.get()
        if dir.size <= 1e5:
            at_most_100k.append(dir)
        for subdir in dir.subdirectories.values():
            queue.put(subdir)

    print(sum(dir.size for dir in at_most_100k))


if __name__ == "__main__":
    main()
