import re
from dataclassy import dataclass

SESSIONS = [
    '53616c7465645f5fa84dc053d6450788a4e374255929271bab87b5571810b6b409d259985976f323a7d689eec97c6cec3ffd7edcba32898480c58f3d345323b7',
    '53616c7465645f5f31bd76685552b94983dce5c1a20ee21a319c38307f1aded11ec8cac034efc583a546d4d53d1f360cc9b8b75bd8694953df05f00bf1af3d31'
    ]


# Utilities
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

@dataclass
class Point:
    x: str
    y: str


def split_in_chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_data(year, day, sessions, integers=False, example=False):
    import os.path
    import requests
    import sys

    if not os.path.isfile(f'data/{day}-example.txt'):
        open(f'data/{day}-example.txt', 'w').close()

    if not os.path.isfile(f'data/{day}.txt'):
        url = f"https://adventofcode.com/{str(year)}/day/{str(day)}/input"
        headers = {'Cookie': f'session={sessions[0]}'}
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
        return [int(l.strip()) for l in data.readlines()]
    else:
        return [l.strip() for l in data.readlines()]

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
