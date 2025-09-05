#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a traversal.
    Instanciated objects can be used to traverse a graph and find a path between two vertices.
    The way the path is found depends on the structure used to store the vertices to visit.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *

# PyRat imports
from Traversal import Traversal

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class DFSTraversal (Traversal):

    """
        This class extends the Traversal class to perform a depth-first traversal.
        It explores the maze by going as far as possible along a path before backtracking.
        It has no guarantee to find the shortest path to the cheese.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)

    #############################################################################################################################################
    #                                                                  METHODS                                                                  #
    #############################################################################################################################################

    @override
    def initialize_structure ( self: Self,
                             ) ->    Any:
    
        """
            This method redefines the abstract method of the parent class.
            It initializes the data structure needed for the traversal.
            In:
                * self: Reference to the current object.
            Out:
                * structure: Initialized data structure.
        """

        # Here, we work with a list
        structure = []
        return structure
    
    #############################################################################################################################################

    @override
    def add_to_structure ( self:      Self,
                           structure: Any,
                           element:   Any
                         ) ->         Any:
    
        """
            This method redefines the abstract method of the parent class.
            It adds an element to the data structure.
            In:
                * self:      Reference to the current object.
                * structure: Data structure to update.
                * element:   Element to add.
            Out:
                * structure: Updated data structure.
        """

        # We append the element to the end of the list
        structure.append(element)

        # The structure was updated in place
        return structure

    #############################################################################################################################################

    @override
    def get_from_structure ( self:      Self,
                             structure: Any,
                           ) ->         Tuple[Any, Any]:
    
        """
            This method redefines the abstract method of the parent class.
            It gets an element from the data structure.
            In:
                * self:      Reference to the current object.
                * structure: Data structure to update.
            Out:
                * element:   Element to get.
                * structure: Updated data structure.
        """

        # Extract the element from the end of the list
        element = structure.pop()

        # The structure was updated in place
        return element, structure

#####################################################################################################################################################
#####################################################################################################################################################