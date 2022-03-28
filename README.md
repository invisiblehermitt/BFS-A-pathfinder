The program must be able to be run as follows:
$ python pathfinder.py [map] [algorithm] [heuristic]
The inputs/options to the program are as follows.
• [map] specifies the path to map, which is a text file formatted according to this
example :
10 10
1 1
10 10
1 1 1 1 1 1 4 7 8 X
1 1 1 1 1 1 1 5 8 8
1 1 1 1 1 1 1 4 6 7
1 1 1 1 1 X 1 1 3 6
1 1 1 1 1 X 1 1 1 1
1 1 1 1 1 1 1 1 1 1
6 1 1 1 1 X 1 1 1 1
7 7 1 X X X 1 1 1 1
8 8 1 1 1 1 1 1 1 1
X 8 7 1 1 1 1 1 1 1


The first line indicates the size of the map (rows by columns), while the second and third line represent the start and end positions respectively. The map data then follows, where all elevation values are integers from 0 to 9 inclusive.
• [algorithm] specifies the search algorithm to use, with the possible values of bfs,
ucs, and astar.
• [heuristic] specifies the heuristic to use for A* search, with the possible values of euclidean and manhattan. This input is ignored for BFS and UCS.

only four actions are available: Up, down, left and right
X represents the obstacle, and the position with X can't be reached.

The program will then print to standard output the path returned by the search algorithm, in the following format:
* * * 1 1 1 4 7 8 X
1 1 * 1 1 1 1 5 8 8
1 1 * * * * * * * 7
1 1 1 1 1 X 1 1 * 6
1 1 1 1 1 X 1 * * 1
1 1 1 1 1 1 1 * 1 1
6 1 1 1 1 X 1 * * *
7 7 1 X X X 1 1 1 *
8 8 1 1 1 1 1 1 1 *
X 8 7 1 1 1 1 1 1 *
where the path is indicated by asterisks ‘*’ superimposed on the original map beginning
from the start position and leading to the end position. Do not include extraneous
spaces or other characters in the output.
If the given map or problem does not have a feasible path, the program will print null
