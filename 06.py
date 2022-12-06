from pprint import pprint as pp

from codetiming import Timer
from rich import print

from utils import (SESSIONS, get_data, sliding_window)

YEAR = 2022
DAY = 6

def sliding_window(lista: list, length: int) -> list:
    for i in range(0, len(lista) - length + 1):
        yield lista[i:i + length]

#Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=False)


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    """
    We'll iterate every piece of LENGTH, cast into a set and see if the len(set) is LENGTH.
    If it's not, there were non-unique characters in there.
    """
    sol1 = 0
    LENGTH = 4
    for datastream in data:
        for index, window in enumerate(sliding_window(datastream, LENGTH)):
            if len(set(x for x in window)) == LENGTH:
                sol1 = index + LENGTH
                break
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    """
    We'll iterate every piece of LENGTH, cast into a set and see if the len(set) is LENGTH.
    If it's not, there were non-unique characters in there.
    Yes, it's the same as part 1, with a different LENGTH.
    """
    sol2 = 0
    LENGTH = 14
    for datastream in data:
        for index, window in enumerate(sliding_window(datastream, LENGTH)):
            if len(set(x for x in window)) == LENGTH:
                sol2 = index + LENGTH
                break
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

