from codetiming import Timer
from rich import print
from dataclassy import dataclass
from utils import (SESSIONS, get_data, MovingThing)



YEAR = 2022
DAY = 14
EXAMPLE = False


@dataclass
class SandParticle(MovingThing):
    """A Sand Particle."""

    def fall_down(self, walls: set[tuple[int]], sand:set[tuple[int]]) -> bool:
        """This is the function that simulates the falling of a particle of sand.
        As per instructions, it checks if the coordinates under it are not walls or not sand.
        If down is empty, it will go down.
        If down is full, it will go diagonal to the left.
        If diagonal to the left is full, it will go diagonal to the right.
        If diagonal to the right is full, it will rest where it is. Adds its coordinate to
            the sand sets. Return False.

        If it rests on the spawner location, return True to end the simulation.

        While going down, if it reaches a y coordinate that's lower than everything else, it's 
        in the void and it will fall forever. Returns True to end the simulation.

        Args:
            walls (set[tuple[int]]): the set that contains all the impassable points coordinates

            sand (set[tuple[int]]): the set that contains the coordinates of the already settled down
                list of particles.

        Returns:
            bool: this will return False when the particle reach a stop, or True when it falls
            in the void (part 1) or it rests on the spawner coordinates (part 2)
        """

        bottom_edge = max(coord[0] for coord in walls)

        while not self.settled:
            left, down, right = [(self.y + 1, self.x - 1), (self.y + 1, self.x), (self.y + 1, self.x + 1)]

            if down not in walls and down not in sand:
                self.y += 1
                if self.y > bottom_edge:
                    return True

            elif left not in walls and left not in sand:
                self.y += 1
                self.x -= 1

            elif right not in walls and right not in sand:
                self.y += 1
                self.x += 1

            else:
                sand.add((self.y, self.x))

                if (self.y, self.x) == (0, 500):
                    return True

                return False

def draw_wall_line(a: tuple[int, int], b: tuple[int, int]) -> set[tuple[int]]:
    """This function will calculate the coordinates of every point between a and b. 
    The segment can only be horizontal or vertical.

    Args:
        a (tuple[int, int]): coordinates of point a
        b (tuple[int, int]): coordinates of point b

    Returns:
        set[tuple[int]]: coordinates of every point between a and b, extremities included.
    """
    y1, x1 = a
    y2, x2, = b
    s = set()

    if y1 == y2:
        for point in range(min(x1, x2), max(x1, x2) + 1):
            s.add((y1, point))

    else: 
        for point in range(min(y1, y2), max(y1, y2) + 1):
            s.add((point, x1))

    return s


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    After that, we'll get the coordinates of every wall segment, as a and b, and pass to the appropriate function
    draw_wall_line(a, b) that will return a set of coordinate for every point in the segment, a and b included.
    We'll build our walls set this way, and pass to part1 and part2
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    
    walls: set = set()

    for wall in data:
        points = []
        for wallpoint in wall.split(' -> '):
            x, y = wallpoint.split(',')
            points.append((int(y), int(x)))

        for i in range(len(points) - 1):
            walls.update(draw_wall_line(points[i], points[i + 1]))

    data = walls


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: set[tuple[int]]) -> int:
    """Until a certain condition (the sand particles fall into the void) occur and switch stop_sim,
    we spawn a new SandParticle at the spawner location (it's hardcoded - (0, 500)) and then we call
    SandParticle().fall_down(walls, sand) where walls is the set of impassable points coordinate and
    sand is an (initially) empty set that will be filled up by the coordinates of every resting place 
    of the falling sand when it finally settles.

    Args:
        data (set[tuple[int]]): this is a set that contains all the 'wall' points coordinates

    Returns:
        int: returns the length of the set that contains all the rested sand particles
    """
    walls = data
    sol1 = 0

    stop_sim = False
    sand = set()

    while not stop_sim:
        particle = SandParticle(x=500, y=0)
        stop_sim = particle.fall_down(walls, sand)

    sol1 = len(sand)

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data: set[tuple[int]]) -> int:
    """First of all, we add to our existing walls set a bottom wall, that is two steps under the lowest point.
    Because the sand will fall at maximum in a perfect diagonal, the total lenght of the bottom is
    - bottom_y <---- spawn_x ----> + bottom_y
    basically is from 500-bottom_y to bottom_y+500. 
    I added 10 of padding in each side just to be sure.

    Until a certain condition (the sand particles fall into the void) occur and switch stop_sim,
    we spawn a new SandParticle at the spawner location (it's hardcoded - (0, 500)) and then we call
    SandParticle().fall_down(walls, sand) where walls is the set of impassable points coordinate and
    sand is an (initially) empty set that will be filled up by the coordinates of every resting place 
    of the falling sand when it finally settles.

    Args:
        data (set[tuple[int]]): this is a set that contains all the 'wall' points coordinates

    Returns:
        int: returns the length of the set that contains all the rested sand particles
    """
    walls = data
    sol2 = 0

    bottom_y = max(coord[0] for coord in walls) + 2
    bottom_wall = set([(bottom_y, x) for x in range(500 - bottom_y - 10, 500 + bottom_y + 10)])
    walls.update(bottom_wall)

    stop_sim = False
    sand = set()

    while not stop_sim:
        particle = SandParticle(x=500, y=0)
        stop_sim = particle.fall_down(walls, sand)

    sol2 = len(sand)

    return sol2


s1 = part1(data)
s2 = part2(data)


print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
