import copy
import logging
import re
import rich
import time

from collections import Counter, defaultdict
from codetiming import Timer
from PIL import Image, ImageDraw 
from pprint import pprint as pp
from rich import print

from utils import SESSIONS, rematch, get_key_from_value, remove_duplicates, dec_to_bin, bin_to_dec, get_data, get_example, split_list, split_in_chunks

YEAR = 2022
DAY = 5

#Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. The first block will be put into [tempstack] to be parsed later, the empy line will switch the boolean parse orders, and the rest of the lines will be parsed and put into the [orders] list.
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=False, example=False)

    stacks = []
    orders = []
    tempstack = []
    parse_orders = False

    for line in data:
        if line == '\n':
            parse_orders = True
            continue

        if not parse_orders:
            tempstack.append(line)

        else:
            _, n, _, mfrom, _, mto = line.split(" ")
            orders.append([int(n), int(mfrom), int(mto)])

    """
    tempstack will be reversed, and then the first line will be parsed for non null characters to detect the labels. Then, every value from every line will be put into a stack list inside stacks.
    """
    tempstack.reverse()

    for index, value in enumerate(tempstack[0]):
        if value not in [' ', '\n']:
            stacks.append([tempstack[x][index] for x in range(1, len(tempstack)) if tempstack[x][index] != ' '])

    """
    We'll put both lists together to be passed to part1() and part2()
    """
    data = stacks, orders


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    """
    First, stacks and orders will be extracted from a deppcopied data
    Parsing the orders, for every quantity of crates, one will be popped (the last item) and it will be appended (at the end)
    from/to the appropriate stack. The solution will be a joined string from the last element of every stack.
    """
    sol1 = 0
    stacks, orders = copy.deepcopy(data)
    for order in orders:
        for _ in range(order[0]):
            crate = stacks[order[1]-1].pop()
            stacks[order[2]-1].append(crate)

    sol1 = ''.join([s[-1] for s in stacks])
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    """
    First, stacks and orders will be extracted from data.
    Parsing the orders, for every order, we'll make a tempslist from the final subsection of the appropriate stack. Then the same section will be
    deleted from the from stack, and extended (inserted at the end) into the appropriate to-stack.
    The solution will be a joined string from the last element of every stack.
    """
    sol2 = 0
    stacks, orders = data
    for order in orders:
        tempstack = stacks[order[1]-1][-order[0]:]
        del stacks[order[1]-1][-order[0]:]
        stacks[order[2]-1].extend(tempstack)
    sol2 = ''.join([s[-1] for s in stacks])
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

