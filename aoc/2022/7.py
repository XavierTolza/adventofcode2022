import os
from os.path import abspath, normpath
from pathlib import Path

import numpy as np

demo_data = """$ cd /
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

demo_result = 95437, 24933642


def main(data_str, maxsize=100000):
    # Get tree
    cwd = Path(normpath("/")).absolute()
    folder_sizes = {}
    for line in data_str.split("\n"):
        if "$ cd" in line:
            cwd = Path(os.path.abspath(str(cwd / line[5:])))
        else:
            try:
                size = int(line.split(" ")[0])
            except Exception:
                continue
            else:
                for path in [cwd] + list(cwd.parents):
                    path = path.absolute()
                    folder_sizes[str(path)] = folder_sizes.get(str(path), 0) + size

    # Part one
    res1 = sum(i for i in folder_sizes.values() if i < maxsize)

    # Part two
    used = folder_sizes[abspath("/")]
    total = 70000000
    required = 30000000
    available = total - used
    to_free = required - available

    data = np.sort(np.array(list(folder_sizes.values())))
    index = np.nonzero(data > to_free)[0]
    res2 = data[index][0]

    return res1, res2
