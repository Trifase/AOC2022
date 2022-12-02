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
DAY = 2
TEST = 0
SESSIONS = [
    '53616c7465645f5fa84dc053d6450788a4e374255929271bab87b5571810b6b409d259985976f323a7d689eec97c6cec3ffd7edcba32898480c58f3d345323b7',
    '53616c7465645f5f31bd76685552b94983dce5c1a20ee21a319c38307f1aded11ec8cac034efc583a546d4d53d1f360cc9b8b75bd8694953df05f00bf1af3d31'
    ]

if TEST:
    FILENAME = f"data/{DAY:02d}-esempio.txt"
else:
    FILENAME = f"data/{DAY:02d}.txt"

t0 = Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms")


#Input parsing
with t0:
    data = get_data(YEAR, DAY, SESSIONS)
    # data = get_example(DAY)

    # print(data)

points = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

rps = {
    'X': "rock",
    'A': "rock",
    'Y': "paper",
    'B': "paper",
    'Z': "scissor",
    'C': "scissor"
}

map_same = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z'
}


def outcome(a, b):
    a = rps.get(a)
    b = rps.get(b)
    if a == b:
        return 3
    elif a == "rock" and b == 'paper':
        return 6
    elif a == 'paper' and b == 'scissor':
        return 6
    elif a == 'scissor' and b == 'rock':
        return 6
    else:
        return 0

def what_to_play(a, b):
    match b:
        case 'Y': # pareggio
            return map_same.get(a)

        case 'Z': # vittoria
            match a:
                case 'A':
                    return 'Y'
                case 'B':
                    return 'Z'
                case 'C':
                    return 'X'

        case 'X': # perdita
            match a:
                case 'A':
                    return 'Z'
                case 'B':
                    return 'X'
                case 'C':
                    return 'Y'

# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):
    sol1 = 0
    for game in data:
        a, b = game.split()
        p = outcome(a, b) + points.get(b)
        # print(f"{game} -> {p}")
        sol1 += p
    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    sol2 = 0
    for game in data:
        a, b = game.split()
        b = what_to_play(a, b)
        p = outcome(a, b) + points.get(b)
        # print(f"{game}: devo giocare {b}, la giocata diventa {a} {b} -> {p}")
        sol2 += p
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

