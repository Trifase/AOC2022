from rich import print

from codetiming import Timer

from utils import SESSIONS, get_data

YEAR = 2022
DAY = 2


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    data = get_data(YEAR, DAY, SESSIONS)

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
    'Z': "scissors",
    'C': "scissors"
}

equivalent = {
    'A': 'X',
    'B': 'Y',
    'C': 'Z'
}


def outcome(a, b):
    a = rps.get(a)
    b = rps.get(b)
    if a == b:
        return 3  # pareggio
    elif a == "rock" and b == 'paper':
        return 6  # vittoria
    elif a == 'paper' and b == 'scissors':
        return 6
    elif a == 'scissors' and b == 'rock':
        return 6
    else:
        return 0  # perdita

def what_to_play(a, b):
    match b:
        case 'Y':  # pareggio
            return equivalent.get(a)

        case 'Z':  # vittoria
            match a:
                case 'A':
                    return 'Y'
                case 'B':
                    return 'Z'
                case 'C':
                    return 'X'

        case 'X':  # perdita
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
        sol2 += p
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")

