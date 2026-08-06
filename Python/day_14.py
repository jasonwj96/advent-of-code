"""
--- Part One ---

--- Day 14: Parabolic Reflector Dish ---
You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side
of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic
reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to
focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where
it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and
pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending
on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes
move and ultimately the focus of the dish.+

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets
you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the
cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your
puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....

You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't
collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge
of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount
of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1

The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support
beams?

Answer: 105249

"""
from functools import cache

"""
--- Part Two ---
The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the 
rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" 
attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. 
After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one 
cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O

This process should work if you leave it running long enough, but you're still worried about the north support beams. 
To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 
1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?
"""


def calculate_score(lines):
    count = 0
    for i, l in enumerate(lines):
        for j, c in enumerate(l):
            if c == 'O':
                count += len(lines) - i

    return count


@cache
def tilt(grid, direction):
    grid = [list(row) for row in grid]

    grid_range = range(len(grid)) if -1 not in direction else range(len(grid) - 1, -1, -1)

    column = direction[1] == 0
    row = direction[0] == 0

    free_space = dict()

    for index1 in grid_range:
        column = index1 if column else 0
        row = index1 if row else 0

        for index2 in grid_range:
            column = index2 if column else index1
            row = index2 if row else index1
            cell = grid[column][row]

            key = row if column else column
            current_free = free_space.get(key, None)

            if cell == '.':
                free_space[key] = (column, row) if current_free is None else current_free
            elif cell == '#':
                free_space[key] = None
            else:
                if current_free is not None:
                    free_space_loc = free_space[key]

                    grid[free_space_loc[0]][free_space_loc[1]] = cell
                    grid[column][row] = '.'

                    new_col = free_space_loc[0] if row else free_space_loc[0] + direction[0]
                    new_row = free_space_loc[1] if column else free_space_loc[1] + direction[1]

                    free_space[key] = (new_col, new_row)

    return grid


def part_1(file):
    lines = [list(row) for row in file.read().splitlines()]

    for i, l in enumerate(lines):
        if i == 0:
            continue
        for j, char in enumerate(l):
            if char == 'O' and lines[i - 1][j] not in 'O#':
                lower_bound = i
                while lower_bound > 0 and lines[lower_bound - 1][j] == '.':
                    lower_bound -= 1

                lines[lower_bound][j], lines[i][j] = lines[i][j], lines[lower_bound][j]

    return calculate_score(lines)


def part_2(file):
    lines = list()

    for line in file:
        lines.append([c for c in line.rstrip()])

    grid = [line.copy() for line in lines]
    prev_grids = dict()

    for index in range(1000000000):
        prev_grids[str(grid)] = index
        for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            grid = tilt(tuple(tuple(row) for row in grid), direction)

        if str(grid) in prev_grids:
            index += 1
            prev_index = prev_grids[str(grid)]
            difference = index - prev_index

            grid_indexes = dict()

            for k, v in prev_grids.items():
                grid_indexes[v] = k

            grid = eval(grid_indexes[((1000000000 - prev_index) % difference) + prev_index])
            break

    return calculate_score(grid)


with open('input/input_14.txt') as file:
    print(f'Part 1: {part_1(file)}')

with open('input/input_14.txt') as file:
    print(f'Part 2: {part_2(file)}')
