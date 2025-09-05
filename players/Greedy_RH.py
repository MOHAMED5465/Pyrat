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
import heapq
import itertools

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Greedy(Player):

    """This player uses the Dijkstra algorithm to find the shortest path from its initial position to the cheese.

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
        self.best_length=float('inf')
        self.best_path=[]

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
            * self:   Reference to the current object.
            * graph:  The graph to traverse.
            * source: The source vertex of the traversal.
        Out:
            * distances:     The distances from the source to each explored vertex.
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
    

    #definir la fct qui renvoie le métagraph associé au graph:
    def meta_graph(self:   Self,
                maze:  Maze,
                R:list,
                source: Integral):
        L=[el for el in R]
        L.append(source)
        n=len(L)
        routes_distances={}
        while len(L)!=0:
            current_source=L.pop()
            for neighbour in L:
                distances,routing_table=self.traversal(maze,current_source)
                P=self.find_route(routing_table,current_source,neighbour)
                routes_distances[(current_source,neighbour)]=P,distances[neighbour]


        L=[el for el in routes_distances.keys()]
        for key in  L:
            value=routes_distances[key]
            reverse_key=key[1],key[0]
            routes_distances[reverse_key]=value[0][::-1],value[1]        
        return routes_distances
    


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
        return route[::-1]
    
        #definir brutforce algorithm

    def partial_path(self:Self,remaining:list,vertex,meta_graph):
        """define the partial path using greedy algorithm"""
        non_visited=remaining.copy()
        partial_path=[vertex]
        current_vertex=vertex
        while len(non_visited)!=0:
            comparaison=[( v, meta_graph[(current_vertex,v)][1] )  for v in non_visited]
            current_vertex= min(comparaison, key=lambda x: x[1])[0]
            partial_path.append(current_vertex)
            non_visited.remove(current_vertex) 
        return partial_path    
 
    def complete_path(self:Self,partial_path,meta_graph):
        path=[]
        for i in range(len(partial_path)-1):
            path+=meta_graph[(partial_path[i],partial_path[i+1])][0][:-1] 
        path.append( partial_path[-1] )
        return path
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
        Cheese=game_state.cheese
        print(f"cheese is in {Cheese}")
        Meta_graph=self.meta_graph(maze,Cheese,source)
        print(f'meta graph is {Meta_graph}')
        partial_path=self.partial_path(Cheese,source,Meta_graph)
        complete_path=self.complete_path(partial_path,Meta_graph)
        print(f'complete path is {complete_path}')
        #convert the route to a list of actions
        Actions = maze.locations_to_actions(complete_path)
        self.actions.extend(Actions)

        #print the route, the routing table and the distances
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
        print(f'stats are {stats}')

#####################################################################################################################################################
#####################################################################################################################################################
