from game import Agent
from game import Directions
import random

from util import manhattanDistance

class DumbAgent(Agent):
    def getAction(self, state):
        print("Location: ", state.getPacmanPosition())
        print("Actions available: ", state.getLegalPacmanActions())
        if Directions.EAST in state.getLegalPacmanActions():
            print("Going East.")
            return Directions.EAST
        else:
            print("Stopping.")
            return Directions.STOP

class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = state.getLegalPacmanActions()
        print("Legal actions: ", legal_actions)
        if legal_actions:
            # Select a random action from the list
            action = random.choice(legal_actions)
            print("Location: ", state.getPacmanPosition())
            print("Actions available: ", state.getLegalPacmanActions())
            return action
        else:
            # If there are no legal actions in that list, stop
            return Directions.STOP

class BetterRandomAgent(Agent):
    def getAction(self, state):
        legal_actions = state.getLegalPacmanActions()
        non_stop_actions = [a for a in legal_actions if a != Directions.STOP]
        action = random.choice(non_stop_actions)
        print("Location: ", state.getPacmanPosition())
        print("Actions available: ", state.getLegalPacmanActions())
        return action

class ReflexAgent(Agent):
    def getAction(self, state):
        legal_actions = state.getLegalPacmanActions()

        best_action = None
        best_score = -float("inf")

        for action in legal_actions:
            successor_state = state.generatePacmanSuccessor(action)
            score = self.evaluationFunction(successor_state)
            if score > best_score:
                best_action = action
                best_score = score
        return best_action

    def evaluationFunction(self, state):
        pacman_position = state.getPacmanPosition()
        ghost_positions = state.getGhostPositions()
        ghost_states = state.getGhostStates()
        food_positions = state.getFood().asList()
        capsule_positions = state.getCapsules()
        walls = state.getWalls().asList()

        score = 0

        if food_positions:
            min_food_distance = min([manhattanDistance(pacman_position, food) for food in food_positions])
            score += 2.0 / min_food_distance  # Increase the weight of food pellets
        else:
            # No food left, assign a high score to encourage completing the level
            score += 1000

        # Calculate the distance to the nearest ghost
        if ghost_positions:
            min_ghost_distance = min([manhattanDistance(pacman_position, ghost) for ghost in ghost_positions])
            score -= 5.0 / min_ghost_distance  # Increase the penalty for being close to ghosts
        else:
            # No ghosts on the board, assign a high value to min_ghost_distance
            min_ghost_distance = float("inf")

        score += state.getScore()

        # Encourage moving towards capsules when ghosts are present
        if ghost_positions and capsule_positions:
            min_capsule_distance = min([manhattanDistance(pacman_position, capsule) for capsule in capsule_positions])
            score += 3.0 / min_capsule_distance  # Increase the reward for being close to capsules

        # Penalize stopping or reversing direction
        legal_actions = state.getLegalPacmanActions()
        if Directions.STOP in legal_actions:
            score -= 10  # Discourage stopping
        reverse_direction = Directions.REVERSE[state.getPacmanState().configuration.direction]
        if reverse_direction in legal_actions:
            score -= 5  # Discourage reversing direction

        # Consider the state of the ghosts
        for ghost_state in ghost_states:
            ghost_position = ghost_state.getPosition()
            if ghost_state.scaredTimer > 0:
                # Encourage eating ghosts when they are scared
                score += 10.0 / manhattanDistance(pacman_position, ghost_position)
            else:
                # Avoid ghosts when they are not scared
                score -= 5.0 / manhattanDistance(pacman_position, ghost_position)

        # Avoid walls and obstacles
        next_position = state.getPacmanState().getPosition()
        for action in legal_actions:
            successor_state = state.generatePacmanSuccessor(action)
            next_position = successor_state.getPacmanState().getPosition()
            if state.hasWall(next_position[0], next_position[1]):
                score -= 100  # Penalize moving towards a wall
            if next_position in ghost_positions and not any(ghost_state.scaredTimer > 0 for ghost_state in ghost_states):
                score -= 200  # Penalize moving towards a non-scared ghost

        # Total number of food pellets still available
        remaining_food_count = state.getNumFood()
        if remaining_food_count > 0:
            score -= 2.0 / remaining_food_count  # Increase the reward for fewer remaining food pellets

        # Whether the game has been won or lost
        if state.isWin():
            print("Winn")
        elif state.isLose():
            print("Losee")

        return score