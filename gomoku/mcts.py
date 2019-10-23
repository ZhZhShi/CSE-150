from __future__ import absolute_import, division, print_function
from math import sqrt, log
import random
import copy
import numpy
from randplay import *
import time

ADD = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

#Feel free to add extra classes and functions

class State:
    def __init__(self, grid, player,position):
        self.grid = grid #grid of state
        self.player = player #the state is under controlled of which player
        self.children = [] #the children states
        self.childrenGrid = [] #the grids of children states
        self.parent = 0 #parent state
        self.game_over = False #whether the game is over
        self.total = 0 #how many moves has been taken from this state
        self.win = 0 #how many moves win
        self.grid_count = 11 #length and width of grid
        self.position = position #where the piece is put
        self.full = False #whether the state is fully expanded
    def check_win(self, r, c):
        #north direction (up)
        n_count = self.get_continuous_count(r, c, -1, 0)
        #south direction (down)
        s_count = self.get_continuous_count(r, c, 1, 0)
        #east direction (right)
        e_count = self.get_continuous_count(r, c, 0, 1)
        #west direction (left)
        w_count = self.get_continuous_count(r, c, 0, -1)
        #south_east diagonal (down right)
        se_count = self.get_continuous_count(r, c, 1, 1)
        #north_west diagonal (up left)
        nw_count = self.get_continuous_count(r, c, -1, -1)
        #north_east diagonal (up right)
        ne_count = self.get_continuous_count(r, c, -1, 1)
        #south_west diagonal (down left)
        sw_count = self.get_continuous_count(r, c, 1, -1)
        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or \
                (se_count + nw_count + 1 >= 5) or (ne_count + sw_count + 1 >= 5):
            self.winner = self.grid[r][c]
            self.game_over = True
    def get_continuous_count(self, r, c, dr, dc):
        piece = self.grid[r][c]
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.grid_count and 0 <= new_c < self.grid_count:
                if self.grid[new_r][new_c] == piece:
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result


class MCTS:
    def __init__(self, grid, player):
        #initalize root
        self.root = State(copy.deepcopy(grid),player,(-1,-1))
        #run uct_search
        self.uct_search()

    def uct_search(self):
        #set timer and time budget
        timeout = time.time()+15
        while time.time()<timeout:
            #select the next move
            node = self.selection(self.root)
            #simulate the result of the move
            winner = self.simulation(node)
            #update total and win
            self.backpropagation(node,winner)
            #print("")

    def selection(self, state):
        #while the state is not terminal
        while not state.game_over:
            #if not fully expanded, expand
            if not self.fullyExpanded(state):
                return self.expansion(state)
            #else choose the best child
            else:
                state = self.best_child(state);
        return state
    def expansion(self, state):
        #get current player
        piece = state.player
        #print("expansion: currrent piece is ",piece)
        #set next player
        if piece=='b':
            nextP = 'w'
        else:
            nextP = 'b'
        # if state.position==(-1,-1):
        #get the set of positions that are occupied by current piece
        allPiece = zip(*numpy.where(numpy.array(state.grid) == piece))
        elsePiece = zip(*numpy.where(numpy.array(state.grid) == nextP))
        #for every position and every possible move
        for pos in allPiece:
            for add in ADD:
                newX = pos[0]+add[0]
                newY = pos[1]+add[1]
                #check within bound
                if -1<newX<11 and -1<newY<11 and state.grid[newX][newY]=='.':
                    #check whether has been expanded
                    if (newX,newY) in state.childrenGrid:
                        continue
                    #print(newX," ",newY)
                    #add to children
                    newGrid = copy.deepcopy(state.grid)
                    newGrid[newX][newY] = piece
                    state.childrenGrid.append((newX,newY))
                    newChild = State(newGrid,nextP,(newX,newY))
                    newChild.parent = state
                    state.children.append(newChild)
                    newChild.position = (newX,newY)
                    #state.childrenGrid.append(newChild.grid)
                    return newChild
        for pos in elsePiece:
            for add in ADD:
                newX = pos[0]+add[0]
                newY = pos[1]+add[1]
                #check within bound
                if -1<newX<11 and -1<newY<11 and state.grid[newX][newY]=='.':
                    #check whether has been expanded
                    if (newX,newY) in state.childrenGrid:
                        continue
                    #print(newX," ",newY)
                    #add to children
                    newGrid = copy.deepcopy(state.grid)
                    newGrid[newX][newY] = piece
                    state.childrenGrid.append((newX,newY))
                    newChild = State(newGrid,nextP,(newX,newY))
                    newChild.parent = state
                    state.children.append(newChild)
                    newChild.position = (newX,newY)
                    #state.childrenGrid.append(newChild.grid)
                    return newChild
        # else:
        #     for add in ADD:
        #         newX = state.position[0]+add[0]
        #         newY = state.position[1]+add[1]
        #         if -1<newX<11 and -1<newY<11 and state.grid[newX][newY]=='.':
        #             newGrid = copy.deepcopy(state.grid)
        #             newGrid[newX][newY] = piece
        #             if (newX,newY) in state.childrenGrid:
        #                 continue
        #             print("leaf",newX," ",newY)
        #
        #             state.childrenGrid.append((newX,newY))
        #             newChild = State(newGrid,nextP,(newX,newY))
        #             newChild.parent = state
        #             state.children.append(newChild)
        #             newChild.position = (newX,newY)
        #             return newChild
    def best_child(self, state):
        count = -1
        #get the child with highest value
        for child in state.children:
            value = child.win/child.total+5*sqrt(numpy.log(state.total)/child.total)
            if value > count:
                ret = child
                count = value
        #print(state.position,"'s best child is ",ret.position)
        return ret
    def simulation(self, state):
        #print("simulate",state.position)
        #check whether the current move has ended the game
        state.check_win(state.position[0],state.position[1])
        if state.game_over:
            return state.player
        #simulate play by random move
        rand = Randplay(copy.deepcopy(state.grid),state.player)
        result = rand.rollout()
        if result['b']==1:
            return 'b'
        return 'w'
    def backpropagation(self, state, result):
        #update total and win from state to root
        while True:
            state.total+=1
            if state.player=='b' and result=='b':
                state.win+=1
            if state.player=='w' and result=='w':
                state.win+=1
            if state.parent!=0:
                state=state.parent
            else:
                break
    def getAction(self):
        count = -1;
        #get the child with highest count
        for child in self.root.children:
            #print(child.position," ",child.win," ",child.total)
            #print(child.position," : ",child.win," / ",child.total)
            if child.win/child.total>count:
                ret = child.position
                count = child.win/child.total
        return ret
    def fullyExpanded(self,state):
        #if state has no children, then it is not fully expanded
        if len(state.children)==0:
            #print(state.position," is not fully expanded")
            return False;
        #if the state is labeled fully expanded
        if state.full ==1:
            return True
        #print(state.position," is not fully expanded")
        piece = state.player
        #check every possible move that can be expanded
        allPiece = zip(*numpy.where(numpy.array(state.grid) == piece))
        if piece=='b':
            NPiece = 'w'
        else:
            NPiece = 'b'
        elsePiece = zip(*numpy.where(numpy.array(state.grid) == NPiece))
        for pos in allPiece:
            for add in ADD:
                newX = pos[0]+add[0]
                newY = pos[1]+add[1]
                if -1<newX<11 and -1<newY<11 and state.grid[newX][newY]=='.':
                    if (newX,newY) not in state.childrenGrid:
                        return False
        for pos in elsePiece:
            for add in ADD:
                newX = pos[0]+add[0]
                newY = pos[1]+add[1]
                if -1<newX<11 and -1<newY<11 and state.grid[newX][newY]=='.':
                    if (newX,newY) not in state.childrenGrid:
                        return False
        state.full = True
        return True
