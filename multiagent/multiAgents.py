# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        #print legalMoves
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print scores
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        #newFood = successorGameState.getFood()
        Food = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print newGhostStates
        foodCount = Food.count(True)
        if(foodCount ==0):
            return 9999
        nearestFood = 1000
        for i, item in enumerate(Food):
            for j, foodItem in enumerate(item):
                nearestFood = min(nearestFood, util.manhattanDistance(newPos, (i, j)) if foodItem else 100)
        ghostDistances = [util.manhattanDistance(newPos, hh.getPosition()) for hh in newGhostStates]
        score = -nearestFood
        for dist in ghostDistances:
            if dist == 0:
                score -= 1000
            elif dist==1:
                score -= 10
        #print "score: ", score, ghostK, nearFoodBonus
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.nextagent = 'max'
        self.ghostidx = 1

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        return self.minimax(gameState, self.depth)[1]

    def minimax(self, gameState, depth, agentidx = 0):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), 'Stop'
        if agentidx == 0:
            return self.max_value(gameState, depth)
        else:
            return self.min_value(gameState, depth, agentidx)


    def max_value(self, gameState, depth):
        max_score = -1000000
        for action in gameState.getLegalActions(0):
            childState = gameState.generateSuccessor(0, action)
            childState_score,  pacman_action= self.minimax(childState, depth, 1)
            if childState_score > max_score:
                max_score = childState_score
                bestaction = action
        return max_score, bestaction

    def min_value(self, gameState, depth, agentidx):
        min_score = 1000000
        for action in gameState.getLegalActions(agentidx):
            childState = gameState.generateSuccessor(agentidx, action)
            if agentidx == gameState.getNumAgents() - 1 and depth ==  1:
                childState_score = self.evaluationFunction(childState)
            else:
                if agentidx == gameState.getNumAgents() - 1 and depth > 1:
                    childState_score = self.minimax(childState, depth - 1, 0)[0]
                else:
                    childState_score = self.minimax(childState, depth, agentidx + 1)[0]
            if childState_score < min_score:
                min_score = childState_score
                bestaction = action
        return  min_score, bestaction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.alphabeta(gameState, self.depth)[1]

    def alphabeta(self, gameState, depth, agentidx = 0, alpha = -float("inf"), beta = float("inf")):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), 'Stop'
        if agentidx == 0:
            return self.max_value(gameState, depth, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentidx, alpha, beta)

    def max_value(self, gameState, depth, alpha = -float("inf"), beta = float("inf")):
        max_score = -float("inf")
        a = alpha
        for action in gameState.getLegalActions(0):
            childState = gameState.generateSuccessor(0, action)
            childState_score,  pacman_action= self.alphabeta(childState, depth, 1, a, beta)
            if childState_score > max_score:
                max_score = childState_score
                bestaction = action
            a = max(max_score, alpha)
            if max_score > beta:
                #print "prune", max_score, childState.state
                return max_score, bestaction
        return max_score, bestaction

    def min_value(self, gameState, depth, agentidx, alpha = -float("inf"), beta = float("inf")):
        min_score = float("inf")
        b = beta
        for action in gameState.getLegalActions(agentidx):
            childState = gameState.generateSuccessor(agentidx, action)
            if agentidx == gameState.getNumAgents() - 1 and depth ==  1:
                childState_score = self.evaluationFunction(childState)
            else:
                if agentidx == gameState.getNumAgents() - 1 and depth > 1:
                    childState_score = self.alphabeta(childState, depth - 1, 0, alpha, b)[0]
                else:
                    childState_score = self.alphabeta(childState, depth, agentidx + 1,  alpha, b)[0]
            if childState_score < min_score:
                min_score = childState_score
                bestaction = action
            b = min(min_score, b)
            if min_score < alpha:
                return  min_score, bestaction
        return  min_score, bestaction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        return self.expectimax(gameState, self.depth)[1]
    def expectimax(self, gameState, depth, agentidx = 0):
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), 'Stop'
        if agentidx == 0:
            return self.max_value(gameState, depth)

        else:
            return self.expect_value(gameState, depth, agentidx)


    def max_value(self, gameState, depth):
        max_score = -1000000
        for action in gameState.getLegalActions(0):
            childState = gameState.generateSuccessor(0, action)
            childState_score,  pacman_action= self.expectimax(childState, depth, 1)
            if childState_score > max_score:
                max_score = childState_score
                bestaction = action
        return max_score, bestaction

    def expect_value(self, gameState, depth, agentidx):
        legal_actions = gameState.getLegalActions(agentidx)
        exp_score = 0
        for action in legal_actions:
            childState = gameState.generateSuccessor(agentidx, action)
            if agentidx == gameState.getNumAgents() - 1 and depth ==  1:
                childState_score = self.evaluationFunction(childState)
            else:
                if agentidx == gameState.getNumAgents() - 1 and depth > 1:
                    childState_score = self.expectimax(childState, depth - 1, 0)[0]
                else:
                    childState_score = self.expectimax(childState, depth, agentidx + 1)[0]
            exp_score += childState_score / (1.0 * len(legal_actions))
        return  exp_score, random.choice(legal_actions)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """

    newPos = currentGameState.getPacmanPosition()
    #newFood = successorGameState.getFood()
    Food = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    #print newScaredTimes

    "*** YOUR CODE HERE ***"
    # print newGhostStates
    foodCount = Food.count(True)
    if(foodCount ==0):
        return 9999
    nearestFood = 1000
    for i, item in enumerate(Food):
        for j, foodItem in enumerate(item):
            nearestFood = min(nearestFood, util.manhattanDistance(newPos, (i, j)) if foodItem else 100)
    ghostDistances = [util.manhattanDistance(newPos, hh.getPosition()) for hh in newGhostStates]
    score = -nearestFood - foodCount*100
    for dist in ghostDistances:
        #print newScaredTimes, ghostDistances.index(dist)
        if newScaredTimes[ghostDistances.index(dist)] > 0:
            score += 10000000.0/dist
        else:
            if dist == 0:
                score -= 100000
            elif dist==1:
                score -= 1000
    return score

# Abbreviation
better = betterEvaluationFunction

