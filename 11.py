from pprint import pprint as pp
import math

from codetiming import Timer
from rich import print
from dataclassy import dataclass
from utils import (SESSIONS, get_data, split_list)


YEAR = 2022
DAY = 11

@dataclass
class Monkey:
    """
    This is the base class for a monkey.
    Items is a list of items they are holding,
    op is a string describing a simple operation, eg. 'old + 3'
    divisible_by is the  factor to test divisibility by,
    is_true and is_false are the indexes of the target monkey if such a test will pass or fail,
    inspected is the number of item inspected.
    """
    items: list[int] = None
    op: str = "new = old"
    divisible_by: int = 1
    if_true: int
    if_false: int
    inspected: int = 0

    def do_monkey_things(self, monkeys: list):
        """
        This is the part1 modus operandi for the monkeys.
        First of all, for each item they are holding, they execute a basic operation, done with eval() because we have a string.
        Then, the item is divided and floored by 3.
        Then, if the item is divisible by divisible_by, we pass it to the monkey with index if_true in the monkeys list,
        else we pass it to the monkey with index if_false in the monkey list.
        We'll increment inspected by one.
        We'll clear the list of items held.
        """
        for item in self.items.copy():

            old = item  # This will be referred by the eval in the next line
            item = eval(self.op)

            item = item//3

            if item % self.divisible_by == 0:
                monkeys[self.if_true].items.append(item)
            else:
                monkeys[self.if_false].items.append(item)

            self.inspected += 1

        self.items.clear()

    def do_monkey_things_p2(self, monkeys: list):
        """
        This is the part2 modus operandi for the monkeys.
        Because we no longer divide by 3, the numbers themselves will reach 500 digits by round 40. So we have to change things around.
        First of all, we calculate the least common multiple of al divisible_by numbers of all the monkeys-
        Then, for each item they are holding, they execute a basic operation, done with eval() because we have a string.
        After that, if the item is divisible by divisible_by, we pass the modulo of the number and the least common multiple to the monkey with index if_true in the monkeys list,
        else we pass the modulo of the number and the least common multiple to to the monkey with index if_false in the monkey list.
        We'll increment inspected by one.
        We'll clear the list of items held.
        """
        mcm = math.prod(x.divisible_by for x in monkeys)
        for item in self.items.copy():

            old = item
            item = eval(self.op)

            if item % self.divisible_by == 0:
                item = item % mcm
                monkeys[self.if_true].items.append(item)
            else:
                item = item % mcm
                monkeys[self.if_false].items.append(item)

            self.inspected += 1

        self.items.clear()

# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line by line. 
    We split the list where there is an empty line, so we can parse later block-by-block
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=False)
    data = split_list(data)


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data: list[str]):
    """
    For each block we instance a Monkey() parsing the list of items, the operation they do, the divisibile by criterion and the two possibile outputs.
    For a number of rounds, for each round, each monkey will do_monkey_things().
    In the end, we grab the two monkeys who have inspected more items, and multiply the numbers together.
    """
    sol1 = 0
    monkeys: list[Monkey] = []

    for monkey in data:
        items = [int(x.strip()) for x in monkey[1].split('Starting items: ')[-1].split(',')]
        op = monkey[2].split('Operation: ')[-1].split(' = ')[-1]
        divisible_by = int(monkey[3].split(' ')[-1])
        if_true = int(monkey[4].split(' ')[-1])
        if_false = int(monkey[5].split(' ')[-1])
        monkeys.append(Monkey(items=items, op=op, divisible_by=divisible_by, if_true=if_true, if_false=if_false))

    for i in range(20):
        for monkey in monkeys:
            monkey.do_monkey_things(monkeys)
  
    monkey_business = list(sorted([x.inspected for x in monkeys], reverse=True))[:2]
    sol1 = math.prod(monkey_business)


    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data):
    """
    For each block we instance a Monkey() parsing the list of items, the operation they do, the divisibile criterion and the two possibile outputs.
    For a number of rounds, for each round, each monkey will do_monkey_things_p2().
    In the end, we grab the two monkeys who have inspected more items, and multiply the numbers together.
    """

    sol2 = 0
    monkeys: list[Monkey] = []

    for monkey in data:
        items = [int(x.strip()) for x in monkey[1].split('Starting items: ')[-1].split(',')]
        op = monkey[2].split('Operation: ')[-1].split(' = ')[-1]
        divisible_by = int(monkey[3].split(' ')[-1])
        if_true = int(monkey[4].split(' ')[-1])
        if_false = int(monkey[5].split(' ')[-1])
        monkeys.append(Monkey(items=items, op=op, divisible_by=divisible_by, if_true=if_true, if_false=if_false))
    

    for i in range(10000):
        for monkey in monkeys:
            monkey.do_monkey_things_p2(monkeys)

    monkey_business = list(sorted([x.inspected for x in monkeys], reverse=True))[:2]
    sol2 = math.prod(monkey_business)
    return sol2


s1 = part1(data)
s2 = part2(data)

print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
