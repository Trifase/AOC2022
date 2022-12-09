from pprint import pprint as pp
import math

from codetiming import Timer
from rich import print
from dataclassy import dataclass
from utils import (SESSIONS, get_data)


YEAR = 2022
DAY = 9

@dataclass
class MovingThing:
    x: int = 0
    y: int = 0
    coords : tuple[int, int] = (0, 0)
    def move(self, dir: str, units: int=1):
        match dir:
            case 'U':
                self.y += units
            case 'D':
                self.y -= units
            case 'R':
                self.x += units
            case 'L':
                self.x -= units

        self.coords = (self.x, self.y)
        # print(f"head: mi sposto su {self.coords}")


class RopePiece(MovingThing):
    attached_to: MovingThing = None

    def follow(self, head: MovingThing= None):
        def sign(a: int):
            if a > 0:
                return 1
            elif a < 0:
                return -1
            else:
                return 0
        if not self.attached_to:
            raise AttributeError("Non sono attaccato a niente")

        head = self.attached_to
        dx, dy = (head.x - self.x), (head.y - self.y)

        if abs(dx) <= 1 and abs(dy) <= 1:
            pass
            # print("tail: Sto fermo")
        else:
            x = sign(dx)
            y = sign(dy)
            self.x += x
            self.y += y
            # print(f"tail: mi sposto su ({self.x}, {self.y})")
            self.coords = (self.x, self.y)


#Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=False)







# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: list[str]):

    """

    """

    sol1 = 0

    visited = set()
    visited.add((0, 0))

    head = RopePiece()
    tail1 = RopePiece(attached_to=head)

    for line in data:
        dir, amount = line.split()
        for _ in range(int(amount)):
            head.move(dir)
            tail1.follow()
            visited.add(tail1.coords)

    sol1 = len(visited)

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    """

    """

    sol2 = 0

    visited = set()
    visited.add((0, 0))

    rope = []
    rope.append(RopePiece())
    for i in range(9):
        rope.append(RopePiece(attached_to=rope[-1]))


    for line in data:
        dir, amount = line.split()
        for _ in range(int(amount)):
            rope[0].move(dir)
            for piece in rope[1:]:
                piece.follow()
            visited.add(rope[-1].coords)

    sol2 = len(visited)
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
