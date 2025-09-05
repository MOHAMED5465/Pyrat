#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player.
    In order to use this player, you need to instanciate it and add it to a game.
    Please refer to example games to see how to do it properly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import os
import sys
import enum

# Add needed directories to the path
this_directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_directory, "..", "utils"))

# PyRat imports
from pyrat import Player, Maze, GameState, Action
from BFSTraversal import BFSTraversal
from DFSTraversal import DFSTraversal
from 

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class TraversalAlgorithm (enum.Enum):

    """
        This enumeration defines all the algorithms supported by the TraversalPlayer.
        Values:
            * BFS: Breadth-first search.
            * DFS: Depth-first search.
    """

    BFS = "BFS"
    DFS = "DFS"
    Dijkstra="Dijkstra"

#####################################################################################################################################################

class TraversalPlayer (Player):

    """
        This player moves in the maze using a traversal algorithm.
        Several traversal algorithms are available, as defined in the TraversalAlgorithm enumeration.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:      Self,
                   algorithm: TraversalAlgorithm,
                   *args:     Any,
                   **kwargs:  Any
                 ) ->         Self:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:      Reference to the current object.
                * algorithm: The traversal algorithm to use.
                * args:      Arguments to pass to the parent constructor.
                * kwargs:    Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

        # Debug
        assert isinstance(algorithm, TraversalAlgorithm) # Type check for algorithm

        # The result will be computed in preprocessing and stored here
        self.actions = []

        # We use the chosen algorithm
        self.traversal_algorithm = None
        if algorithm == TraversalAlgorithm.BFS:
            self.traversal_algorithm = BFSTraversal()
        elif algorithm == TraversalAlgorithm.DFS:
            self.traversal_algorithm = DFSTraversal()
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################

    @override
    def preprocessing ( self:       Self,
                        maze:       Maze,
                        game_state: GameState,
                      ) ->          None:
        
        """
            This method redefines the method of the parent class.
            It is called once at the beginning of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * None.
        """
        
        # Perform the traversal to get the shortest paths from the player location to all the other cells
        self.traversal_algorithm.traversal(maze, game_state.player_locations[self.name])

        # Find the series of locations/actions to go from the player location to the first piece of cheese
        route = self.traversal_algorithm.find_route(game_state.cheese[0])
        self.actions = maze.locations_to_actions(route)

    #############################################################################################################################################

    @override
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Action:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Return the next action
        action = self.actions.pop(0)
        return action

#####################################################################################################################################################
#####################################################################################################################################################