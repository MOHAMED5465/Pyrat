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
                source,
                pieces_of_cheese):
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
    

    def neighbors_sorted(self, source, pieces_of_cheese, meta_graph):
        """
            Sorts the neighbors of each vertex in the meta-graph by their distance.

            In:
                * self (Self): Reference to the current object.
                * source: The source vertex.
                * pieces_of_cheese (list): List of vertices representing the positions of the pieces of cheese.
                * meta_graph (dict): The meta-graph, where each vertex is connected to other vertices with
                                    associated distances and routes.

            Out:
                * None. The method populates 'self.the_nearest', a dictionary where each key is a vertex, and the value
                is a sorted list of tuples (neighbor_vertex, distance), ordered by increasing distance.
        """
        # Combine source and pieces of cheese into a single list of vertices.
        vertices = pieces_of_cheese + [source]

        # Iterate over each vertex in the list to compute its sorted neighbors.
        for peice in vertices:
            # Create a list of tuples (neighbor_vertex, distance) for each vertex's neighbors.
            to_sort = [(v, meta_graph[peice][v][0]) for v in vertices if v != peice]

            # Sort the list of neighbors by distance using the second element in the tuple.
            self.the_nearest[peice] = sorted(to_sort, key=lambda x: x[1])


    def next_destination(self, maze, position, pieces_of_cheese):
        """
        Determines whether the player needs to update their destination.

            In:
                * self (Self): Reference to the current object.
                * maze: The maze object representing the game environment.
                * position: The current position of the player in the maze.
                * pieces_of_cheese (list): A list of vertices representing the positions of the remaining pieces of cheese.

            Out:
                * bool: 
                    - Returns True if the player's destination is updated.
                    - Returns False if no update is needed.
        """
        # Check if the player is at their current destination.
        if position == self.destination:
            # Find all valid destinations (pieces of cheese that are still available).
            possible_destinations = set(pieces_of_cheese)

            # Find the nearest valid destination using the sorted list of neighbors.
            i = 0
            while self.the_nearest[position][i][0] not in possible_destinations:
                i += 1

            # Update the player's destination to the nearest valid piece of cheese.
            self.destination = self.the_nearest[position][i][0]
            return True

        # If the player hasn't reached their destination, no update is needed.
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

        # Sort the neighbors by distance to prioritize the closest targets.
        self.neighbors_sorted(source, pieces_of_cheese, self.graph)

        # Set the nearest piece of cheese as the next destination.
        self.destination = self.the_nearest[source][0][0]

        # Retrieve the shortest route from the source to the destination.
        route = self.graph[source][self.destination][1]

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
