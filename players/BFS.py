#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################


#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *

# PyRat imports
from pyrat import Player, Maze, GameState, Action,Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class BFS (Player):

    """
        This player uses the BFS algorithm to find the shortest path from the starting position to the peice of cheese in an
        unweighted graph.
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
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            Arguments *args and **kwargs are used to pass arguments to the parent constructor.
            This is useful not to declare again all the parent's attributes in the child class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        self.actions = []
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################
    def traversal ( self:   Self,
                    graph:  Graph,
                    source: Integral
                ) ->      Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:

        """
            This method performs a BFS traversal of a graph.
            It returns the explored vertices with associated distances.
            It also returns the routing table, that is, the parent of each vertex in the traversal.
            In:
                * self:   Reference to the current object.
                * graph:  The graph to traverse.
                * source: The source vertex of the traversal.
            Out:
                * distances:     The distances from the source to each explored vertex.
                * routing_table: The routing table, that is, the parent of each vertex in the traversal (None for the source).
        """
        # Initialize the distances dictionary with the source vertex set to a distance of 0.
        # This keeps track of the shortest distance from the source to each vertex.
        distances = {source: 0}

        # Initialize the routing table with the source vertex having no parent (None).
        # This table will store the parent of each vertex during traversal.
        routing_table = {source: None}

        # Create a set to keep track of visited vertices to avoid processing a vertex more than once.
        visited = set()

        # Initialize the queue with the source vertex.
        # This queue will be used to manage the Breadth-First Search (BFS) order.
        queue = [source]

        # Perform BFS while there are vertices in the queue.
        while len(queue) > 0:
            # Remove and get the first vertex in the queue (FIFO behavior for BFS).
            current_vertex = queue.pop(0)

            # If the vertex has not been visited, process it.
            if current_vertex not in visited:
                # Mark the current vertex as visited.
                visited.add(current_vertex)

                # Iterate over all neighbors of the current vertex.
                for neighbor in list(graph.get_neighbors(current_vertex)):
                    # If the neighbor has not been visited yet, process it.
                    if neighbor not in visited:
                        # Update the distance of the neighbor from the source vertex.
                        distances[neighbor] = distances[current_vertex] + 1

                        # Record the current vertex as the parent of the neighbor in the routing table.
                        routing_table[neighbor] = current_vertex

                        # Add the neighbor to the queue for further exploration.
                        queue.append(neighbor)

        # Return the distances and the routing table as the result of the traversal.
        return distances, routing_table

    def find_route ( self:          Self,
                    routing_table: Dict[Integral, Optional[Integral]],
                    source:        Integral,
                    target:        Integral
                ) ->             List[Integral]:

        """
            This method finds the route from the source to the target using the routing table.
            In:
                * self:          Reference to the current object.
                * routing_table: The routing table.
                * source:        The source vertex.
                * target:        The target vertex.
            Out:
                * route: The route from the source to the target.
        """
        # Initialize an empty list to store the route from the target to the source.
        route = []

        # Start from the target vertex and backtrack to the source using the routing table.
        current_vertex = target

        # Continue backtracking until we reach the source vertex.
        while current_vertex != source:
            # Add the current vertex to the route.
            route.append(current_vertex)

            # Move to the parent of the current vertex using the routing table.
            current_vertex = routing_table[current_vertex]

        # Add the source vertex to the route, as it is the starting point.
        route.append(source)

        # Reverse the route so that it starts from the source and ends at the target.
        return route[::-1]

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
        # Get the current location of the player from the game state.
        source = game_state.player_locations[self.name]

        # Get the location of the target (e.g., cheese) from the game state.
        target = game_state.cheese[0]

        # Perform a graph traversal from the source to build the routing table.
        # The routing table maps each vertex to its parent in the traversal path.
        routing_table = self.traversal(maze, source)[1]

        # Use the routing table to find the route from the source to the target.
        route = self.find_route(routing_table, source, target)

        # Convert the route (list of locations) into a series of actions that the player can take.
        actions = maze.locations_to_actions(route)

        # Store the resulting actions in the player's object for use during the game.
        self.actions = actions

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
        # Return the next action from the precomputed list of actions.
        # The list `self.actions` is populated during preprocessing.
        # The `pop(0)` method retrieves and removes the first action from the list, ensuring actions are taken in order.
        return self.actions.pop(0)

#############################################################################################################################################

    @override
    def postprocessing ( self:       Self,
                         maze:       Maze,
                         game_state: GameState,
                         stats:      Dict[str, Any],
                       ) ->          None:

        """
            This method redefines the method of the parent class.
            It is called once at the end of the game.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
                * stats:      Statistics about the game.
            Out:
                * None.
        """

        # Print phase of the game
        print("Postprocessing")

#####################################################################################################################################################
#####################################################################################################################################################
