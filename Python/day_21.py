"""
21: Step Counter ---
You manage to catch the airship right as it's dropping someone else off on their
all-expenses-paid trip to Desert Island! It even helpfully drops you off near the gardener and
his massive farm.

"You got the sand flowing again! Great work! Now we just need to wait until we have enough sand
to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are at solving
problems and would like your help. He needs to get his steps in for the day, and so he'd like to
know which garden plots he can reach with exactly his remaining 64 steps.

He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (
.), and rocks (#). For example:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take
one step north, south, east, or west, but only onto tiles that are garden plots. This would allow
him to reach any of the tiles marked O:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
Then, he takes a second step. Since at this point he could be at either tile marked O, his second
step would allow him to reach any garden plot that is one step north, south, east, or west of any
tile that he could have reached after the first step:

...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
After two steps, he could be at any of the tiles marked O above, including the starting position
(either by going north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
He will continue like this until his steps for the day have been exhausted. After a total of 6
steps, he could reach any of the garden plots marked O:

...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to
reach any of 16 garden plots.

However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger
than the example map.

Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in
exactly 64 steps?

Answer: 3572
"""

"""
--- Part Two ---
The Elf seems confused by your answer until he realizes his mistake: he was reading from a list 
of his favorite numbers that are both perfect squares and perfect cubes, not his step counter.

The actual number of steps he needs to get today is exactly 26501365.

He also points out that the garden plots and rocks are set up so that the map repeats infinitely 
in every direction.

So, if you were to look one additional map-width or map-height out from the edge of the example 
map above, you would find that it keeps repeating:

.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm layout; garden 
plots and rocks repeat as far as you can see. The Elf still starts on the one middle tile marked 
S, though - every other repeated S is replaced with a normal garden plot (.).

Here are the number of reachable garden plots in this new infinite version of the example map for 
different numbers of steps:

In exactly 6 steps, he can still reach 16 garden plots.
In exactly 10 steps, he can reach any of 50 garden plots.
In exactly 50 steps, he can reach 1594 garden plots.
In exactly 100 steps, he can reach 6536 garden plots.
In exactly 500 steps, he can reach 167004 garden plots.
In exactly 1000 steps, he can reach 668697 garden plots.
In exactly 5000 steps, he can reach 16733044 garden plots.
However, the step count the Elf needs is much larger! Starting from the garden plot marked S on 
your infinite map, how many garden plots could the Elf reach in exactly 26501365 steps?

Answer: 594606492802848
"""

from collections import deque

D = open('input/input_21.txt').read().strip()
L = D.split('\n')
G = [[c for c in row] for row in L]
R = len(G)
C = len(G[0])

for r in range(R):
    for c in range(C):
        if G[r][c] == 'S':
            sr, sc = r, c


def findD(r, c):
    D = {}
    Q = deque([(0, 0, sr, sc, 0)])
    while Q:
        tr, tc, r, c, d = Q.popleft()
        if r < 0:
            tr -= 1
            r += R
        if r >= R:
            tr += 1
            r -= R
        if c < 0:
            tc -= 1
            c += C
        if c >= C:
            tc += 1
            c -= C
        if not (0 <= r < R and 0 <= c < C and G[r][c] != '#'):
            continue
        if (tr, tc, r, c) in D:
            continue
        if abs(tr) > 4 or abs(tc) > 4:
            continue
        D[(tr, tc, r, c)] = d
        for dr, dc in [[-1, 0], [0, 1], [1, 0], [0, -1]]:
            Q.append((tr, tc, r + dr, c + dc, d + 1))
    return D


D = findD(sr, sc)

SOLVE = {}


def solve(d, v, L):
    amt = (L - d) // R
    if (d, v, L) in SOLVE:
        return SOLVE[(d, v, L)]
    ret = 0
    for x in range(1, amt + 1):
        if d + R * x <= L and (d + R * x) % 2 == (L % 2):
            ret += ((x + 1) if v == 2 else 1)
    SOLVE[(d, v, L)] = ret
    # print(f'd={d} v={v} L={L} R={R} amt={amt} ret={ret}')
    return ret


def solve21(part1):
    L = (64 if part1 else 26501365)
    ans = 0
    for r in range(R):
        for c in range(C):
            if (0, 0, r, c) in D:
                # print('='*20, r, c, D[(0,0,r,c)], '='*20)
                def fast(tr, tc):
                    ans = 0
                    B = 3
                    if tr > B:
                        ans += R * (abs(tr) - B)
                        tr = B
                    if tr < -B:
                        ans += R * (abs(tr) - B)
                        tr = -B
                    if tc > B:
                        ans += C * (abs(tc) - B)
                        tc = B
                    if tc < -B:
                        ans += C * (abs(tc) - B)
                        tc = -B
                    # print(tr,tc,r,c,D[(tr,tc,r,c)])
                    ans += D[(tr, tc, r, c)]
                    return ans

                # for tr in range(-8,8):
                #  msg = []
                #  for tc in range(-8,8):
                #    msg.append(str(D[(tr,tc,r,c)]))
                #  #print(' '.join(msg))
                # for tr in range(-8,8):
                #  for tc in range(-8,8):
                #    assert D[(tr,tc,r,c)]==fast(tr,tc), f'{tr} {tc} {D[(tr,tc,r,c)]} {fast(tr,tc)}'

                # How many ways are there to get a copy of (r,c) in L steps?
                # interior point: just check that point
                # edge: represents everything in that direction. can add arbitrarily many R to
                # distance
                # corner: represents everything in that quadrant. can add arbitrarily many R or C
                # to that distance

                # CEEEC
                # E...E
                # E...E
                # E...E
                # CEEEC
                assert R == C
                OPT = [-3, -2, -1, 0, 1, 2, 3]
                for tr in OPT:
                    for tc in OPT:
                        if part1 and (tr != 0 or tc != 0):
                            continue
                        d = D[(tr, tc, r, c)]
                        if d % 2 == L % 2 and d <= L:
                            ans += 1
                        if tr in [min(OPT), max(OPT)] and tc in [min(OPT), max(OPT)]:
                            ans += solve(d, 2, L)
                        elif tr in [min(OPT), max(OPT)] or tc in [min(OPT), max(OPT)]:
                            ans += solve(d, 1, L)
    return ans


print(solve21(True))
print(solve21(False))
