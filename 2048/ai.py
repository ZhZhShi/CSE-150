from __future__ import absolute_import, division, print_function
import copy
import random
import math

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
NUM = [[0.5,4,4.5,8],[1,3.5,5,7.5],[1.5,3,5.5,7],[2,2.5,6,6.5]]
NUMS = [[1,8,9,45],[2,7,10,34],[3,6,11,27],[4,5,15,20]]

class Gametree:
	"""main class for the AI"""
	# Hint: Two operations are important. Grow a game tree, and then compute minimax score.
	# Hint: To grow a tree, you need to simulate the game one step.
	# Hint: Think about the difference between your move and the computer's move.
	def __init__(self, root_state, depth_of_tree, current_score): 
		self.root = root_state
		self.depth = depth_of_tree
		self.score = current_score
		#create the root node
		self.start = Simulator(copy.deepcopy(root_state), current_score, 1, None, -1)
		#build the tree and calculate the decision
		self.growTree()
		self.compute_decision()


	# expectimax for computing best move
	def expectimax(self, state):
		#terminal node
		if len(state.children) == 0:
			return state.heuristic()#use the total score with heuristic funtion
		#max player
		elif state.maxP == 1:
			value = -float('inf')
			for n in state.children:
				value = max(value, self.expectimax(n))
			return value
		#chance player
		else:
			value = 0
			for n in state.children:
				value = value + self.expectimax(n)
			value = value/len(state.children) #take average
			return value


	# function to return best decision to game
	def compute_decision(self):
		max_value = 0
		ret = 0
		#compare four different moves
		for node in self.start.children:
			curr = self.expectimax(node)
			if curr > max_value:
				ret = node.direction
				max_value = curr
		return ret


	#build the tree
	def growTree(self):
		#depth one -- move up, down, right, or left
		for i in range(0,4):
			game = Simulator(copy.deepcopy(self.root), self.start.total_points, 0, self.start, i)
			game.move(i)
			#make sure it is different from the original matrix
			if not game.tileMatrix==self.root:
				self.start.children.append(game)
		#depth two -- chance player
		for node in self.start.children:
			#look for every 0 tile
			for i in range(0,4):
				for j in range(0,4):
					if node.tileMatrix[i][j] == 0:
						ma = copy.deepcopy(node.tileMatrix)
						ma[i][j] = 2
						game = Simulator(ma, node.total_points, 1, node, -1)
						node.children.append(game)
		#	depth three -- move up, down, right, and left
		for sub in self.start.children:
			for node in sub.children:
				for i in range(0,4):
					game = Simulator(copy.deepcopy(node.tileMatrix),node.total_points, 0, node, i)
					game.move(i)
					#make sure it is different from the original matrix
					if not game.tileMatrix == node.tileMatrix:
						node.children.append(game)
		# #depth four -- chance player
		# for sub in self.start.children:
		# 	for subb in sub.children:
		# 		for node in subb.children:
		# 			for i in range(0,4):
		# 				for j in range(0,4):
		# 					if node.tileMatrix[i][j] == 0:
		# 						ma = copy.deepcopy(node.tileMatrix)
		# 						ma[i][j] = 2
		# 						game = Simulator(ma, node.total_points, 1, node, -1)
		# 						node.children.append(game)
		# #depth five -- move up, down, right, and left
		# for sub in self.start.children:
		# 	for subb in sub.children:
		# 		for su in subb.children:
		# 			for node in su.children:
		# 				for i in range(0,4):
		# 					game = Simulator(copy.deepcopy(node.tileMatrix),node.total_points, 0, node, i)
		# 					game.move(i)
		# 					#make sure it is different from the original matrix
		# 					if not game.tileMatrix == node.tileMatrix:
		# 						node.children.append(game)


class Simulator:
	def __init__(self, tileMatrix, score, maxP, parent, dir):
		self.tileMatrix = tileMatrix
		self.total_points = score
		self.board_size = 4
		self.maxP = maxP #is this a max player?
		self.children = []
		self.parent = parent
		self.direction = dir #which direction does it move

	def move(self, direction):
		for i in range(0, direction):
			self.rotateMatrixClockwise()
		if self.canMove():
			self.moveTiles()
			self.mergeTiles()
		for j in range(0, (4 - direction) % 4):
			self.rotateMatrixClockwise()

	def rotateMatrixClockwise(self):
		tm = self.tileMatrix
		for i in range(0, int(self.board_size/2)):
			for k in range(i, self.board_size- i - 1):
				temp1 = tm[i][k]
				temp2 = tm[self.board_size - 1 - k][i]
				temp3 = tm[self.board_size - 1 - i][self.board_size - 1 - k]
				temp4 = tm[k][self.board_size - 1 - i]
				tm[self.board_size - 1 - k][i] = temp1
				tm[self.board_size - 1 - i][self.board_size - 1 - k] = temp2
				tm[k][self.board_size - 1 - i] = temp3
				tm[i][k] = temp4

	def canMove(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for j in range(1, self.board_size):
				if tm[i][j-1] == 0 and tm[i][j] > 0:
					return True
				elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
					return True
		return False

	def moveTiles(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for j in range(0, self.board_size - 1):
				while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
					for k in range(j, self.board_size - 1):
						tm[i][k] = tm[i][k + 1]
					tm[i][self.board_size - 1] = 0
	def mergeTiles(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for k in range(0, self.board_size - 1):
				if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
					tm[i][k] = tm[i][k] * 2
					tm[i][k + 1] = 0
					self.total_points += tm[i][k]
					self.moveTiles()

	def heuristic(self):
		#add each tile's score times a weighed scaler and the total points
		for i in range(0,4):
			for j in range(0,4):
				self.total_points += NUMS[i][j]*self.tileMatrix[i][j]
		return self.total_points

	# def space(self):
	# 	if self.total_points==0:
	# 		return 0
	# 	num_empty = 0
	# 	for i in range(0,4):
	# 		for j in range(0,4):
	# 			if self.tileMatrix[i][j]==0:
	# 				num_empty += 1
	# 	return math.log(self.total_points)*num_empty
