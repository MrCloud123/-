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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print(successorGameState.getGhostStates()[0])
        #print(successorGameState.getGhostStates()[1])
        #print(newPos)#坐标（1，2）
        #print(successorGameState.getScore())#单纯数字
        #return successorGameState.getScore()
        d=manhattanDistance(newPos,successorGameState.getGhostPositions()[0])
        foodls=currentGameState.getFood().asList()
        close=999
        for i in foodls:
            if close>manhattanDistance(newPos,i):
                close=manhattanDistance(newPos,i)
        if d<=3:
            return 0
        elif close==0:
            return 100+random.random()*0.1
        else:
            return 1/(close+1)

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
        "*** YOUR CODE HERE ***"
        k=self.minimax(gameState,0,1)
        return k
    def minimax(self,state,index,layer):
        if (state.isWin() or state.isLose() or layer>self.depth):
            #import time
            #time.sleep(1)
            return self.evaluationFunction(state)
        actions=state.getLegalActions(index)
        ls=[]
        for i in actions:
            successor=state.generateSuccessor(index,i)
            if (index==state.getNumAgents()-1):
            #index=0说明是pacman
                ls.append(self.minimax(successor,0,layer+1))
            else:
                ls.append(self.minimax(successor,index+1,layer))
        if index==0:
            if(layer==1):
                for i in range(len(ls)):
                    if (ls[i]==max(ls)):
                        return actions[i]
            else:
                return max(ls)
        else:
            return min(ls)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        k=self.AlphaBetamax(gameState)[1]
        #print(k)
        return k

    def AlphaBetamax(self,state,layer=0,index=0,alpha=-float("inf"),beta=float("inf")):
        actions=state.getLegalActions(index)
        actions=[i for i in actions if i!= "Stop"]
        if layer==self.depth or len(actions)==0:
            return self.evaluationFunction(state),"None"
        maxval=-float("inf")
        bestaction=None
        for i in actions:
            successor=state.generateSuccessor(index,i)
            v=self.AlphaBetamin(successor,layer,index+1,alpha,beta)[0]
            if v>maxval:
                maxval=v
                bestaction=i
            if v>beta:
                return v,i
            alpha=v if v>alpha else alpha               
        return maxval,bestaction

    def AlphaBetamin(self,state,layer=0,index=1,alpha=-float("inf"),beta=float("inf")):
        actions=state.getLegalActions(index)
        if layer==self.depth or len(actions)==0:
            return self.evaluationFunction(state),"None"
        minval=float("inf")
        bestaction=None
        for i in actions:
            successor=state.generateSuccessor(index,i)
            if (index==state.getNumAgents()-1):#说明是pacman
            #index=0说明是pacman
                v=self.AlphaBetamax(successor,layer+1,0,alpha,beta)[0]
            else:#说明是鬼
                v=self.AlphaBetamin(successor,layer,index+1,alpha,beta)[0]
            if v<minval:
                minval=v
                bestaction=i
            if v<alpha:   
                return v,i
            beta=v if v<beta else beta
        return minval,bestaction
        #深度优先搜索，只能比较之前的和目前的分支
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
        "*** YOUR CODE HERE ***"
        k=self.getmax(gameState)[1]
        return k

    def getmax(self,state,layer=0,index=0):
        actions=state.getLegalActions(index)
        actions=[i for i in actions if i!= "Stop"]
        if layer==self.depth or len(actions)==0:
            return self.evaluationFunction(state),"Stop"
        maxval=-float("inf")
        bestaction="Stop"
        for i in actions:
            successor=state.generateSuccessor(index,i)
            v=self.getexp(successor,layer,index+1)[0]
            if v>maxval:
                maxval=v
                bestaction=i           
        return maxval,bestaction

    def getexp(self,state,layer=0,index=1):
        actions=state.getLegalActions(index)
        actions=[i for i in actions if i!= "Stop"]
        #print(actions)
        if layer==self.depth or len(actions)==0:
            return self.evaluationFunction(state),"Stop"
        bestaction="Stop"
        total=0
        for i in actions:
            successor=state.generateSuccessor(index,i)
            if (index==state.getNumAgents()-1):#说明是pacman
            #index=0说明是pacman
                v=self.getmax(successor,layer+1,0)[0]
            else:#说明是鬼
                v=self.getexp(successor,layer,index+1)[0]
            total+=v
        return total/len(actions),bestaction

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: The first step is to judge the scared time of the ghost. If the time is larger than 2, 
                 #the pacman should try to get closer to the ghost and try to eat it. In the normal state, 
                 #the pacman should find the closest food when the distance between pacman and ghost is larger than 3.
                 #If the distance is smaller than 2, it means that the ghost is approaching, so the best strategy is 
                 #running away.  In order to prevent the situation that the two point may have same score and the pacman
                 #may wander between two points for a long time, I add a very small random number to let the pacman jump out
                 #from the wandering. The adding of that random number is useful, the average score increases by about 6%.
    """
    "*** YOUR CODE HERE ***"
    score=currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    d=manhattanDistance(newPos,currentGameState.getGhostPositions()[0])
    scaredTime=currentGameState.getGhostStates()[0].scaredTimer
    foodls=newFood.asList()
    close=999
    for i in foodls:
        if close>=manhattanDistance(newPos,i):
            close=manhattanDistance(newPos,i)
    if scaredTime<2:
        if d==0:
            return -float("INF")
        elif d<2:
            return score
        return 1/(close+1)+score+random.random()*0.01
    else:
        return 1/d+score+random.random()*0.01

# Abbreviation
better = betterEvaluationFunction
