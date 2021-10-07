#!/usr/bin/env python3

import time_info

test = time_info.TimeCheck()
hw02 = test.load('hw02')

FINAL_GRADE = True
SEED = 'testing'
BIG_NEGATIVE = -10000

from game import Agent
from ghostAgents import RandomGhost, DirectionalGhost
import random, math, traceback, sys, os

import pacman, time, layout, textDisplay
textDisplay.SLEEP_TIME = 0
textDisplay.DRAW_EVERY = 1000
thismodule = sys.modules[__name__]


def run(layname, pac, ghosts, nGames = 1):

  if test.fatalError:
    return {'time': 65536, 'wins': 0, 'games': None, 'scores': [0]*nGames, 'timeouts': nGames}

  lay = layout.getLayout(layname, 3)
  disp = textDisplay.NullGraphics()

  games = pacman.runGames(lay, pac, ghosts, disp, nGames, False, catchExceptions=False)

  stats = {'wins': [g.state.isWin() for g in games].count(True), 'games': games, 'scores': [g.state.getScore() for g in games], 'timeouts': [g.agentTimeout for g in games].count(True)}

  return stats


def small_map(agentName):
  stats = {}
  if agentName == 'alphabeta':
    stats = run('smallmap', hw02.AlphaBetaAgent(depth=3), [DirectionalGhost(i + 1) for i in range(2)])
  elif agentName == 'minimax':
    stats = run('smallmap', hw02.MinimaxAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)])
  else:
    stats = run('smallmap', hw02.ExpectimaxAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)])
  if stats['timeouts'] > 0:
    test.fail('Your ' + agentName + ' agent timed out on smallmap.')
    return



def medium_map(agentName):
  stats = {}
  if agentName == 'alphabeta':
    stats = run('mediummap', hw02.AlphaBetaAgent(depth=3), [DirectionalGhost(i + 1) for i in range(2)])
  elif agentName == 'minimax':
    stats = run('mediummap', hw02.MinimaxAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)])
  else:
    stats = run('mediummap', hw02.ExpectimaxAgent(depth=2), [DirectionalGhost(i + 1) for i in range(2)])
  if stats['timeouts'] > 0:
    test.fail('Your ' + agentName + ' agent timed out on mediummap.')
    return




maxSeconds = 5

test.addTest('MiniMax For Small Map', lambda : small_map('minimax'), maxSeconds=maxSeconds, description='MiniMax for timeout on smallMap.')
test.addTest('AlphaBeta For Small Map', lambda : small_map('alphabeta'), maxSeconds=maxSeconds, description='AlphaBeta for timeout on smallMap.')

test.addTest('MiniMax For Medium Map', lambda : medium_map('minimax'), maxSeconds=maxSeconds, description='MiniMax for timeout on mediumMap.')
test.addTest('AlphaBeta For Medium Map', lambda : medium_map('alphabeta'), maxSeconds=maxSeconds, description='AlphaBeta for timeout on mediumMap.')




test.start()
