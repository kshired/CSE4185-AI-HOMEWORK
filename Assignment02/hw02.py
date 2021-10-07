from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):

    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)

######################################################################################

class MinimaxAgent(AdversialSearchAgent):
  """
    [문제 01] MiniMax의 Action을 구현하시오. (20점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def minimax(self, state, depth, agent, maximize):
    if state.isWin() or state.isLose()  or depth == self.depth:
      return {
        "action": None,
        "score": self.evaluationFunction(state)
      }
    
    best = {
      "score" : float("inf") if agent else float("-inf"),
      "action" : None
    }

    for action in state.getLegalActions(agent):
      new_state = state.generateSuccessor(agent, action)
      if maximize:
        score = self.minimax(new_state, depth, 1, False)["score"]
        best["action"], best["score"] = [(best["action"], best["score"]), (action, score)][score > best["score"]]
      else:
        if agent >= state.getNumAgents() - 1:
          if depth == self.depth - 1:
            score = self.evaluationFunction(new_state)
          else:
            score = self.minimax(new_state, depth + 1, 0, True)["score"]
        else:
          score = self.minimax(new_state, depth, agent + 1, False)["score"]
        best["score"] = min(score, best["score"])

    return best

  def Action(self, gameState):
  	# ####################### Write Your Code Here ################################
    return self.minimax(gameState, 0 ,0, True)["action"]
    ############################################################################




class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBeta의 Action을 구현하시오. (25점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def alpha_beta(self, state, depth, agent, maximize, alpha, beta):
    if state.isWin() or state.isLose() or depth == self.depth:
      return {
        "action":None,
        "score": self.evaluationFunction(state)
      }
    
    best = {
      "score" : float("inf") if agent else float("-inf"),
      "action" : None
    }

    for action in state.getLegalActions(agent):
      new_state = state.generateSuccessor(agent, action)
      if maximize:
        score = self.alpha_beta(new_state, depth, 1, False, alpha, beta)["score"]
        best["action"], best["score"] = [(best["action"], best["score"]), (action, score)][score > best["score"]]
        alpha = max(alpha, best["score"])
        if best["score"] >= beta:
          return {
            "action": None,
            "score": best["score"],
          }
      else:
        if agent == state.getNumAgents() - 1:
          score = self.alpha_beta(new_state, depth + 1, 0, True, alpha, beta)["score"]
        else:
          score = self.alpha_beta(new_state, depth, agent + 1, False, alpha, beta)["score"]
        best["score"] = min(score, best["score"])
        beta = min(beta, best["score"])
        if alpha >= best["score"]:
          return {
            "action": None,
            "score": best["score"],
          }

    return best

  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    return self.alpha_beta(gameState, 0 ,0, True, float("-inf"), float("inf"))["action"]
    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] Expectimax의 Action을 구현하시오. (25점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################



























    raise Exception("Not implemented yet")

    ############################################################################
