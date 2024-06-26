# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    frontier = []  # Queue for BFS
    reached = set()  # Set to store visited states

    # Push the start state along with an empty list of actions to the queue
    frontier.append((problem.getStartState(), []))

    # Perform breadth-first search
    while frontier:
        node = frontier.pop(0)  # Pop the first element (FIFO)
        state, actions = node

        # Check if the current state is the goal state
        if problem.isGoalState(state):
            return actions  # Return the list of actions leading to the goal

        # Get the successors of the current state
        successors = problem.getSuccessors(state)

        # Iterate over the successors
        for successor, action, _ in successors:
            # Check if the successor state has not been visited
            if successor not in reached:
                # Mark the successor state as visited
                reached.add(successor)
                # Add the successor state and the updated list of actions to the queue
                frontier.append((successor, actions + [action]))

    # If no solution is found, return an empty list
    return []

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    frontier = util.Stack()
    visited = set()

    # Push the start state along with an empty list of actions to the stack
    frontier.push((problem.getStartState(), []))

    # Perform depth-first search
    while not frontier.isEmpty():
        # Pop the current state and actions from the stack
        state, actions = frontier.pop()

        # Check if the current state is the goal state
        if problem.isGoalState(state):
            return actions

        # Add the current state to the visited set
        visited.add(state)

        # Get the successors of the current state
        successors = problem.getSuccessors(state)

        # Iterate over the successors
        for successor, action, _ in successors:
            # Check if the successor state has not been visited
            if successor not in visited:
                # Push the successor state and the updated list of actions to the stack
                frontier.push((successor, actions + [action]))
                print("Current state:", successor)
                print("Current actions:", actions + [action])
                print()

    # If no solution is found, return an empty list
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    frontier = []  # Priority queue for UCS
    reached = {}  # Set to store visited states and their costs

    # Push the start state along with its cost and an empty list of actions to the priority queue
    frontier.append((problem.getStartState(), 0, []))

    # Perform uniform cost search
    while frontier:
        # Pop the node with the lowest cost
        node = min(frontier, key=lambda x: x[1])
        frontier.remove(node)
        state, cost, actions = node

        # Check if the current state is the goal state
        if problem.isGoalState(state):
            return actions  # Return the list of actions leading to the goal

        # Check if the state has been visited with a lower cost
        if state in reached and reached[state] <= cost:
            continue

        # Mark the state as visited with its cost
        reached[state] = cost

        # Get the successors of the current state
        successors = problem.getSuccessors(state)

        # Iterate over the successors
        for successor, action, step_cost in successors:
            # Calculate the total cost to reach the successor
            total_cost = cost + step_cost

            # Add the successor state, its total cost, and the updated list of actions to the priority queue
            frontier.append((successor, total_cost, actions + [action]))
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def bestFirstSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    reached = {}
    startState = problem.getStartState()
    startNode = (startState, [], 0)  # (state, action, cost)
    frontier.push(startNode, heuristic(startState, problem))
    while not frontier.isEmpty():
        # begin exploring first (lowest-cost) node on frontier
        currentState, actions, currentCost = frontier.pop()
        if (currentState not in reached) or (currentCost < reached[currentState]):
            # put popped node's state into explored list
            reached[currentState] = currentCost
            if problem.isGoalState(currentState):
                return actions
            else:
                # list of (successor, action, stepCost)
                successors = problem.getSuccessors(currentState)
                for succState, succAction, succCost in successors:
                    newAction = actions + [succAction]
                    newCost = currentCost + succCost
                    newNode = (succState, newAction, newCost)
                    frontier.update(newNode, heuristic(succState, problem))
    return actions

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()

    reached = []  # holds (state, cost)

    startState = problem.getStartState()
    startNode = (startState, [], 0)  # (state, action, cost)

    frontier.push(startNode, 0)

    while not frontier.isEmpty():
        # begin exploring first (lowest-combined (cost+heuristic) ) node on frontier
        currentState, actions, currentCost = frontier.pop()
        # put popped node into explored list
        currentNode = (currentState, currentCost)
        reached.append((currentState, currentCost))
        if problem.isGoalState(currentState):
            return actions
        else:
            # list of (successor, action, stepCost)
            successors = problem.getSuccessors(currentState)
            # examine each successor
            for succState, succAction, succCost in successors:
                newAction = actions + [succAction]
                newCost = problem.getCostOfActions(newAction)
                newNode = (succState, newAction, newCost)
                # check if this successor has been explored
                already_explored = False
                for explored in reached:
                    # examine each explored node tuple
                    exploredState, exploredCost = explored
                    if (succState == exploredState) and (newCost >= exploredCost):
                        already_explored = True
                # if this successor not explored, put on frontier and explored list
                if not already_explored:
                    frontier.push(newNode, newCost + heuristic(succState, problem))
                    reached.append((succState, newCost))
    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
befs = bestFirstSearch
