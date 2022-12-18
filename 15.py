from codetiming import Timer
from rich import print
from dataclassy import dataclass
from utils import (SESSIONS, get_data, MovingThing)



YEAR = 2022
DAY = 15
EXAMPLE = False


# Input parsing
with Timer(name="Parsing", text="Parsing done: \t{milliseconds:.0f} ms"):
    """
    We'll parse the input line beacon_y line. 
    """
    data = get_data(YEAR, DAY, SESSIONS, strip=True, example=EXAMPLE)
    beacons = {}
    for line in data:
        sensor, beacon = line.split(': closest beacon is at')
        sensor = sensor.split(',')
        sensor_x = int(sensor[0].split('=')[-1])
        sensor_y = int(sensor[1].split('=')[-1])
        beacon = beacon.split(',')
        beacon_x = int(beacon[0].split('=')[-1])
        beacon_y = int(beacon[1].split('=')[-1])
        beacons[(sensor_x, sensor_y)] = (beacon_x, beacon_y)

    data = beacons

    def segments_overlap(a, b) -> bool:
        return (
            (a[0] <= b[0] <= a[1]) or 
            (b[0] <= a[1] <= b[1]) or
            (b[0] <= a[0] <= b[1]) or
            (a[0] <= b[1] <= a[1])
            )

    def segmento_sum(segmento1, segmento2) -> tuple:
        return (min(segmento1[0], segmento2[0]), max(segmento1[1], segmento2[1]))


# Part 1
@Timer(name="Part 1", text="Part 1 done: \t{milliseconds:.0f} ms")
def part1(data, y=2000000):
    if EXAMPLE:
        y = 10


    sol1 = 0
    segments = []
    for sensor, beacon in data.items():
        sensor_x, sensor_y = sensor
        beacon_x, beacon_y = beacon
        man_dist =  abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        row_to_be_found = y
        lunghezza_row = ((man_dist + man_dist) + 1) - (abs(1*(row_to_be_found - sensor_y))*2)
        if lunghezza_row > 0:
            half = lunghezza_row//2
            begin = sensor_x - half
            end = sensor_x + half
            segments.append((begin, end))

    segmento = segments[0]

    stop = False

    segmenti_sums = []
    while segments:
        stop = False
        while not stop:
            stop = True
            for _, segmento_candidato in enumerate(segments[1:].copy()):
                segmento = segments[0]
                if segments_overlap(segmento, segmento_candidato):
                    stop = False
                    segments.pop(0)
                    segments.remove(segmento_candidato)
                    segments.insert(0, segmento_sum(segmento, segmento_candidato))
        single_segment = segments.pop(0)
        segmenti_sums.append(single_segment)

    for segment in segmenti_sums:
        sol1 += (segment[1] - segment[0])


    return sol1


# Part 2
@Timer(name="Part 2", text="Part 2 done: \t{milliseconds:.0f} ms")
def part2(data) -> int:

    LIMIT = 4_000_000

    sol2 = 0

    for y in range(0, LIMIT+1):
        sol1 = 0
        segments = []
        for sensor, beacon in data.items():
            sensor_x, sensor_y = sensor
            beacon_x, beacon_y = beacon
            man_dist =  abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
            row_to_be_found = y
            lunghezza_row = ((man_dist + man_dist) + 1) - (abs(1*(row_to_be_found - sensor_y))*2)
            if lunghezza_row > 0:
                half = lunghezza_row//2
                begin = sensor_x - half
                end = sensor_x + half
                if begin < 0:
                    begin = 0
                if end > LIMIT:
                    end = LIMIT
                segments.append((begin, end))

        segmento = segments[0]

        stop = False
        segmenti_sums = []
        while segments:
            stop = False
            while not stop:
                stop = True
                for segmento_candidato in segments[1:].copy():
                    segmento = segments[0]
                    if segments_overlap(segmento, segmento_candidato):
                        stop = False
                        segments.pop(0)
                        segments.remove(segmento_candidato)
                        segments.insert(0, segmento_sum(segmento, segmento_candidato))
            single_segment = segments.pop(0)
            segmenti_sums.append(single_segment)

        for segment in segmenti_sums:
            sol1 += (segment[1] - segment[0])

        if len(segmenti_sums) == 2 and sol1 == LIMIT - 2:
            sol2 = f"{(((sorted(segmenti_sums)[0][1])+1)*LIMIT)+y}"
            sol2 += f" or {(((sorted(segmenti_sums)[0][1])+2)*LIMIT)+y}"
            break
    
    return sol2


s1 = part1(data)
s2 = part2(data)


print("=========================")
print(f"Soluzione Parte 1: [{s1}]")
print(f"Soluzione Parte 2: [{s2}]")
