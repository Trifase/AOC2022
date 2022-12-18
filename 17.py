from codetiming import Timer
from rich import print
from dataclassy import dataclass
from utils import (SESSIONS, get_data)
from itertools import cycle

from typing import Self

YEAR = 2022
DAY = 17
EXAMPLE = False

Coord = tuple[int, int]


@dataclass
class GenericPiece:
    origin: Coord
    box_h: int
    box_w: int
    _occupied_points: set[Coord]

    @property
    def occupied_points(self):
        y, x = self.origin
        mypoints = set()
        for point in self._occupied_points:
            a, b = point
            mypoints.add((a+y, b+x))
        return mypoints
    
    @property
    def shadow_points_down(self):
        mypoints = set()
        for point in self.occupied_points:
            point = (point[0]+1, point[1])
            if point not in self.occupied_points:
                mypoints.add(point)
        return mypoints

    @property
    def shadow_points_right(self):
        mypoints = set()
        for point in self.occupied_points:
            point = (point[0], point[1] + 1)
            if point not in self.occupied_points:
                mypoints.add(point)
        return mypoints

    @property
    def shadow_points_left(self):
        mypoints = set()
        for point in self.occupied_points:
            point = (point[0], point[1] - 1)
            if point not in self.occupied_points:
                mypoints.add(point)
        return mypoints

    def move_right(self, field):
        if (max(p[1] for p in self.occupied_points) < 6) and all(p not in field for p in self.shadow_points_right):
            y, x = self.origin
            self.origin = (y, x + 1)
            return True
        else:
            return False
    
    def move_left(self, field):
        if (min(p[1] for p in self.occupied_points) > 0) and all(p not in field for p in self.shadow_points_left):
            y, x = self.origin
            self.origin = (y, x - 1)
            return True
        else:
            return False

    def move_down(self, field):
        if all(p not in field for p in self.shadow_points_down):
            y, x = self.origin
            self.origin = (y + 1, x)
            return True
        else:
            return False
    
    def print_piece(self):
        grid = []
        for y in range(self.box_h):
            row = []
            for x in range(self.box_w):
                row.append(' ')
            grid.append(row)

        for y in range(self.box_h):
            for x in range(self.box_w):
                if (y, x) in self._occupied_points:
                    grid[y][x] = '#'
        for row in grid:
            print(''.join(row))
        return grid



class PieceHLine(GenericPiece):
    box_h: int = 1
    box_w: int= 4
    _occupied_points: set[Coord] = {
        (0, 0), (0, 1), (0,2), (0, 3)
        }

class PieceVLine(GenericPiece):
    box_h: int = 4
    box_w: int= 1
    _occupied_points: set[Coord] = {
        (0, 0),
        (1, 0),
        (2, 0),
        (3, 0)
        }

class PieceL(GenericPiece):
    box_h: int = 3
    box_w: int= 3
    _occupied_points: set[Coord] = {
                        (0, 2),
                        (1, 2),
        (2, 0), (2, 1), (2, 2)
        }

class PieceCross(GenericPiece):
    box_h: int = 3
    box_w: int= 3
    _occupied_points: set[Coord] = {
                (0, 1),
        (1, 0), (1, 1), (1, 2),
                (2, 1)
        }

class PieceBox(GenericPiece):
    box_h: int = 2
    box_w: int= 2
    _occupied_points: set[Coord] = {
        (0, 0), (0, 1),
        (1, 0), (1, 1)
        }


def print_field(field, piece):
    field = field | piece.occupied_points if piece else field
    max_x = max(p[1] for p in field)
    min_y = min(p[0] for p in field)
    max_y = max(p[0] for p in field)
    # print(field, max_x, min_y, max_y)
    # quit()
    grid = []
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(7):
            row.append('.')
        grid.append(row)

    for point in field:
        y, x = point
        if y == 0:
            grid[abs(y)][x] = '-'
        else:
            grid[abs(y)][x] = '#'
    
    grid = reversed(grid)
    for row in grid:
        if ''.join(row) == '-------':
            print('+' + ''.join(row) + '+')
        else:
            print('|' + ''.join(row) + '|')
    print()



# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    data = [char for char in data[0]]


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data):

    sol1 = 0
    spawned = 0
    base_h = 0
    altezza_max = base_h
    spawn_order = [PieceHLine, PieceCross, PieceL, PieceVLine, PieceBox]
    field: set = set()
    piece = None

    for x in range(7):
        field.add((altezza_max, x))
    

    for order in cycle(data):
        if spawned == 2022:
            break
        
        
        if not piece:
            
            # print(field)

            piece: GenericPiece
            next_h = spawn_order[spawned % 5].box_h
            # print(next_h)
            # print(f"Spawno il pezzo #{spawned} ({spawn_order[spawned % 5]}) con origin {(altezza_max - 3 - next_h, 2)}")
            piece = spawn_order[spawned % 5](origin=(altezza_max - 3 - next_h, 2))
            # print_field(field, piece)
        # print(order)
        if order == '>':
            # print("vado a destra")
            # print(piece.move_right(field))
            # print_field(field, piece)
            piece.move_right(field)
        else:
            # print("vado a sx")
            # print(piece.move_left(field))
            # print_field(field, piece)
            piece.move_left(field)

        # print("vado giù")
        movement = piece.move_down(field)
        # print_field(field, piece)
        # print(movement)
        # print(piece.occupied_points)
        if not movement:
            # print("Mi fermo!")
            # print(field)
            for point in piece.occupied_points:
                field.add(point)
            # print(field)
            altezza_max = min(p[0] for p in field)
            piece = None
            spawned += 1
            # print(f"Nuova altezza massima: {altezza_max}")
        # quit()
    print(altezza_max)
    print(spawned)
    sol1 = base_h - altezza_max

    return sol1

# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data) -> int:
    sol2 = 0

    return sol2


s1 = part1(data)
s2 = part2(data)


print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
