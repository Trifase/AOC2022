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

    settled: bool = False
    last_pos: tuple[int, int] = (0, 500)
    last_last_pos: tuple[int, int] = (0, 500)

    def fall_down(self, walls: set[tuple[int, int]], sand: set[tuple[int, int]], void: int) -> tuple[bool, tuple[int,int] | None, tuple[int, int]]:
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
            walls (set[tuple[int, int]]): the set that contains all the impassable points coordinates

            sand (set[tuple[int, int]]): the set that contains the coordinates of the already settled down
                list of particles.

            void (int): the lowest (actually higher) y coordinates. After that, the particle will fall forever.

        Returns:
            tuple[bool, tuple[int,int] | None, tuple[int, int]]: this will return a tuple with tree values. The first is a bool:
            False when the particle reach a stop, or True when it falls in the void (part 1) or it rests on 
            the spawner coordinates (part 2). The second value is the particle coordinate when it is settled. 
            The third value is the third last position, used as spawn for the next particle
        """
        
        while not self.settled:
            left, down, right = [(self.y + 1, self.x - 1), (self.y + 1, self.x), (self.y + 1, self.x + 1)]
            self.last_last_pos = self.last_pos
            
            if down not in walls and down not in sand:
                self.last_pos = (self.y, self.x)
                self.y += 1
                if self.y > void:
                    return (True, None, self.last_last_pos)

            elif left not in walls and left not in sand:
                self.last_pos = (self.y, self.x)
                self.y += 1
                self.x -= 1

            elif right not in walls and right not in sand:
                self.last_pos = (self.y, self.x)
                self.y += 1
                self.x += 1

            else:
                self.settled = True
                if (self.y, self.x) == (0, 500):
                    return (True, (self.y, self.x), self.last_last_pos)

                return (False, (self.y, self.x), self.last_last_pos)

def get_wall_points(a: tuple[int, int], b: tuple[int, int]) -> set[tuple[int, int]]:
    """This function will calculate the coordinates of every point between a and b. 
    The segment can only be horizontal or vertical.

    Args:
        a (tuple[int, int]): coordinates of point a
        b (tuple[int, int]): coordinates of point b

    Returns:
        set[tuple[int, int]]: coordinates of every point between a and b, extremities included.
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

def simulate_sand(walls: set[tuple[int, int]]) -> set[tuple[int, int]]:
    stop_sim = False
    sand = set()
    void = max(coord[0] for coord in walls)
    spawn_y, spawn_x = 0, 500

    while not stop_sim:
        particle = SandParticle(x=spawn_x, y=spawn_y)
        stop_sim, sand_coord, last_particle = particle.fall_down(walls, sand, void)
        if sand_coord:
            sand.add(sand_coord)

            """Ottimizzazione 1: invece di spawnare la sabbia all'inizio, la spawniamo nella terzultima posizione registrata.
            Ad esempio, se la particella si ferma nella posizione n, la funzione ritorna anche n-2 (temporalmente) e riutilizziamo
            quella per spwnare la prossima"""
            spawn_y, spawn_x = last_particle
    return sand


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    After that, we'll get the coordinates of every wall segment, as a and b, and pass to the appropriate function
    get_wall_points(a, b) that will return a set of coordinate for every point in the segment, a and b included.
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
            walls.update(get_wall_points(points[i], points[i + 1]))

    data = walls


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: set[tuple[int, int]]) -> int:
    """Until a certain condition (the sand particles fall into the void) occur and switch stop_sim,
    we spawn a new SandParticle at the spawner location (it's hardcoded - (0, 500)) and then we call
    SandParticle().fall_down(walls, sand, void) where walls is the set of impassable points coordinate,
    sand is an (initially) empty set that will be filled up by the coordinates of every resting place 
    of the falling sand when it finally settles and void is the y-coordinate of the void.
    Everytime a particle settles, we will add to sets.

    Args:
        data (set[tuple[int, int]]): this is a set that contains all the 'wall' points coordinates

    Returns:
        int: returns the length of the set that contains all the rested sand particles
    """
    walls = data
    sol1 = 0

    sand = simulate_sand(walls)

    sol1 = len(sand)

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data: set[tuple[int, int]]) -> int:
    """First of all, we add to our existing walls set a bottom wall, that is two steps under the lowest point.
    Because the sand will fall at most in a perfect diagonal, the total lenght of the bottom is
    - bottom_y <---- spawn_x ----> + bottom_y
    basically is from 500-bottom_y to bottom_y+500. 

    Until a certain condition (the sand particles fall into the void) occur and switch stop_sim,
    we spawn a new SandParticle at the spawner location (it's hardcoded - (0, 500)) and then we call
    SandParticle().fall_down(walls, sand, void) where walls is the set of impassable points coordinate,
    sand is an (initially) empty set that will be filled up by the coordinates of every resting place 
    of the falling sand when it finally settles and void is the y-coordinate of the void.
    Everytime a particle settles, we will add to sets.

    Args:
        data (set[tuple[int, int]]): this is a set that contains all the 'wall' points coordinates

    Returns:
        int: returns the length of the set that contains all the rested sand particles
    """
    walls = data
    sol2 = 0

    """Here we calculate the y-coordinate and length of the bottom wall, generate all the points
    and add to the walls set."""
    bottom_y = max(coord[0] for coord in walls) + 2
    bottom_wall = get_wall_points((bottom_y, 500 - bottom_y), (bottom_y, 500 + bottom_y))
    walls.update(bottom_wall)

    # sand = simulate_sand(walls)
    # sol2 = len(sand)

    """Ok listen. This is too slow. So i commented the last part and wrote a new method. 
    Kudos to Giulio (https://github.com/CapacitorSet) for the idea.
    Basically, we start with one grain of sand. We descend a row. For each grain, we add three children, (bottomleft, down, bottomright)
    if they are not in the same spot of points of walls. We do this for every row until the very end."""

    SPAWN = (0, 500)
    last_row: set = set()

    last_row.add(SPAWN)

    def get_three_children(granello, walls): 
        """return a set of three children if they are not walls"""
        y, x = granello
        children = ((y + 1, x - 1), (y + 1, x), (y + 1, x + 1))
        return set(children).difference(walls)

    sol2 = 1  # Spawn point
    for _ in range(max(coord[0] for coord in walls)):
        tempset = set()
        for granello in last_row:
            tempset.update(get_three_children(granello, walls))
        sol2 += len(tempset)
        last_row = tempset

    return sol2


s1 = part1(data)
s2 = part2(data)


print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
