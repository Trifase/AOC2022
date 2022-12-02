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

from utils import rematch, get_key_from_value, remove_duplicates, dec_to_bin, bin_to_dec, get_data, get_example, split_list

YEAR = 2022
DAY = 1
TEST = 0
SESSIONS = [
    '53616c7465645f5fa84dc053d6450788a4e374255929271bab87b5571810b6b409d259985976f323a7d689eec97c6cec3ffd7edcba32898480c58f3d345323b7',
    '53616c7465645f5f31bd76685552b94983dce5c1a20ee21a319c38307f1aded11ec8cac034efc583a546d4d53d1f360cc9b8b75bd8694953df05f00bf1af3d31'
    ]

if TEST:
    FILENAME = f"data/{DAY:02d}-test.txt"
else:
    FILENAME = f"data/{DAY:02d}.txt"

t0 = Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms")


#Input parsing
with t0:
    data = get_data(YEAR, DAY, SESSIONS)

    data = get_example(DAY)

    data = split_list(data)
    # print(data)




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

if TEST:
    print("\n======================\nTesting environment:\n======================")
else:
    print("\n======================")

print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

