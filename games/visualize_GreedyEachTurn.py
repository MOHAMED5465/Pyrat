# %% [markdown]
# <h1 style="background-color: gray;
#            color: black;
#            padding: 20px;
#            text-align: center;">INFO</h1>
# 
# In this script, we run player `Dijkstra` in a maze, to visualize its behavior.

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
from pyrat import Game
from GreedyEachTurn_opt import GreedyEachTurn

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
          'nb_cheese':41,
          'random_seed':80}

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

# Instantiate a player and add it to the game
player = GreedyEachTurn()
game.add_player(player)

# Start the game and
stats = game.start()

# %% [markdown]
# We visualize results using a pretty printer.

# %%
# Show statistics
pprint.pprint(stats)


