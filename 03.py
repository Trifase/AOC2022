from rich import print

from codetiming import Timer

from utils import SESSIONS, get_data

YEAR = 2022
DAY = 3


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    data = get_data(YEAR, DAY, SESSIONS, example=True)


def get_priority(common_item):
    letters = "0abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return list(letters).index(list(common_item)[0])


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    sol1 = 0
    for rucksack in data:
        common_item = set(rucksack[:(len(rucksack)//2)]).intersection(set(rucksack[(len(rucksack)//2):]))
        priority = get_priority(common_item)
        sol1 += priority
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    sol2 = 0
    for chunk in (data[i:i + 3] for i in range(0, len(data), 3)):
        common_item = set(chunk[0]).intersection(chunk[1], chunk[2])
        priority = get_priority(common_item)
        sol2 += priority
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

