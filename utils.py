import re
import dataclassy as dataclass

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

def get_data(year, day, sessions):
    import os.path
    import requests
    import sys
    
    if not os.path.isfile(f'data/{day}.txt'):
        url = f"https://adventofcode.com/{str(year)}/day/{str(day)}/input"
        headers = {'Cookie': f'session={sessions[0]}'}
        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            with open(f'data/{day}.txt', 'w') as file:
                file.write(r.text)
        else:
            sys.exit(f"/api/alerts response: {r.status_code}: {r.reason} \n{r.content}")

    data = open(f'data/{day}.txt', 'r')
    return [l.strip() for l in data.readlines()]

