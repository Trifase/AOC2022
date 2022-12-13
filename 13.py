from codetiming import Timer
from rich import print
from utils import (SESSIONS, get_data, split_list, remove_empty_from_data)

from typing import Self


YEAR = 2022
DAY = 13
EXAMPLE = False

# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)


Packet: list[int | Self ] | int

def compare(left: Packet, right: Packet) -> bool | None:
    """
    Controlliamo i due pacchetti seguendo le istruzioni praticamente alla lettera. Se non è True o False continuiamo a testa bassa.

    Args:
        left (Packet): the left packet
        right (Packet): the right packet

    Returns:
        bool | none: True if the packets are in the right order, False if the packets are out of order, None if they are equal
    """
    if type(left) == type(right) == int:
        if left < right:
            return True
        if left > right:
            return False
        return None

    elif type(left) == type(right) == list:
        for inner_left, inner_right in zip(left, right):
            is_ok = compare(inner_left, inner_right)
            if is_ok in [True, False]:
                return is_ok
        
        if len(left) < len(right):
            return True
        if len(left) > len(right):
            return False

        return None

    else:
        if type(left) == int:
            left = [left]
        else:
            right = [right]
        return compare(left, right)


def bubble_sort(lista: list) -> None:
    """
    In place bubble sort

    Args:
        lista (list): The list to be sorted
    """
    length = len(lista)
    for passes in range(length - 1):

        riordinato = False
        for index in range(length - 1):
            if compare(lista[index], lista[index + 1]) is False:
                riordinato = True
                lista[index], lista[index + 1] = lista[index + 1], lista[index]

        if not riordinato:
            return 


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: list[str]) -> int:
    """
    Per ogni blocco di due pacchetti, usiamo eval per ricavare la lista dalla stringa.
    Usiamo compare() per compararli, e se sono in ordine, addiamo l'indice (1-indexed) a sol1.

    Args:
        data (list[str]): the input list

    Returns:
        int: the sum of the indexes of the correct ordered pairs of packets
    """
    sol1 = 0

    data = split_list(data)
    for n, pair in enumerate(data, start=1):
        left, right = [eval(x) for x in pair]
        comparison = compare(left, right)
        if comparison:
            sol1 += n

    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data: list[str]) -> int:
    """
    Togliamo le righe vuote dalla lista originaria, usiamo eval per ricavare la lista dalla stringa.
    Estendiamo la lista per aggiungere i due divider.
    Usiamo bubble_sort e compare() per compararli, e quando saranno in ordine, ci cerchiamo
    l'indice (sempre 1-indexed) dei due dividers, e li moltiplichiamo tra di loro.

    Args:
        data (list[str]): the input list

    Returns:
        int: the products of the indexes of the two dividers.
    """

    sol2 = 0
    indexes = []

    data = remove_empty_from_data(data)
    data = [eval(x) for x in data]
    dividers = [[[2]], [[6]]]
    data.extend(dividers)

    bubble_sort(data)

    for index, packet in enumerate(data, start=1):
        if packet in dividers:
            indexes.append(index)

    sol2 = indexes[0] * indexes[1]

    return sol2


s1 = part1(data)
s2 = part2(data)


print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
