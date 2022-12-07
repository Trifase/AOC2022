from pprint import pprint as pp
import random

from codetiming import Timer
from rich import print

from dataclassy import dataclass
from utils import (SESSIONS, get_data, sliding_window)

YEAR = 2022
DAY = 7

@dataclass
class FileDir:
    name: str
    size: int = 0
    children: dict = {}
    type: str

    subdirectories = []

    def total_size(self):
        if self.type == 'file':
            return self.size
        else:
            total_size = sum([child.total_size() for child in self.children.values()])
            # print(f"{self.name} ({self.type}) · {total_size}")
            return total_size


@dataclass
class Dir(FileDir):
    type: str = 'dir'

@dataclass
class File(FileDir):
    type: str = 'file'


def populate_with_dir_under_limit(d: dict, obj: Dir, limit: int):
    if obj.type == 'dir':
        size = obj.total_size()
        if size <= limit:
            name = f"{obj.name}_{random.randint(0, 999)}"
            d[name] = size
        for child in obj.children.values():
            populate_with_dir_under_limit(d, child, limit)
    return d

def populate_with_dir_over_limit(d: dict, obj: Dir, limit: int):
    if obj.type == 'dir':
        size = obj.total_size()
        if size >= limit:
            name = f"{obj.name}_{random.randint(0, 999)}"
            d[name] = size
        for child in obj.children.values():
            populate_with_dir_over_limit(d, child, limit)
    return d

#Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=False)
    
    root = Dir(name='/')
    paths = [root]

    for line in data[1:]:
        if line.startswith('$'):  # è un comando
            match line.split()[1]:
                case 'cd':  # cambio directory
                    if line.split()[2] == '..':  # si va su
                        paths.pop()
                    else:  # si entra in directory
                        paths.append(paths[-1].children[line.split()[2]])
                        pass
                case 'ls':  # list
                    pass

        elif line.startswith('dir'):  # è una dir
            paths[-1].children[line.split()[1]] = Dir(name=line.split()[1])

        else:  # è un file
            paths[-1].children[line.split()[1]] = File(name=line.split()[1], size=int(line.split()[0]))

    data = paths[0]



# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    sol1 = 0

    d = {}
    newd = populate_with_dir_under_limit(d, data, 100000)
    sol1 = sum(x for x in newd.values())

    return sol1



# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):

    sol2 = 0
    data: FileDir

    TOTAL_FS = 70000000
    SPACE_NEEDED = 30000000

    total_occupied_space = data.total_size()
    free_space_required = SPACE_NEEDED - (TOTAL_FS - total_occupied_space)

    d = {}
    newd = populate_with_dir_over_limit(d, data, free_space_required)
    sol2 = sorted(newd.values())[0]

    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
