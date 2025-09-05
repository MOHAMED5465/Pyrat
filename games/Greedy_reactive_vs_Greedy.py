# %% [markdown]
# <h1 style="background-color: gray;
#            color: black;
#            padding: 20px;
#            text-align: center;">INFO</h1>
# 
# This script creates a sample game, in which two players compete in the maze.

# %% [markdown]
# <h1 style="background-color: gray;
#            color: black;
#            padding: 20px;
#            text-align: center;">IMPORTS</h1>

# %%
# External imports
import sys
import os
import pprint

# Add needed directories to the path
this_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_directory, "..","players"))

# PyRat imports
from   pyrat import *
from Greedy import Greedy
#from GreedyEachTurn_opt import GreedyEachTurn
#from GreedyEachCheese import GreedyEachCheese
from GreedyEachTurn_opt import GreedyEachTurn
from two_opt_reactive import Two_opt_reactive
from two_opt import Two_opt

# %% [markdown]
# <h1 style="background-color: gray;
#            color: black;
#            padding: 20px;
#            text-align: center;">CONSTANTS</h1>
# 
# Let's configure the game with a dictionary.

# %%
# Customize the game elements
CONFIG = {'maze_width': 25,
          'maze_height': 20,
          'cell_percentage': 80.0,
          'wall_percentage': 60.0,
          'mud_percentage': 20.0,
          'mud_range': [4, 9],
          'preprocessing_time': 3.0,
          'turn_time': 0.1,
          'random_seed':100,
          'nb_cheese': 15}

# %% [markdown]
# <h1 style="background-color: gray;
#            color: black;
#            padding: 20px;
#            text-align: center;">RUN THE GAME</h1>

# %% [markdown]
# We perform a single game with the configuration defined above.

# %%
# Instantiate a game with specified arguments
game = Game(**CONFIG)
pprint.pprint(game.maze.vertices)
# Instantiate players in distinct teams
player_1=Two_opt()
game.add_player(player_1, team="Team Ratz", location=StartingLocation.RANDOM)
player_2=Greedy()
game.add_player(player_2, team="Team Pythons", location=StartingLocation.RANDOM)
# Start the game
stats = game.start()

# %% [markdown]
# We visualize results using a pretty printer.

# %%
# Show statistics
pprint.pprint(stats)
