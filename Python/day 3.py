"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you
up to
the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't
expecting anyone!
The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer
to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure
out which one. If
you can add up all the part numbers in the engine schematic, it should be easy to work out which
part
is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There
are
lots of numbers
and symbols you don't really understand, but apparently any number adjacent to a symbol,
even diagonally,
is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114
(top right) and 58 (middle right).
Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all the part numbers \
in the engine schematic?

Answer: 519444
"""
"""
--- Part Two ---
The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure 
why the water stopped;
however, he can show you how to get to the water source to check it out for yourself. It's just 
up ahead!

As you continue your walk, the Elf poses a second question: in each game you played, what is the 
fewest number of cubes
of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If 
any color had even one
fewer cube, the game would have been impossible.

Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.

The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied 
together. The power of the
minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. 
Adding up these five
powers
produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the 
power of these sets?

Answer: 74528807
"""

grid = open('input/input_3.txt').read().splitlines()
memory = set()

# Part 1
for i, row in enumerate(grid):
    for j, char in enumerate(row):
        if char.isdigit() or char == ".":
            continue
        for dr in range(i - 1, i + 2):
            for dc in range(j - 1, j + 2):
                if dr < 0 or dr >= len(grid) or dc < 0 or dc >= len(grid[dr]) or not grid[dr][dc].isdigit():
                    continue
                while dc > 0 and grid[dr][dc - 1].isdigit():
                    dc -= 1
                memory.add((dr, dc))

ns = []

for i, j in memory:
    s = ""
    while j < len(grid[i]) and grid[i][j].isdigit():
        s += grid[i][j]
        j += 1
    ns.append(int(s))

print(f"Part 1: {sum(ns)}")

total = 0

# Part 2
for i, row in enumerate(grid):
    for j, char in enumerate(row):
        if char != "*":
            continue

        memory = set()

        for cr in [i - 1, i, i + 1]:
            for cc in [j - 1, j, j + 1]:
                if cr < 0 or cr >= len(grid) or cc < 0 or cc >= len(grid[cr]) or not grid[cr][cc].isdigit():
                    continue
                while cc > 0 and grid[cr][cc - 1].isdigit():
                    cc -= 1
                memory.add((cr, cc))

        if len(memory) != 2:
            continue

        ns = []

        for cr, cc in memory:
            s = ""
            while cc < len(grid[cr]) and grid[cr][cc].isdigit():
                s += grid[cr][cc]
                cc += 1
            ns.append(int(s))

        total += ns[0] * ns[1]

print(f"Part 2: {total}")
