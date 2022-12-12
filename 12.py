from pprint import pprint as pp
import math

from codetiming import Timer
from rich import print
from utils import (SESSIONS, get_data)

from PIL import Image
import random

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

def get_neighbors(coords: tuple[int], grid: list[str]) -> tuple[tuple[int]]:
    y, x = coords
    neighs = get_possible_neighbors(coords, grid)
    elevs = get_possible_elevations(grid[y][x])

    for n in neighs:
        if grid[n[0]][n[1]] == 'E' and 'z' in elevs:
            elevs = elevs + ('E', )

    return tuple(n for n in neighs if grid[n[0]][n[1]] in elevs)

def dijkstra_fewest_steps(grid: list[str], start: tuple[int], end: tuple[int]) -> int:

    edges = {}
    for y in range(len(data)):
        for x in range(len(data[0])):
            edges[(y, x)] = get_neighbors((y, x), data)

    to_visit = {start}
    distance = {start: 0}
    source = {start: None}
    while to_visit:
        current = to_visit.pop()

        if current == end:
            break

        for n in edges[current]:
            next_distance = distance[current] + 1

            if n not in distance or next_distance < distance[n]:
                distance[n] = next_distance
                source[n] = current
                to_visit.add(n)

    path = []
    v = source[end]

    while v != start:
        path.append(v)
        v = source[v]

    if end in distance:
        return [distance[end], path]
    else:
        return [99999, 99999]

# Viz
def draw_map(grid: list[str], gif=False):

    elev = {
        "S": (0, 0, 0),
        "E": (0, 0, 0),
        "a": (59,118,77),
        "b": (61,128,31),
        "c": (65, 144, 27),
        'd': (62, 128, 31),
        'e': (81, 148, 29),
        'f': (81, 148, 29),
        'g': (106, 152, 31),
        'h': (106, 152, 31),
        'i': (130, 153, 34),
        'j': (130, 153, 34),
        'k': (146, 153, 37),
        'l': (146, 153, 37),
        'm': (141, 137, 39),
        'n': (141, 137, 39),
        'o': (113, 100, 39),
        'p': (113, 100, 39),
        'q': (91, 76, 49),
        'r': (91, 76, 49),
        's': (108, 96, 87),
        't': (108, 96, 87),
        'u': (150, 146, 144),
        'v': (150, 146, 144),
        'w': (173, 173 ,173),
        'x': (173, 173 ,173),
        'y': (225, 225, 225),
        'z': (225, 225, 225)
    }

    start = find_specific_cell(grid=data, target='S')
    end = find_specific_cell(grid=data, target='E')
    
    path = dijkstra_fewest_steps(grid=data, start=start, end=end)[1]
    im = Image.new(mode="RGB", size=(len(grid[0]), len(grid)))

    pixels = im.load()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            c = elev[grid[y][x]]
            nc = tuple(x+random.randint(-2, +2) for x in c)
            pixels[x, y] = nc

    if gif:
        im.save(f"viz/day{DAY}-000.png")

    i = 0
    for p in path[::-1]:
        pixels[p[1], p[0]] = (220, 0, 0)
        if gif:

            im.save(f"viz/day{DAY}-{i}.png")

            i += 1

    if not gif:
        im.save(f"viz/day{DAY}.png")


def draw_map_p2(grid: list[str], gif=False, paths=None):

    elev = {
        "S": (0, 0, 0),
        "E": (0, 0, 0),
        "a": (59,118,77),
        "b": (61,128,31),
        "c": (65, 144, 27),
        'd': (62, 128, 31),
        'e': (81, 148, 29),
        'f': (81, 148, 29),
        'g': (106, 152, 31),
        'h': (106, 152, 31),
        'i': (130, 153, 34),
        'j': (130, 153, 34),
        'k': (146, 153, 37),
        'l': (146, 153, 37),
        'm': (141, 137, 39),
        'n': (141, 137, 39),
        'o': (113, 100, 39),
        'p': (113, 100, 39),
        'q': (91, 76, 49),
        'r': (91, 76, 49),
        's': (108, 96, 87),
        't': (108, 96, 87),
        'u': (150, 146, 144),
        'v': (150, 146, 144),
        'w': (173, 173 ,173),
        'x': (173, 173 ,173),
        'y': (225, 225, 225),
        'z': (225, 225, 225)
    }
    paths = []
    end = find_specific_cell(grid=data, target='E')
    all_paths = []
    for y in range(len(data)):

        for x in range(2):
            if data[y][x] == 'a':
                start = (y, x)
                results = dijkstra_fewest_steps(grid=data, start=start, end=end)
                paths.append(results[0])
                all_paths.append(results[1])

    im = Image.new(mode="RGBA", size=(len(grid[0]), len(grid)))

    pixels = im.load()
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            c = elev[grid[y][x]]
            nc = tuple(x+random.randint(-2, +2) for x in c)
            pixels[x, y] = nc

    if gif:
        im.save(f"viz/day{DAY}-p2--000.png")

    i = 0
    for path in all_paths:
        for p in path[::-1]:
            pixels[p[1], p[0]] = (255, 0, 0, 127)
            if gif:

                im.save(f"viz/day{DAY}-p2-{i}.png")

                i += 1

    if not gif:
        im.save(f"viz/day{DAY}-p2.png")


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: list[str]):

    sol1 = 0
    start = find_specific_cell(grid=data, target='S')
    end = find_specific_cell(grid=data, target='E')

    sol1 = dijkstra_fewest_steps(grid=data, start=start, end=end)[0]
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
    all_paths = []
    for y in range(len(data)):
        """
        Guardando l'input (la mappa) si ci accorge che l'unico modo per una a arrivare alla E è passare per una b.
        Le b sono soltanto su x = 1, quindi le uniche a che possono arrivare ad E sono quelle su x = 0 e x = 2.
        """
        for x in range(2):
            if data[y][x] == 'a':
                start = (y, x)
                results = dijkstra_fewest_steps(grid=data, start=start, end=end)
                paths.append(results[0])
                all_paths.append(results[1])
    sol2 = min(paths)

    return sol2


s1 = part1(data)
s2 = part2(data)

# Viz
# draw_map(data)
# draw_map_p2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
