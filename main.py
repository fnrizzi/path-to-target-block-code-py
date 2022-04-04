#!/bin/python3

from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection
from matplotlib.patches import Rectangle, Circle

class Pawn:
  def __init__(self):
    self.ori_ = [] # W,N,E,S
    self.pos_ = []

  def setInitial(self, ori, pos):
    self.ori_ = [ori]
    self.pos_ = [pos]

  def symbol(self, index):
    if self.ori_[index] == 'N': return '^'
    if self.ori_[index] == 'E': return '>'
    if self.ori_[index] == 'S': return 'v'
    if self.ori_[index] == 'W': return '<'

  def total(self):
    return len(self.pos_)

  def pos(self, i):
    return self.pos_[i]

  def ori(self, i):
    return self.ori_[i]

  def isRotation(self, index):
    return self.ori_[index] != self.ori_[index-1]

  def moveFoward(self, n):
    pos = self.pos_[-1]
    ori = self.ori_[-1]
    newPos = pos.copy()
    if ori == 'N': newPos[1] += n
    if ori == 'E': newPos[0] += n
    if ori == 'S': newPos[1] -= n
    if ori == 'W': newPos[0] -= n

    self.pos_.append(newPos)
    self.ori_.append(ori)

  def rotateLeft(self):
    pos = self.pos_[-1]
    ori = self.ori_[-1]
    newOri = ori
    if ori == 'N': newOri = 'W'
    if ori == 'E': newOri = 'N'
    if ori == 'S': newOri = 'E'
    if ori == 'W': newOri = 'S'

    self.pos_.append(pos.copy())
    self.ori_.append(newOri)

  def rotateRight(self):
    pos = self.pos_[-1]
    ori = self.ori_[-1]
    if ori == 'N': newOri = 'E'
    if ori == 'E': newOri = 'S'
    if ori == 'S': newOri = 'W'
    if ori == 'W': newOri = 'N'

    self.pos_.append(pos.copy())
    self.ori_.append(newOri)

pawn = Pawn()
circleSize = 1500
N = 10
index = -1
problem = -1
handles = []

def avanti_n_passi(n):
  global pawn
  pawn.moveFoward(n)

def ruota_a_destra():
  global pawn
  pawn.rotateRight()

def ruota_a_sinistra():
  global pawn
  pawn.rotateLeft()

def avanti_1_passo(): avanti_n_passi(1)
def avanti_2_passi(): avanti_n_passi(2)
def avanti_3_passi(): avanti_n_passi(3)
def avanti_4_passi(): avanti_n_passi(4)
def indietro_1_passo(): avanti_n_passi(-1)
def indietro_2_passi(): avanti_n_passi(-2)
def indietro_3_passi(): avanti_n_passi(-3)
def indietro_4_passi(): avanti_n_passi(-4)

def plotmesh(ax):
  xg, yg = np.meshgrid(np.linspace(0,N,N+1), np.linspace(0,N,N+1))
  segs1 = np.stack((xg,yg), axis=2)
  segs2 = segs1.transpose(1,0,2)
  ax.add_collection(LineCollection(segs1))
  ax.add_collection(LineCollection(segs2))

def initializePawn():
  global pawn
  if problem in [0,1,2,4]:
    pawn.setInitial('N', [0.5, 0.5])
  elif problem in [3]:
    pawn.setInitial('S', [3.5, 2.5])
  elif problem in [5,6]:
    pawn.setInitial('W', [2.5, 3.5])

def drawTarget(ax):
  global problem
  if problem in [0,1,2]:
    ax.scatter(9.5, 1.5, s=circleSize, c='g', zorder=2)
  elif problem in [3]:
    ax.scatter(8.5, 8.5, s=circleSize, c='g', zorder=2)
  elif problem in [4]:
    ax.scatter(5, 5, s=circleSize, c='g', zorder=2)
  elif problem in [5,6]:
    ax.scatter(8.5, 5.5, s=circleSize, c='g', zorder=2)

def drawObstacle(ax):
  global problem
  if problem == 0:
    pass
  elif problem==1:
    r1 = Rectangle((4, 5), 2, 5, linewidth=3, \
                   edgecolor='k', facecolor='k')
    r2 = Rectangle((4, 0), 2, 4, linewidth=3, \
                   edgecolor='k', facecolor='k')
    ax.add_patch(r1)
    ax.add_patch(r2)
  elif problem in [2,3]:
    r1 = Rectangle((4, 5), 2, 5, linewidth=3, \
                   edgecolor='k', facecolor='k')
    r2 = Rectangle((4, 0), 2, 4, linewidth=3, \
                   edgecolor='k', facecolor='k')
    r3 = Rectangle((1, 3), 3, 1, linewidth=3, \
                   edgecolor='k', facecolor='k')
    r4 = Rectangle((1, 4), 1, 3, linewidth=3, \
                   edgecolor='k', facecolor='k')
    ax.add_patch(r1)
    ax.add_patch(r2)
    ax.add_patch(r3)
    ax.add_patch(r4)
  elif problem in [4]:
    r1 = Circle((5, 5), 2, linewidth=3, \
                edgecolor='k', facecolor='k')
    r2 = Circle((5, 1.5), 1.5, linewidth=3, \
                edgecolor='k', facecolor='k')
    ax.add_patch(r1)
    ax.add_patch(r2)
  elif problem==5:
    for yr in [1,3,5,7,9]:
      r1 = Circle((5, yr), 1, linewidth=3, \
                   edgecolor='k', facecolor='k')
      ax.add_patch(r1)
  elif problem==6:
    r1 = Rectangle((4, 0), 2, 10, linewidth=3, \
                   edgecolor='k', facecolor='k')
    r2 = Rectangle((6, 8), 4, 2, linewidth=3, \
                   edgecolor='k', facecolor='k')
    r3 = Rectangle((6, 0), 4, 2, linewidth=3, \
                   edgecolor='k', facecolor='k')
    ax.add_patch(r1)
    ax.add_patch(r2)
    ax.add_patch(r3)

def onclick(event, ax):
  global pawn, index, problem, handles
  if event.button == 1:
    index += 1
    if index==0:
      plotmesh(ax)

      pos = pawn.pos(index)
      mark = pawn.symbol(index)
      h = ax.scatter(pos[0], pos[1], s=circleSize, c='r', marker=mark)
      handles.append(h)
      drawObstacle(ax)
      drawTarget(ax)

      ax.set_xlim((0,N))
      ax.set_ylim((0,N))
      ax.set_aspect(aspect=1.)
      plt.draw()

    if index < pawn.total() and index>=1:
      oldX,oldY=pawn.pos(index-1)[0], pawn.pos(index-1)[1]
      newX,newY=pawn.pos(index)[0], pawn.pos(index)[1]

      if pawn.isRotation(index):
        plt.setp(handles[-1], alpha=0.2)

      #plt.clf()
      mark = pawn.symbol(index)
      h = plt.scatter(newX,newY, s=circleSize, c='r', marker=mark)
      handles.append(h)
      dx,dy = newX-oldX, newY-oldY
      plt.arrow(oldX, oldY, dx,dy, \
                shape='full', lw=1, head_length=0, \
                length_includes_head=True, head_width=0)
      ax.set_xlim((0,N))
      ax.set_ylim((0,N))
      ax.set_aspect(aspect=1.)
      plt.draw() #redraw

    if index==pawn.total():
      index=-1
      plt.cla()
      plt.draw() #redraw

def visualize():
  global path, index
  fig,ax=plt.subplots()
  ax.tick_params(axis='x',label1On=False)
  ax.tick_params(axis='y',label1On=False)
  fig.canvas.mpl_connect('button_press_event', \
                         lambda event: onclick(event, ax))
  ax.set_aspect(aspect=1.)
  ax.set_xlim((0,N))
  ax.set_ylim((0,N))
  plt.show()




##############################
if __name__== "__main__":
##############################
  parser = ArgumentParser()
  parser.add_argument("-p", dest="prob", \
                      type=int, required=True)
  args     = parser.parse_args()
  problem = args.prob
  initializePawn()

  ruota_a_sinistra()
  avanti_4_passi()
  ruota_a_sinistra()
  avanti_4_passi()
  avanti_4_passi()
  ruota_a_sinistra()
  avanti_3_passi()
  avanti_3_passi()
  ruota_a_sinistra()
  avanti_2_passi()

  visualize()
