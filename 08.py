from pprint import pprint as pp
import math

from codetiming import Timer
from rich import print

from utils import (SESSIONS, get_data)


YEAR = 2022
DAY = 8


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=False)


def get_arms(coord: tuple[int, int], data: list[str]) -> list[list[int]]:
    """
    This will return a list of four list (arms), each containing the value of all the trees in all 4 directions, origin not included, ordered towards the edges.
    """
    y = coord[0]
    x = coord[1]

    MAX_Y = len(data)
    MAX_X = len(data[0])

    top = [data[n][x] for n in range(0, y)]
    bottom = [data[n][x] for n in range(y + 1, MAX_Y)]
    left = [data[y][n] for n in range(0, x)]
    right = [data[y][n] for n in range(x + 1, MAX_X)]

    return [list(reversed(top)), bottom, list(reversed(left)), right]


def is_visible(coord: tuple[int, int], data: list[str]) -> bool:
    """
    This will check that the tree in coord is the tallest in at least one of the arms, and thus is visible from at least a direction
    """
    y = coord[0]
    x = coord[1]
    height = data[y][x]
    arms = get_arms(coord, data)

    if any(all(x < height for x in arm) for arm in arms):
        return True

    return False


def get_scenic_score(coord: tuple[int, int], data: list[str]) -> int:
    """
    This will calculate the scenic score for a tree in coord.
    It will get all arms from that tree and checks where the nearest tree with equal or higher heights is.
    Will return the math.prod() of the distance for the 4 directions.
    """
    y = coord[0]
    x = coord[1]

    height = data[y][x]
    arms = get_arms(coord, data)

    scenic_score = []

    for arm in arms:
        c= 0
        if arm:
            for tree in arm:
                c += 1
                if tree >= height:
                    break
                else:
                    pass
        scenic_score.append(c)

    return math.prod(scenic_score)


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: list[str]):

    """
    This iterate every tree in the matrix and checks if it's visible.
    Sol1 is the sum of all the visible trees
    """

    sol1 = 0

    MAX_Y = len(data)
    MAX_X = len(data[0])

    for x in range(0, MAX_X):
        for y in range(0, MAX_Y):
            if is_visible((y,x), data):
                sol1 += 1

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    """
    This will calculate the scenic score for every tree in the matrix
    and return the max scenic score
    """

    sol2 = 0
    scenic_scores = []
    MAX_Y = len(data)
    MAX_X = len(data[0])

    for x in range(0, MAX_X):
        for y in range(0, MAX_Y):
            scenic_scores.append(get_scenic_score((y, x), data))
    sol2 = max(scenic_scores)

    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
