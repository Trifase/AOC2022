import re
from rich import print
import copy
import rich
import pprint
import logging
import time

from PIL import Image, ImageDraw 
from collections import Counter, defaultdict
from codetiming import Timer

from utils import SESSIONS, rematch, get_key_from_value, remove_duplicates, dec_to_bin, bin_to_dec, get_data, get_example, split_list, split_in_chunks

YEAR = 2022
DAY = 4


#Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    data = get_data(YEAR, DAY, SESSIONS, example=False)

# print(data)



# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    sol1 = 0
    for pair in data:
        elf1, elf2 = pair.split(",")
        s1 = set(range(int(elf1.split("-")[0]), int(elf1.split("-")[1]) + 1))
        s2 = set(range(int(elf2.split("-")[0]), int(elf2.split("-")[1]) + 1))
        if not (s1 - s2) or not (s2 - s1):
            sol1 += 1
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    sol2 = 0
    for pair in data:
        elf1, elf2 = pair.split(",")
        s1 = set(range(int(elf1.split("-")[0]), int(elf1.split("-")[1]) + 1))
        s2 = set(range(int(elf2.split("-")[0]), int(elf2.split("-")[1]) + 1))
        if s1.intersection(s2):
            sol2 += 1
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

