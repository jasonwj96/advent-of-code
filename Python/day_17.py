"""
--- Day 17: Clumsy Crucible ---

The lava starts flowing rapidly once the Lava Production Facility is
operational. As you leave, the reindeer offers
you a parachute, allowing you to quickly reach Gear Island.

As you descend, your bird's-eye view of Gear Island reveals why you had
trouble finding anyone on your way up: half
of Gear Island is empty, but the half below you is a giant factory city!

You land near the gradually-filling pool of lava at the base of your new
lavafall. Lavaducts will eventually carry
the lava throughout the city, but to make use of it immediately, Elves are
loading it into large crucibles on wheels.

The crucibles are top-heavy and pushed by hand. Unfortunately, the crucibles
become very difficult to steer at high
speeds, and so it can be hard to go in a straight line for very long.

To get Desert Island the machine parts it needs as soon as possible, you'll
need to find the best way to get the
crucible from the lava pool to the machine parts factory. To do this,
you need to minimize heat loss while choosing a
route that doesn't require the crucible to go in a straight line for too long.

Fortunately, the Elves here have a map (your puzzle input) that uses traffic
patterns, ambient temperature,
and hundreds of other parameters to calculate exactly how much heat loss can
be expected for a crucible entering any
particular city block.

For example:

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533

Each city block is marked by a single digit that represents the amount of
heat loss if the crucible enters that
block. The starting point, the lava pool, is the top-left city block; the
destination, the machine parts factory,
is the bottom-right city block. (Because you already start in the top-left
block, you don't incur that block's heat
loss unless you leave that block and then return to it.)

Because it is difficult to keep the top-heavy crucible going in a straight
line for very long, it can move at most
three blocks in a single direction before it must turn 90 degrees left or
right. The crucible also can't reverse
direction; after entering each city block, it may only turn left, continue
straight, or turn right.

One way to minimize heat loss is this path:

2>>34^>>>1323
32v>>>35v5623
32552456v>>54
3446585845v52
4546657867v>6
14385987984v4
44578769877v6
36378779796v>
465496798688v
456467998645v
12246868655<v
25465488877v5
43226746555v>

This path never moves more than three consecutive blocks in the same
direction and incurs a heat loss of only 102.

Directing the crucible from the lava pool to the machine parts factory,
but not moving more than three consecutive
blocks in the same direction, what is the least heat loss it can incur?

Answer: 817

"""
"""
--- Part Two ---
The crucibles of lava simply aren't large enough to provide an adequate supply of lava to the 
machine parts factory. Instead, the Elves are going to upgrade to ultra crucibles.

Ultra crucibles are even more difficult to steer than normal crucibles. Not only do they have 
trouble going in a straight line, but they also have trouble turning!

Once an ultra crucible starts moving in a direction, it needs to move a minimum of four blocks in 
that direction before it can turn (or even before it can stop at the end). However, 
it will eventually start to get wobbly: an ultra crucible can move a maximum of ten consecutive 
blocks without turning.

In the above example, an ultra crucible could follow this path to minimize heat loss:

2>>>>>>>>1323
32154535v5623
32552456v4254
34465858v5452
45466578v>>>>
143859879845v
445787698776v
363787797965v
465496798688v
456467998645v
122468686556v
254654888773v
432267465553v
In the above example, an ultra crucible would incur the minimum possible heat loss of 94.

Here's another example:

111111111111
999999999991
999999999991
999999999991
999999999991
Sadly, an ultra crucible would need to take an unfortunate path like this one:

1>>>>>>>1111
9999999v9991
9999999v9991
9999999v9991
9999999v>>>>
This route causes the ultra crucible to incur the minimum possible heat loss of 71.

Directing the ultra crucible from the lava pool to the machine parts factory, what is the least 
heat loss it can incur?

Answer: 925 

"""

import sys

sys.setrecursionlimit(1000000)
import heapq

grid = list()

with open('input/input_17.txt') as f:
    for line in f:
        grid.append([int(cell) for cell in line.rstrip()])

up = (-1, 0)
down = (1, 0)
left = (0, -1)
right = (0, 1)

TARGET = (len(grid) - 1, len(grid[0]) - 1)


def pathfind(grid, min_total_direction, max_total_direction):
    visited = set()
    directions_to_go = [(0, 0, 0, right, 1), (0, 0, 0, down, 1)]
    heapq.heapify(directions_to_go)

    while len(directions_to_go) > 0:
        total, y, x, direction, total_direction = heapq.heappop(directions_to_go)

        if (y, x, direction, total_direction) in visited:
            continue
        else:
            visited.add((y, x, direction, total_direction))

        if total_direction > max_total_direction:
            continue

        coord = (y + direction[0], x + direction[1])

        if coord[0] < 0 or coord[0] >= len(grid) or coord[1] < 0 or coord[1] >= len(grid[0]):
            continue

        total += grid[coord[0]][coord[1]]

        if total_direction >= min_total_direction and coord[0] == TARGET[0] and coord[1] == TARGET[
            1]:
            return total

        for d in [up, down, left, right]:
            if d[0] + direction[0] == 0 and d[1] + direction[1] == 0:
                continue
            if d != direction and total_direction < min_total_direction:
                continue
            new_total_dir = 1 if d != direction else total_direction + 1
            heapq.heappush(directions_to_go, (total, coord[0], coord[1], d, new_total_dir))


def part1():
    return pathfind(grid, 0, 3)


def part2():
    return pathfind(grid, 4, 10)


print(f"Part 1: {str(part1())}")
print(f"Part 2: {str(part2())}")
