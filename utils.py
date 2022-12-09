import re
import dotenv
import os
import os.path
import requests
import sys

from dataclassy import dataclass

dotenv.load_dotenv()
SESSIONS = os.environ["AOC_SESSION"]


# Utilities


@dataclass
class MovingThing:
    """
    This is the base class of a moving things in a 2D matrix. It has two coords (x and y) and
    a move() function that takes a direction ((L)eft, (R)ight, (U)p and (D)own) and optionally an amount.
    
    """
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

    def move_to(self, coords: tuple[int, int]):
        self.x = coords[0]
        self.y = coorde[1]
        self.coords = (self.x, self.y)



def rematch(pattern, string):
    return re.fullmatch(pattern, string)

def dec_to_bin(dec,bit):
    b = str(bin(int(dec))[2:]).zfill(bit)
    return b

def bin_to_dec(string, bit=2):
        dec = int(string, bit)
        return dec

def remove_duplicates(lista):
  return list(dict.fromkeys(lista))

def get_key_from_value(my_dict, to_find):
    for k,v in my_dict.items():
        if sorted(v) == sorted(to_find): return k
    return None


def split_in_chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_data(year, day, sessions, strip=True, integers=False, example=False):
    USER_AGENT = {}

    if not os.path.isfile(f'data/{day}-example.txt'):
        open(f'data/{day}-example.txt', 'w').close()

    if not os.path.isfile(f'data/{day}.txt'):
        url = f"https://adventofcode.com/{str(year)}/day/{str(day)}/input"
        headers = {
            'Cookie': f'session={sessions}',
            'User-Agent': 'github.com/Trifase/AOC2022 by luca.bellanti@gmail.com',
        }
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            with open(f'data/{day}.txt', 'w') as file:
                file.write(r.text)
        else:
            sys.exit(f"/api/alerts response: {r.status_code}: {r.reason} \n{r.content}")

    if example:
        data = open(f'data/{day}-example.txt', 'r')
    else:
        data = open(f'data/{day}.txt', 'r')

    if integers:
        return [int(l.strip()) if strip else int(l) for l in data.readlines()]
    else:
        return [l.strip() if strip else l for l in data.readlines()]

def get_example(day, integers=False):
    with open(f'data/{day}-example.txt', 'r') as file:
        if integers:
            return [int(l.strip()) for l in file.readlines()]
        else:
            return [l.strip() for l in file.readlines()]

def split_list(list):
    l = []
    for y in '\n'.join(list).split('\n\n'):
        l.append([x for x in y.split('\n')])
    return l

def sliding_window(lista: list, length: int) -> list:
    for i in range(0, len(lista) - length + 1):
        yield lista[i:i + length]