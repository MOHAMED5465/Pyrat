import sys
import os
import time
from pyrat import BigHolesRandomMaze, MazeFromDict
this_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_directory, "..", "players"))
from GreedyEachTurn_opt import GreedyEachTurn
player=GreedyEachTurn()

MUD_PERCENTAGE = 20.0

maze = BigHolesRandomMaze(width = 6,
                            height = 5,
                            cell_percentage = 80,
                            wall_percentage = 60,
                            mud_percentage = MUD_PERCENTAGE,
                            mud_range=(4, 9))
d=maze.as_dict()
print(d)
start_time = time.perf_counter()
peices_of_cheese=[5,10,22]
print(player.meta_graph(maze,0,peices_of_cheese))
end_time = time.perf_counter()
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")