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

# PyRat imports
from pyrat import Player, Maze, GameState, Action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class GreedyEachTurn_density(Player):

    """
        A player that uses a greedy approach to determine the next destination at each turn.

        This player recalculates its route to the nearest piece of cheese during every turn,
        ensuring it adapts to changes in the game state. It overrides preprocessing, turn, and 
        postprocessing methods to interact seamlessly with the game environment.
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
        self.graph={}
        self.the_nearest={}
        self.actions=[]
        self.destination=None
       
    #############################################################################################################################################
    #                                                               PYRAT METHODS                                                               #
    #############################################################################################################################################
    def traversal ( self:   Self,
                maze:  Maze,
                source: Integral,
                targets
              ) ->      Tuple[Dict[Integral, Integral], Dict[Integral, Optional[Integral]]]:

        """
            This method performs a Dijkstra traversal of a graph.It stops when all the targets are visited.
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
    
    def find_route_and_distance(self: Self,
                                routing_table: Dict[Integral, Optional[Integral]],
                                distances: Dict[Integral, Integral],
                                source: Integral,
                                target: Integral
                                ) -> Tuple[List[Integral], Integral]:
        """
            Finds the shortest route and its distance from the source to the target using the routing table.

            In:
                * self (Self): Reference to the current object.
                * routing_table (Dict[Integral, Optional[Integral]]): The routing table where each vertex maps to its parent
                    on the shortest path to the source. The source vertex maps to `None`.
                * distances (Dict[Integral, Integral]): A dictionary containing the shortest distance from the source to each vertex.
                * source (Integral): The source vertex.
                * target (Integral): The target vertex.
            Out:
                * Tuple[List[Integral], Integral]: 
                    - A list of vertices representing the route from the source to the target.
                    - The total distance of the route from the source to the target.
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
        return route[::-1], distances[target]
        

    def meta_graph(self: Self,
                maze: Maze,
                source: Integral,
                pieces_of_cheese)->Dict[Integral,Dict[Integral,Tuple[Integral,List[Integral]]]]:
        """
        Builds a meta-graph where each node represents either the source or a piece of cheese, and edges 
        represent the shortest paths between them in the original maze.

        In:
            * self (Self): The current instance of the player.
            * maze (Maze): The maze representation, which provides the graph structure of the environment.
            * source: The starting point in the maze.
            * pieces_of_cheese (list): A list of positions of the pieces of cheese in the maze.

        Out:
            * dict: A complete graph (meta-graph) where:
                - Nodes are the source and the pieces of cheese.
                - Edges are the shortest paths (and their distances) between these nodes.
                Each edge is represented as a tuple containing the distance and the path.
        """
        # Initialize the complete meta-graph
        complete_graph = {}

        # Add the source and all pieces of cheese as nodes in the meta-graph
        sources = pieces_of_cheese + [source]
        for element in sources:
            complete_graph[element] = {}

        # Copy the list of nodes to iterate over
        nodes = sources.copy()

        # Process each node to calculate shortest paths to other nodes
        while len(nodes) > 0:
            # Pop a node to serve as the starting point
            start = nodes.pop()

            # Identify all target nodes that are not yet connected to the start node
            targets = [target for target in sources if target != start and target not in complete_graph[start]]

            # Perform a traversal to find distances and routing tables
            distances, routing_table = self.traversal(maze, start, targets)

            # Calculate shortest paths and update the meta-graph
            for target in targets:
                # Find the shortest path and distance between start and target
                route, distance = self.find_route_and_distance(routing_table, distances, start, target)

                # Update the meta-graph with the shortest path and distance
                complete_graph[target][start] = (distance, route[::-1])  # Reverse the route for backward path
                complete_graph[start][target] = (distance, route)        # Forward path

        # Return the complete meta-graph
        return complete_graph
    
    def surrounding_cells(self,cheese,maze):
        rows=maze.height
        cols=maze.width
        # Convert cell index to 2D coordinates
        row = cheese // cols
        col = cheese % cols

        # Determine the bounds of the 5x5 area
        start_row = max(0, row - 2)
        end_row = min(rows - 1, row + 2)
        start_col = max(0, col - 2)
        end_col = min(cols - 1, col + 2)

        # Collect surrounding cell indices
        result = []
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                result.append(r * cols + c)

        return result
    def density(self,cheese,pieces_of_cheese,maze):
        area=self.surrounding_cells(cheese,maze)
        density=0
        for cell in area:
            if cell in pieces_of_cheese:
                density+=1
        return density/(maze.width*maze.height)
    def nearest(self,position,pieces_of_cheese,maze):
        min_weight = float('inf')
        destination = position
        for target in pieces_of_cheese:
            weight=self.graph[position][target][0]/self.density(target,pieces_of_cheese,maze)
            # Update the nearest piece of cheese if the current one is closer.
            if weight < min_weight:
                min_weight = weight
                destination = target
        return destination


    def next_destination(self:Self,
                         maze:Maze,
                         position:Integral,
                         pieces_of_cheese:List[Integral])->bool:
        """
            Determines the next destination for the player based on its current position and the positions 
            of the remaining pieces of cheese.

            In:
                * self (Self): Reference to the current object.
                * maze: The maze object representing the game environment.
                * position: The current position of the player.
                * pieces_of_cheese (list): List of vertices representing the positions of the remaining pieces of cheese.

            Out:
                * bool: 
                    - Returns True if a new destination is selected or if the destination is updated.
                    - Returns False if no new destination is needed.
        """
        # Case 1: Player has reached its current destination.
        if position == self.destination:
            self.destination=self.nearest(position,pieces_of_cheese,maze)
            return True
        # Case 2: The current destination is no longer a valid piece of cheese.
        elif self.destination not in pieces_of_cheese:
            # Perform a traversal to compute distances and routing information from the current position.
            distances, routing_table = self.traversal(maze, position, pieces_of_cheese)

            # Initialize or update the graph representation for the current position.
            self.graph[position] = {}

            # Variables to track the nearest piece of cheese.
            min_weight = float('inf')
            destination = position

            # Evaluate all pieces of cheese to find the nearest one.
            for target in pieces_of_cheese:
                # Find the shortest route and its distance from the current position to the target.
                route, distance = self.find_route_and_distance(routing_table, distances, position, target)

                # Update the graph with the computed route and distance.
                self.graph[target][position] = (distance, route[::-1])  # Reverse the route for the reverse direction.
                self.graph[position][target] = (distance, route)

                # Update the nearest piece of cheese if the current one is closer.
                weight=self.graph[position][target][0]/self.density(target,pieces_of_cheese,maze)
                # Update the nearest piece of cheese if the current one is closer.
                if weight < min_weight:
                    min_weight = weight
                    destination = target

            # Update the player's destination to the nearest piece of cheese.
            self.destination = destination
            return True

        # Case 3: The player has not reached its destination, and the destination is still valid.
        else:
            return False


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
        # Get the player's current location and the locations of the remaining cheese.
        source = game_state.player_locations[self.name]
        pieces_of_cheese = game_state.cheese

        # Build the meta-graph to calculate shortest paths between the source and all pieces of cheese.
        self.graph = self.meta_graph(maze, source, pieces_of_cheese)

        # Set the nearest piece of cheese as the next destination.
        self.destination = self.nearest(source,pieces_of_cheese,maze)

        # Retrieve the shortest route from the source to the destination.
        route = self.graph[source][self.destination][1]
        print(route)
        # Convert the route into a series of actions the player can take in the maze.
        actions = maze.locations_to_actions(route)

        # Store the actions for execution during the game.
        self.actions = actions


    #############################################################################################################################################

    @override
    def turn(self: Self,
            maze: Maze,
            game_state: GameState) -> Action:
        """
        Executes the player's turn in the game.

        This method redefines the abstract method of the parent class and is called at each turn of the game.
        It determines the player's next action based on the current game state, maze structure, and the
        positions of pieces of cheese.

            In:
                * self (Self): Reference to the current player object.
                * maze (Maze): The maze object representing the structure of the game environment.
                * game_state (GameState): The current state of the game, including player locations and cheese positions.

            Out:
                * action (Action): One of the possible actions from the 'Action' enumeration, such as moving "up", "down",
                "left", or "right".
        """
        # Get the current position of the player and the remaining pieces of cheese.
        position = game_state.player_locations[self.name]
        pieces_of_cheese = game_state.cheese

        # Determine if the player needs to update their destination or route.
        boolv = self.next_destination(maze, position, pieces_of_cheese)
        # If a new route is required, compute it and update the player's actions.
        if boolv:
            route = self.graph[position][self.destination][1]
            # Convert the route (list of locations) into a series of actions.
            actions = maze.locations_to_actions(route)
            # Store the actions for future turns.
            self.actions = actions

        # Return the next action to perform during this turn.
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
