from pprint import pprint as pp
import math

from codetiming import Timer
from rich import print
from utils import (SESSIONS, get_data)

import PIL

YEAR = 2022
DAY = 12
EXAMPLE = False

# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)


def get_possible_elevations(x: str) -> tuple[str]:
    if x == 'S':
        x = 'a'
    elif x == 'E':
        x = 'z'

    elev = "abcdefghijklmnopqrstuvwxyz"
    if x not in elev:
        raise ValueError('Non è una elevazione valida')

    i = elev.index(x)

    if i == len(elev):
        return tuple(x for x in elev)

    else:
        return tuple(x for x in elev[:i + 2])

def get_possible_neighbors(coords: tuple[int], grid: list[str]) -> list[tuple[int]]:
        y, x = coords
        y_max = len(grid)
        x_max = len(grid[0])
        # print(f"{y=}, {x=}, {y_max=}, {x_max=}")

        su = (y - 1, x) if y != 0 else None
        dx = (y, x + 1) if x != x_max - 1 else None
        giu = (y + 1, x) if y != y_max - 1 else None
        sx = (y, x - 1) if x != 0 else None
        # print(f"{su=}, {dx=}, {giu=}, {sx=}")

        return [t for t in [su, dx, giu, sx] if t]

def find_specific_cell(target: str, grid: list[str]) -> tuple[int]:
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == target:
                return (y, x)

def get_neighbors(coords: tuple[int], grid: list[str]) -> list[tuple[int]]:
    y, x = coords
    neighs = get_possible_neighbors(coords, grid)
    elevs = get_possible_elevations(grid[y][x])

    for n in neighs:
        if grid[n[0]][n[1]] == 'E' and 'z' in elevs:
            elevs = elevs + ('E', )

    return [n for n in neighs if grid[n[0]][n[1]] in elevs]

def dijkstra_fewest_step(grid: list[str], start: tuple[int], end: tuple[int]) -> int:

    edges = {}
    for y in range(len(data)):
        for x in range(len(data[0])):
            edges[(y, x)] = get_neighbors((y, x), data)

    to_visit = {start}
    distance = {start: 0}
    while to_visit:
        current = to_visit.pop()

        if current == end:
            break

        for n in edges[current]:
            next_distance = distance[current] + 1

            if n not in distance or next_distance < distance[n]:
                distance[n] = next_distance
                to_visit.add(n)

    if end in distance:
        return distance[end]
    else:
        return 99999


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: list[str]):

    sol1 = 0
    start = find_specific_cell(grid=data, target='S')
    end = find_specific_cell(grid=data, target='E')

    sol1 = dijkstra_fewest_step(grid=data, start=start, end=end)
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    """
    1135 iterazioni come quella di prima, ci metterà un po'.
    """

    sol2 = 0
    paths = []
    end = find_specific_cell(grid=data, target='E')

    for y in range(len(data)):
        """
        Guardando l'input (la mappa) si ci accorge che l'unico modo per una a arrivare alla E è passare per una b.
        Le b sono soltanto su x = 1, quindi le uniche a che possono arrivare ad E sono quelle su x = 0 e x = 2.
        """
        for x in range(2):
            if data[y][x] == 'a':
                start = (y, x)
                paths.append(dijkstra_fewest_step(grid=data, start=start, end=end))
    sol2 = min(paths)

    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
