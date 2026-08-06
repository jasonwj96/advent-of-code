"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant
"garden" that looks
more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't
receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with
dirty water.
Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days...
weeks... oh no." His face
sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we
stopped
getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much
faster than your
boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the
ferry,
maybe you can help us with our food production problem. The latest Island Island Almanac just
arrived and we're
having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists
what type
of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil,
what type
of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so
on is identified with a number, but numbers are reused by each category - that is, soil 123 and
fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source
category into numbers in a destination category. That is, the section that starts with
seed-to-soil map:
describes how to convert a seed number (the source) to a soil number (the destination). This lets
the gardener and his team know which soil to use with which seeds, which water to use with which
fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps
describe entire ranges of numbers that can be converted. Each line within a map contains three
numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48

The first line has a destination range start of 50, a source range start of 98, and a range
length of 2.
This line means that the source range starts at 98 and contains two values: 98 and 99. The
destination
range is the same length, but it starts at 50, so its two values are 50 and 51. With this
information,
you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to
soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96,
97.
This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53,
..., 98, 99.
So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number
10 corresponds to
soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51

With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the
closest location that needs a seed. Using these maps, find the lowest location number that
corresponds to any of the initial seeds. To do this, you'll need to convert each seed number
through other categories until you can find its corresponding location number. In this example,
the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

----------------------------
0 seeds        |79|14|55|13|
----------------------------
1 soil         |81|14|57|13|
----------------------------
2 fertilizer   |81|53|57|52|
----------------------------
3 water        |81|49|53|41|
----------------------------
4 light        |74|42|46|34|
----------------------------
5 temperature  |78|42|82|34|
----------------------------
6 humidity     |78|43|82|35|
----------------------------
7 location     |82|43|86|35|
----------------------------

Answer: 318728750

"""
"""
--- Part Two ---

Everyone will starve if you only plant such a small number of seeds.
Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs.
Within each pair, the first value is the start of the range
and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13

This line describes two ranges of seed numbers to be planted in the garden.
The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92.
The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82,
which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46,
and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac.
What is the lowest location number that corresponds to any of the initial seed numbers?

Answer: 37384986

"""

import math

lines: list()

with open("input/input_5.txt") as file:
    lines = file.read().splitlines()


def part1():
    seeds = list()
    locations = list()

    for line in lines:
        if line.startswith('seeds:'):
            for num in line.split(':')[1].strip().split(' '):
                seeds.append(int(num))
        break

    for seed in seeds:
        location = seed
        found = False
        for line in lines:
            if ':' in line or line == '':
                found = False
                continue
            if found:
                continue

            nums = line.split(' ')
            destination = int(nums[0])
            source = int(nums[1])
            length = int(nums[2])

            if source <= location <= source + length:
                location = destination + location - source
                found = True

        locations.append(location)

    return min(locations)


def part2():
    seed_ranges = list()
    maps = list()
    map_section = list()
    for line in lines:
        if line.startswith('seeds:'):
            s_range = list()
            for num in line.split(':')[1].strip().split(' '):
                if len(s_range) == 0:
                    s_range.append(int(num))
                else:
                    s_range.append(s_range[0] + int(num))
                    seed_ranges.append(s_range)
                    s_range = list()
            continue

        if ':' in line or line == '':
            if len(map_section) > 0:
                maps.append(map_section)
                map_section = list()
            continue

        nums = line.split(' ')
        map_section.append([
            int(nums[0]),
            int(nums[1]),
            int(nums[1]) + int(nums[2]) - 1,
        ])
    if map_section not in maps:
        maps.append(map_section)

    for current_map in maps:
        new_seed_ranges = list()
        for index, seed_range in enumerate(seed_ranges):
            for map in current_map:
                convert = map[0] - map[1]
                # not within range at all
                if (seed_range[0] < map[1] and seed_range[1] < map[1]) or (
                        seed_range[0] > map[2] and seed_range[1] > map[2]):
                    continue

                # seed range completely within map range
                if seed_range[0] >= map[1] and seed_range[1] <= map[2]:
                    seed_ranges[index] = [
                        seed_range[0] + convert,
                        seed_range[1] + convert,
                    ]
                    break
                # first seed number outside of map range
                elif seed_range[0] < map[1]:
                    # second seed number within map range
                    if seed_range[1] <= map[2]:
                        # continue with the part of seed range which is outside
                        seed_ranges[index] = [
                            seed_range[0],
                            map[1] - 1
                        ]
                        # add part within map range as new seed for next map section
                        new_seed_ranges.append([
                            map[1] + convert,
                            seed_range[1] + convert,
                        ])
                    # second seed number outside of map range (seed range over extends both ways)
                    else:
                        # add whole range
                        new_seed_ranges.append([
                            map[1] + convert,
                            map[2] + convert,
                        ])
                        # redo range part too low
                        seed_ranges[index] = [
                            seed_range[0],
                            map[1] - 1
                        ]
                        # redo range part too high
                        seed_ranges.append([
                            map[2] + 1,
                            seed_range[1],
                        ])
                # first seed part is within range
                else:
                    seed_ranges[index] = [
                        map[2],
                        seed_range[1],
                    ]
                    new_seed_ranges.append([
                        seed_range[0] + convert,
                        map[0] + map[2] - map[1],
                    ])
                seed_range = seed_ranges[index]
        seed_ranges += new_seed_ranges

    minimum = math.inf
    for seed in seed_ranges:
        if seed[0] < minimum:
            minimum = seed[0]
    return minimum


print(f"Part 1: {str(part1())}")
print(f"Part 2: {str(part2())}")
