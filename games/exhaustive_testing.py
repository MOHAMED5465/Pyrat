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

# Add needed directories to the path

this_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_directory, "..", "players"))

# PyRat imports
from pyrat import Game
from Exhaustive import Exhaustive

# %% [markdown]
# <h1 style="background-color: gray;
#            color: black;
#            padding: 20px;
#            text-align: center;">CONSTANTS</h1>
# 
# Let's configure the game with a dictionary.

# %%
# Customize the game elements
CONFIG = {"mud_percentage": 30.0,
          "nb_cheese": 5,
          "random_seed": 68,
          "trace_length": 1000}

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
player = Exhaustive()
game.add_player(player)

# Start the game and
stats = game.start()

