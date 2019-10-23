from __future__ import print_function
from collections import deque

#Use priority queues from Python libraries, don't waste time implementing your own
from heapq import *

ACTIONS = [(0,-1),(-1,0),(0,1),(1,0)]

class Agent:
    def __init__(self, grid, start, goal, type):
        self.grid = grid
        self.previous = {}
        self.explored = []
        self.start = start 
        self.grid.nodes[start].start = True
        self.goal = goal
        self.grid.nodes[goal].goal = True
        self.new_plan(type)
    def new_plan(self, type):
        self.finished = False
        self.failed = False
        self.type = type
        if self.type == "dfs" :
            #use stack as frontier
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "bfs":
            #use queue as frontier
            self.frontier = deque([self.start])
            self.explored = []
        elif self.type == "ucs":
            #use heap queue as frontier
            self.frontier = []
            heappush(self.frontier,(0,self.start))
            self.explored = []
        elif self.type == "astar":
            #use heap queue as frontier
            self.frontier = []
            heappush(self.frontier,((self.start[0]-self.grid.goal[0])**2 + (self.start[1]-self.grid.goal[1])**2,self.start))
            self.explored = []
    def show_result(self):
        current = self.goal
        while not current == self.start:
            current = self.previous[current]
            self.grid.nodes[current].in_path = True #This turns the color of the node to red
    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()
    def dfs_step(self):
        #If no path exists, exit
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        #get current node
        current = self.frontier.pop()
        print("current node: ", current)
        #pop the first node from F and push the first node to X
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #iterate every child of current node
        for node in children:
            #exclude children that are in X or F
            if node in self.explored or node in self.frontier:
                print("explored before: ", node)
                continue
            #check whether the node is reachable in the field of grid
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #if encounter a puddle, ignore it
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #set the predecessor of the node
                    self.previous[node] = current
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        #add the node to F
                        self.frontier.append(node)
                        #set the node in the grid to frontier
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
    def bfs_step(self):
        #If no path exists, exit
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        #get the current by following the rule of first in, first out
        current = self.frontier.popleft()
        print("current node: ", current)
        #pop the first node from F and push the first node to X
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #iterate every child of current node
        for node in children:
            #exclude children that are in X or F
            if node in self.explored or node in self.frontier:
                print("explored before: ", node)
                continue
            #check whether the node is reachable in the field of grid
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #if encounter a puddle, ignore it
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #set the predecessor of the node
                    self.previous[node] = current
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        #add the node to F
                        self.frontier.append(node)
                        #set the node in the grid to frontier
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
    def ucs_step(self):
        #[Hint] you can get the cost of a node by node.cost()
        #If no path exists, exit
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        #get node with loweset cost and its cost
        currentPair = heappop(self.frontier)
        currentCost = currentPair[0]
        current = currentPair[1]
        print("current node: ", current)
        #pop the first node from F
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #if current node have not been explored yet
        if current not in self.explored:
            #move current node to explored
            self.explored.append(current)
            #iterate every child of current node
            for node in children:
                #exclude children that are in X or F
                if node in self.explored or node in self.frontier:
                    print("explored before: ", node)
                    continue
                #check whether the node is reachable in the field of grid
                if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                    #if encounter a puddle, ignore it
                    if self.grid.nodes[node].puddle:
                        print("puddle at: ", node)
                    else:
                        #set the predecessor of the node
                        self.previous[node] = current
                        if node == self.goal:
                            self.finished = True
                            print("Total cost: ",currentCost+1)
                            return
                        else:
                            #calculate the cost by adding every node's cost
                            cost = currentCost + self.grid.nodes[node].cost()
                            #add the node to F
                            heappush(self.frontier,(cost,node))
                            #set the node in the grid to frontier
                            self.grid.nodes[node].frontier = True
                else:
                    print("out of range: ", node)
    def astar_step(self):
        #[Hint] you need to declare a heuristic function for Astar
        #[Hint] you can get the cost of a node by node.cost()
        #If no path exists, exit
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        #get node with lowest cost and its cost
        currentPair = heappop(self.frontier)
        currentCost = currentPair[0]
        current = currentPair[1]
        print("current node: ", current)
        #pop the first node from F
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #if current node have not been explored yet
        if current not in self.explored:
            #move current node to X
            self.explored.append(current)
            #iterate every child of current node
            for node in children:
                #exclude children that are in X or F
                if node in self.explored or node in self.frontier:
                    print("explored before: ", node)
                    continue
                #check whether the node is reachable in the field of grid
                if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                    #if encounter a puddle, ignore it
                    if self.grid.nodes[node].puddle:
                        print("puddle at: ", node)
                    else:
                        #set the predecessor of the node
                        self.previous[node] = current
                        if node == self.goal:
                            self.finished = True
                            print("Total cost: ",currentCost-(current[0]-self.grid.goal[0])**2
                                  -(current[1]-self.grid.goal[1])**2+1)
                            return
                        else:
                            #use the heuristic function to get the cost
                            cost = currentCost + self.grid.nodes[node].cost() \
                                   + (node[0]-self.grid.goal[0])**2 + (node[1]-self.grid.goal[1])**2 \
                                   - (current[0]-self.grid.goal[0])**2 - (current[1]-self.grid.goal[1])**2
                            #add the node to F
                            heappush(self.frontier,(cost,node))
                            #set the node in the grid to frontier
                            self.grid.nodes[node].frontier = True
                else:
                    print("out of range: ", node)
