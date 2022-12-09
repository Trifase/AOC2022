from pprint import pprint as pp
import math

from codetiming import Timer
from rich import print
from dataclassy import dataclass
from utils import (SESSIONS, get_data, MovingThing)

YEAR = 2022
DAY = 9

class RopePiece(MovingThing):
    """
    This is a piece of a rope, based on Movingthing.
    It can be attached to another MovingThing with the attach_to parameter.
    The function follow() is used to move this piece, it takes no parameters.
    """
    attached_to: MovingThing = None

    def follow(self, head: MovingThing= None):
        """
        This is used to move the piece based on the position of the piece it is attached_to.
        If there is not such piece, raise AttributeError.
        First, it calculates the Chess Distance (https://en.wikipedia.org/wiki/Chebyshev_distance)
        from the piece it is attached to, and if it's more than 1, it moves accordingly in one 
        of the 4 cardinal directions or in diagonal.  
        """
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

        if abs(dx) <= 1 and abs(dy) <= 1: # Chess Distance
            pass
        else:
            x = sign(dx)
            y = sign(dy)
            self.x += x
            self.y += y
            self.coords = (self.x, self.y)

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
    We'll instance a Head and a Tail of a rope.
    Tail will be attached_to Head.
    We'll parse every line to grab the (dir)ection
    and the (amount) of moving steps.
    For every step in (dir), we'll move head with head.move() and we'll move the tail with tail.move().
    We'll save every position tail visits in a (visited) set (so we won't have duplicates).
    We'll solve getting the lenght of the set.
    """

    sol1 = 0

    visited = set()
    visited.add((0, 0))

    head = RopePiece()
    tail = RopePiece(attached_to=head)

    for line in data:
        dir, amount = line.split()
        for _ in range(int(amount)):
            head.move(dir)
            tail.follow()
            visited.add(tail.coords)

    sol1 = len(visited)

    return sol1

# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    """
    In a list (rope) we'll add a head.
    Then we will append 9 tail pieces, every one of them will be attached_to to the previous.
    We'll parse every line to grab the (dir)ection and the (amount) of moving steps.
    For every step in (dir), we'll move head with head.move() according to the input
    and we'll move all the tail pieces calling tail.follow() with a for-loop. 
    We'll save every position the last tail visits in a (visited) set (so we won't have duplicates).
    We'll solve getting the lenght of the set.
    """

    sol2 = 0

    visited = set()
    visited.add((0, 0))

    rope = []
    # We add the head
    rope.append(RopePiece())

    # We add all the tails, each one attached_to the previous one
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
