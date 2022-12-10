from pprint import pprint as pp
import math

from codetiming import Timer
from rich import print
from dataclassy import dataclass
from advent_of_code_ocr import convert_array_6
from utils import (SESSIONS, get_data, MovingThing)

YEAR = 2022
DAY = 10


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=False)

# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: list[str]):
    """
    For every command, two things can happen. If it is a noop command, we'll advance one cycle and check
    If not, we'll advance one cycle, check, add x, advance one cycle, check.
    Check means that if we check if we are in cycle 20/60/100/140/180/220, and if we are, we'll multiply cycle and x, and add it to sol1.
    """
    x = 1
    cycle = 1
    sol1 = 0

    for line in data:
        if line == 'noop':
            cycle += 1

        else:
            cycle += 1
            if cycle in [20, 60, 100, 140, 180, 220]:
                sol1 += cycle*x

            x += int(line.split()[-1])
            cycle += 1

        if cycle in [20, 60, 100, 140, 180, 220]:
                sol1 += cycle*x

    return sol1

# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    """
    For every command, two things can happen. If it is a noop command, we'll advance one cycle and check
    If not, we'll advance one cycle, check, add x, advance one cycle, check.
    Check means that we check that the crt value is in the same columns of the three pixel wide sprite centered in x.
    If we are, we'll lit that crt pixel. crt loops at 40.
    """

    def print_char(crt, x):
        """
        This checks if crt value is one of the three pixel of the sprite. If it is return a full char, else an empty one
        """
        if crt in range(x-1, x+2):
            return '█'
        else:
            return '.'

    sol2 = 0
    display = ""
    crt = 0
    x = 1
    cycle = 1
    final_string = []

    for line in data:
        if line == 'noop':
            display += print_char(crt, x)
            crt = (crt + 1)%40
            cycle += 1

        else:
            display += print_char(crt, x)
            crt = (crt + 1)%40
            cycle += 1

            display += print_char(crt, x)
            x += int(line.split()[-1])
            crt = (crt + 1)%40
            cycle += 1

    for i in [0, 40, 80, 120, 160, 200]:
        final_string.append([x for x in display[i:i+40]])
 
    # we use convert_array_6 from https://github.com/bsoyka/advent-of-code-ocr to display the string instead of the pixels array
    sol2 = convert_array_6(final_string, fill_pixel='█', empty_pixel='.')

    return sol2

s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
