"""
--- Day 23: A Long Walk ---
The Elves resume water filtering operations! Clean water starts flowing over the edge of Island
Island.

They offer to help you go over the edge of Island Island, too! Just hold on tight to one end of
this impossibly long rope and they'll lower you down a safe distance from the massive waterfall
you just created.

As you finally reach Snow Island, you see that the water isn't really reaching the ground: it's
being absorbed by the air itself. It looks like you'll finally have a little downtime while the
moisture builds up to snow-producing levels. Snow Island is pretty scenic, even without any snow;
why not take a walk?

There's a map of nearby hiking trails (your puzzle input) that indicates paths (.), forest (#),
and steep slopes (^, >, v, and <).

For example:

#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
You're currently on the single path tile in the top row; your goal is to reach the single path
tile in the bottom row. Because of all the mist from the waterfall, the slopes are probably quite
icy; if you step onto a slope tile, your next step must be downhill (in the direction the arrow
is pointing). To make sure you have the most scenic hike possible, never step onto the same tile
twice. What is the longest hike you can take?

In the example above, the longest hike you can take is marked with O, and your starting position
is marked S:

#S#####################
#OOOOOOO#########...###
#######O#########.#.###
###OOOOO#OOO>.###.#.###
###O#####O#O#.###.#.###
###OOOOO#O#O#.....#...#
###v###O#O#O#########.#
###...#O#O#OOOOOOO#...#
#####.#O#O#######O#.###
#.....#O#O#OOOOOOO#...#
#.#####O#O#O#########v#
#.#...#OOO#OOO###OOOOO#
#.#.#v#######O###O###O#
#...#.>.#...>OOO#O###O#
#####v#.#.###v#O#O###O#
#.....#...#...#O#O#OOO#
#.#########.###O#O#O###
#...###...#...#OOO#O###
###.###.#.###v#####O###
#...#...#.#.>.>.#.>O###
#.###.###.#.###.#.#O###
#.....###...###...#OOO#
#####################O#
This hike contains 94 steps. (The other possible hikes you could have taken were 90, 86, 82, 82,
and 74 steps long.)

Find the longest hike you can take through the hiking trails listed on your map. How many steps
long is the longest hike?

Answer: 2130
"""

"""
--- Part Two ---
As you reach the trailhead, you realize that the ground isn't as slippery as you expected; you'll 
have no problem climbing up the steep slopes.

Now, treat all slopes as if they were normal paths (.). You still want to make sure you have the 
most scenic hike possible, so continue to ensure that you never step onto the same tile twice. 
What is the longest hike you can take?

In the example above, this increases the longest hike to 154 steps:

#S#####################
#OOOOOOO#########OOO###
#######O#########O#O###
###OOOOO#.>OOO###O#O###
###O#####.#O#O###O#O###
###O>...#.#O#OOOOO#OOO#
###O###.#.#O#########O#
###OOO#.#.#OOOOOOO#OOO#
#####O#.#.#######O#O###
#OOOOO#.#.#OOOOOOO#OOO#
#O#####.#.#O#########O#
#O#OOO#...#OOO###...>O#
#O#O#O#######O###.###O#
#OOO#O>.#...>O>.#.###O#
#####O#.#.###O#.#.###O#
#OOOOO#...#OOO#.#.#OOO#
#O#########O###.#.#O###
#OOO###OOO#OOO#...#O###
###O###O#O###O#####O###
#OOO#OOO#O#OOO>.#.>O###
#O###O###O#O###.#.#O###
#OOOOO###OOO###...#OOO#
#####################O#
Find the longest hike you can take through the surprisingly dry hiking trails listed on your map. 
How many steps long is the longest hike?

Answer: 6710
"""
import sys
from collections import deque

D = open('input/input_23.txt').read().strip()
L = D.split('\n')
G = [[c for c in row] for row in L]
R = len(G)
C = len(G[0])

sys.setrecursionlimit(10 ** 6)


def solve(part1):
    V = set()
    for r in range(R):
        for c in range(C):
            nbr = 0
            for ch, dr, dc in [['^', -1, 0], ['v', 1, 0], ['<', 0, -1], ['>', 0, 1]]:
                if (0 <= r + dr < R and 0 <= c + dc < C and G[r + dr][c + dc] != '#'):
                    nbr += 1
            if nbr > 2 and G[r][c] != '#':
                V.add((r, c))

    for c in range(C):
        if G[0][c] == '.':
            V.add((0, c))
            start = (0, c)
        if G[R - 1][c] == '.':
            V.add((R - 1, c))
            end = (R - 1, c)

    E = {}
    for (rv, cv) in V:
        E[(rv, cv)] = []
        Q = deque([(rv, cv, 0)])
        SEEN = set()
        while Q:
            r, c, d = Q.popleft()
            if (r, c) in SEEN:
                continue
            SEEN.add((r, c))
            if (r, c) in V and (r, c) != (rv, cv):
                E[(rv, cv)].append(((r, c), d))
                continue
            for ch, dr, dc in [['^', -1, 0], ['v', 1, 0], ['<', 0, -1], ['>', 0, 1]]:
                if (0 <= r + dr < R and 0 <= c + dc < C and G[r + dr][c + dc] != '#'):
                    if part1 and G[r][c] in ['<', '>', '^', 'v'] and G[r][c] != ch:
                        continue
                    Q.append((r + dr, c + dc, d + 1))

    count = 0
    ans = 0
    SEEN = [[False for _ in range(C)] for _ in range(R)]
    seen = set()

    def dfs(v, d):
        nonlocal count
        nonlocal ans
        count += 1
        r, c = v
        if SEEN[r][c]:
            return
        SEEN[r][c] = True
        if r == R - 1:
            ans = max(ans, d)
        for (y, yd) in E[v]:
            dfs(y, d + yd)
        SEEN[r][c] = False

    dfs(start, 0)
    # print(count)
    return ans


print(solve(True))
print(solve(False))
