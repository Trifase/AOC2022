from codetiming import Timer
from rich import print
from dataclassy import dataclass
from utils import (SESSIONS, get_data, MovingThing)

from typing import Self

YEAR = 2022
DAY = 16
EXAMPLE = True

@dataclass
class Valve:
    name: str
    flow: int
    children: list[Self]


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line beacon_y line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    valves = []
    v = {}
    for line in data:
        line = line.split(';')
        name, flow = line[0].split('=')
        name = name[6:8]
        children = line[1].split(' ', maxsplit=5)[-1].split(',')
        children = [child.strip() for child in children]
        valves.append(Valve(name=name, flow=int(flow), children=children))
        v[name] = Valve(name=name, flow=int(flow), children=children)
    data = valves, v

# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    def get_neighbors(valve, data):
        return valve.children


    valves, v = data
    print("valves")
    print(valves)
    non_zero_valves = [v for v in valves if v.name == 'AA']
    non_zero_valves.extend([v for v in valves if v.flow])
    print("Non zero Valves")
    print(non_zero_valves)
    sol1 = 0
    edges = {}
    for valve in valves:
        edges[valve.name] = get_neighbors(valve, valves)
    print("edges")
    print(edges)
    print("v")
    print(v)
    start = 'AA'
    all_distances = {}
    for start in [v.name for v in non_zero_valves]:
        for end in [v.name for v in non_zero_valves]:
            to_visit = {start}
            distance = {start: 0}
            source = {start: None}

            while to_visit:
                current = to_visit.pop()

                for n in edges[current]:
                    next_distance = distance[current] + 1

                    if n not in distance or next_distance < distance[n]:
                        distance[n] = next_distance
                        source[n] = current
                        to_visit.add(n)



            if end in distance:
                if start not in all_distances:
                    all_distances[start] = {}
                all_distances[start][end] = distance[end]

    print(all_distances)
    print(sorted(non_zero_valves, key=lambda x: x.flow, reverse=True))
    print("===========")
    start = 'AA'
    print(all_distances[start])
    unsorted_list = [(v[x].flow - all_distances[start][x], x) for x in all_distances[start]]

    print(sorted(unsorted_list, key=lambda element: (element[0], element[1]), reverse=True))
    # print([v[x].flow - all_distances[start][x] for x in all_distances[start]])


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data) -> int:
    sol2 = 0

    return sol2


s1 = part1(data)
s2 = part2(data)


print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
