from rich import print

from codetiming import Timer

from utils import SESSIONS, get_data

YEAR = 2022
DAY = 1


def split_list(list):
    l = []
    for y in '\n'.join(list).split('\n\n'):
        l.append([x for x in y.split('\n')])
    return l


# Input Parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=False) 
    data = split_list(data)


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    sol1 = 0
    sol1 = max([sum([int(x) for x in elf]) for elf in data])
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    sol2 = 0
    sol2 = sum(sorted([sum([int(x) for x in elf]) for elf in data], reverse=True)[:3])
    return sol2


s1 = part1(data)
s2 = part2(data)

print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

