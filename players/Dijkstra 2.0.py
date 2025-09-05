#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player that uses 
    Dijkstra algorithm to find the shortest path to the cheese.
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
import heapq

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Dijkstra (Player):

    """
        This player uses the Dijkstra algorithm to find the shortest path from its initial position to the cheese.

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
    #define the function  traversal that returns the shortest path between two points source and target following the Dijkstra algorithm
    def traversal ( self:   Self,
                maze:  Maze,
                source: Integral
              ) ->      Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:

        """
            This method performs a Dijkstra traversal of a graph.
            It returns the explored vertices with associated distances.
            It also returns the routing table, that is, the parent of each vertex in the traversal.
            In:
                * self: Reference to the current object.
                * graph: The graph to traverse.
                * source: The source vertex of the traversal.
            Out:
               * distances:  The distances from the source to each explored vertex.
               * routing_table: The routing table, that is, the parent of each vertex in the traversal (None for the source).
        """
        #initialize the min heap, the distances, the visited vertices and the routing table
        min_heap=[]
        heapq.heappush(min_heap,(0,source))
        distances={source:0}
        visited_vertices=[]
        routing_table = {source: None}
        
        while len(min_heap) != 0:
            #get the vertex with the minimum distance
            distance, current_vertex=heapq.heappop(min_heap)
            #verify if the vertex is not visited vertices
            if current_vertex not in visited_vertices:
                #mark the vertex as visited
                visited_vertices.append(current_vertex)
                #Go through the  non visited neighbors of the current vertex
                for neighbor in maze.get_neighbors(current_vertex):
                    if neighbor not in visited_vertices:
                        #calculate the new distance
                        new_distance = distance + maze.get_weight(current_vertex, neighbor)
                        #update the distance and the routing table,and the min heap
                        if neighbor not in distances.keys() or new_distance < distances[neighbor]:
                            distances[neighbor]=new_distance
                            heapq.heappush(min_heap,(new_distance,neighbor))
                            routing_table[neighbor]=current_vertex   
        #return the distances and the routing table                            
        return distances, routing_table 

#definir la fonction qui retourne le chemin le plus court entre deux points traget and source suivant l alg de Dijkstra
    def find_route(self,
                routing_table: Dict[Integral, Optional[Integral]],
                source: Integral,
                target: Integral) -> List[Integral]:
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
        route = []
        current_vertex = target

        # Trace back from the target to the source
        while current_vertex is not None and current_vertex != source:
            route.append(current_vertex)
            
            # Check if the current vertex exists in the routing table
            if current_vertex not in routing_table:
                raise ValueError(f"No route found: {current_vertex} not in routing table.")
            
            current_vertex = routing_table[current_vertex]

        if current_vertex is None:
            raise ValueError("No valid route from source to target.")
        
        # Add the source to the route
        route.append(source)

        # Return the route in the correct order (from source to target)
        print(route[::-1])
        return route[::-1]
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
        print("Preprocessing")

        #define the source and the target of the path from the initial position of the player to the cheese
        source=game_state.player_locations[self.name]
        target=game_state.cheese[0]

        #perform the Dijkstra traversal of the maze, and get the routing table and the distances
        Traversal = self.traversal(maze,source)
        routing_table = Traversal[1]
        distances=Traversal[0]

        #find the route from the source to the target using the routing table
        route=self.find_route(routing_table,source,target)

        #convert the route to a list of actions
        Actions = maze.locations_to_actions(route)
        self.actions.extend(Actions)

      

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
        print("Turn")
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
