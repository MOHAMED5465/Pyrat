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
import heapq

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class GreedyEachCheese(Player):



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
        self.peices_of_cheese=set()
        self.nb_cheese=0
        self.actions=[]
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################
    def shortest_path ( self:   Self,
                maze:  Maze,
                source: Integral,
                targets
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
        # Initialize a priority queue (min-heap) to keep track of vertices to explore.
        min_heap = []
        targets=set(targets)

        # Push the source vertex onto the heap with a distance of 0.
        heapq.heappush(min_heap, (0, source))

        # Create a set to keep track of visited vertices to avoid reprocessing them.
        visited = set()

        # Initialize the distances dictionary with the source vertex set to 0.
        distances = {source: 0}

        # Initialize the routing table with the source vertex having no parent (None).
        routing_table = {source: None}

        # While there are vertices in the priority queue, continue the traversal.
        while len(min_heap) > 0 and not targets.issubset(visited):
            # Extract the vertex with the smallest distance from the heap.
            distance, vertice = heapq.heappop(min_heap)

            # Mark the current vertex as visited.
            visited.add(vertice)

            # Get the neighbors of the current vertex.
            neighbors = maze.get_neighbors(vertice)

            # Iterate over all neighbors of the current vertex.
            for neighbor in neighbors:
                # Get the weight of the edge between the current vertex and the neighbor.
                weight = maze.get_weight(vertice, neighbor)

                # Calculate the new distance to the neighbor via the current vertex.
                new_distance = distance + weight

                # If the neighbor hasn't been visited or the new distance is smaller, update.
                if neighbor not in distances or new_distance < distances[neighbor]:
                    # Update the shortest distance to the neighbor.
                    distances[neighbor] = new_distance

                    # Update the routing table to record the current vertex as the parent of the neighbor.
                    routing_table[neighbor] = vertice

                    # Push the neighbor onto the heap with the updated distance.
                    heapq.heappush(min_heap, (new_distance, neighbor))

        # Return the distances and routing table as the result of the traversal.
        return distances, routing_table
    
    def find_route_and_distance ( self:          Self,
                    routing_table: Dict[Integral, Optional[Integral]],
                    distances,
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
        return route[::-1],distances[target]
    
    def meta_graph(self:   Self,
                   maze:  Maze,
                   source,
                   peices_of_cheese
                   ):
        complete_graph={}
        sources = peices_of_cheese + [source]
        for element in sources:
            complete_graph[element]={}
        nodes=sources.copy()
        while len(nodes)>0:
            start=nodes.pop()
            targets = [target for target in sources if target != start and target not in complete_graph[start]]
            distances ,routing_table=self.shortest_path(maze,start,targets)
            for target in targets:
                route,distance=self.find_route_and_distance(routing_table,distances,
                                                            start,target)
                complete_graph[target][start]=(distance,route[::-1])
                complete_graph[start][target]=(distance,route)
        return complete_graph

    def partial_path(self:Self,peices_of_cheese:list,source,meta_graph):
        """define the partial path using greedy algorithm"""
        non_visited=peices_of_cheese.copy()
        partial_path=[source]
        current_vertex=source
        while len(non_visited)>0:
            comparaison=[( v, meta_graph[current_vertex][v][0] )  for v in non_visited]
            current_vertex= min(comparaison, key=lambda x: x[1])[0]
            partial_path.append(current_vertex)
            non_visited.remove(current_vertex) 
        return partial_path    

    def complete_path(self:Self,partial_path,meta_graph):
        path=[]
        for i in range(len(partial_path)-1):
            path+=meta_graph[partial_path[i]][partial_path[i+1]][1][:-1] 
        path.append( partial_path[-1] )
        return path

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
        peices_of_cheese = game_state.cheese
        self.peices_of_cheese=set(peices_of_cheese)
        self.nb_cheese=len(peices_of_cheese)
        meta_graph=self.meta_graph(maze,source,peices_of_cheese)
        partial_path=self.partial_path(peices_of_cheese,source,meta_graph)
        route=self.complete_path(partial_path,meta_graph)

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
        position=game_state.player_locations[self.name]
        if position in self.peices_of_cheese:
            self.nb_cheese=self.nb_cheese-1
            if self.nb_cheese-len(game_state.cheese)>0:
                source = game_state.player_locations[self.name]
                # Get the location of the target (e.g., cheese) from the game state.
                peices_of_cheese = game_state.cheese
                self.peices_of_cheese=set(peices_of_cheese)
                self.nb_cheese=len(peices_of_cheese)
                meta_graph=self.meta_graph(maze,source,peices_of_cheese)
                partial_path=self.partial_path(peices_of_cheese,source,meta_graph)
                route=self.complete_path(partial_path,meta_graph)

                # Convert the route (list of locations) into a series of actions that the player can take.
                actions = maze.locations_to_actions(route)

                # Store the resulting actions in the player's object for use during the game.
                self.actions = actions
        self.nb_cheese=len(game_state.cheese)
        self.peices_of_cheese=set(game_state.cheese)
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
