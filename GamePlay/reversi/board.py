import common
from common import *


class game_model:
	"""
	The game structure, data and logic
	"""

	def __init__(self):

		## common parameters
		self.BLACK_CELL = common.BLACK_CELL
		self.WHITE_CELL = common.WHITE_CELL
		self.EMPTY_CELL = common.EMPTY_CELL
		self.SIDE_LEN = common.SIDE_LEN

		## create the game grid & initialize it with empty cells
		self.grid = [[0 for x in range(self.SIDE_LEN)] for y in range(self.SIDE_LEN)]
		for i in range(self.SIDE_LEN):
			for j in range(self.SIDE_LEN):
				self.grid[i][j] = self.EMPTY_CELL

		## set the initial 4 center cells
		self.grid[3][3] = self.WHITE_CELL
		self.grid[4][4] = self.WHITE_CELL
		self.grid[3][4] = self.BLACK_CELL
		self.grid[4][3] = self.BLACK_CELL

		self.valid_moves = []

	def reset_game_board(self):
		
		## create the game grid & initialize it with empty cells
		self.grid = [[0 for x in range(self.SIDE_LEN)] for y in range(self.SIDE_LEN)]
		for i in range(self.SIDE_LEN):
			for j in range(self.SIDE_LEN):
				self.grid[i][j] = self.EMPTY_CELL

		## set the initial 4 center cells
		self.grid[3][3] = self.WHITE_CELL
		self.grid[4][4] = self.WHITE_CELL
		self.grid[3][4] = self.BLACK_CELL
		self.grid[4][3] = self.BLACK_CELL

	
	def set_cell(self, pos, color):
		self.grid[pos[0]][pos[1]] = color

	
	def get_grid(self):
		return self.grid


	def get_valid_moves(self, turn):
		"""
		Get and return the valid moves for the current player.
		Each move is represented as a one integer value which
		range from 0 to 63, where this number equals i * 8 + j
		"""

		valid_moves = []
		for i in range(self.SIDE_LEN):
			for j in range(self.SIDE_LEN):
				if self.grid[i][j] != self.EMPTY_CELL:
					continue
				for k in range(common.DIR_COUNT):
					count_my_cells = 0
					count_other_cells = 0
					cur_X = i + common.dx[k]
					cur_Y = j + common.dy[k]
					while self.SIDE_LEN > cur_X >= 0 and self.SIDE_LEN > cur_Y >= 0 :
						if self.grid[cur_X][cur_Y] == 1 - turn:
							count_other_cells += 1
							cur_X += dx[k]
							cur_Y += dy[k]
						elif self.grid[cur_X][cur_Y] == turn:
							count_my_cells += 1
							break
						else:
							break
					if count_my_cells > 0 and count_other_cells > 0:
						valid_moves.append(i * self.SIDE_LEN + j)
						break
		self.valid_moves = valid_moves
		return self.valid_moves


	def is_game_ended(self):
		"""
		Returns true if the game already ended and false otherwise
		"""

		count_white, count_black = self.get_cell_count()

		# One of them already lost all his cells
		if count_white == 0 or count_black == 0:
			return True

		# The board all is full (no empty cells)
		if count_white + count_black == self.SIDE_LEN * self.SIDE_LEN:
			return True

		# If no one can do any more moves
		if self.get_valid_moves(self.WHITE_CELL) == [] and self.get_valid_moves(self.BLACK_CELL) == []:
			return True

		#Otherwise the game still running
		return False



	def get_cell_count(self):
		"""
		Returns 2 parameters, which is the number of 
		white and the number of black cells exists on the board
		"""

		white = 0
		black = 0
		for i in range(self.SIDE_LEN):
			for j in range(self.SIDE_LEN):
				if self.grid[i][j] == self.WHITE_CELL:
					white += 1
				elif self.grid[i][j] == self.BLACK_CELL:
					black += 1
		return white, black


	def make_move(self, move_pos, turn):
		# TO DO
		i = move_pos[0]
		j = move_pos[1]
		for k in range(common.DIR_COUNT):
			count_my_cells = 0
			count_other_cells = 0
			cur_X = i + common.dx[k]
			cur_Y = j + common.dy[k]
			while self.SIDE_LEN > cur_X >= 0 and self.SIDE_LEN > cur_Y >= 0 :
				if self.grid[cur_X][cur_Y] == 1 - turn:
					count_other_cells += 1
					cur_X += dx[k]
					cur_Y += dy[k]
				elif self.grid[cur_X][cur_Y] == turn:
					count_my_cells += 1
					break
				else:
					break
			if count_my_cells > 0 and count_other_cells > 0:
				cur_X = i + common.dx[k]
				cur_Y = j + common.dy[k]
				while self.SIDE_LEN > cur_X >= 0 and self.SIDE_LEN > cur_Y >= 0 :
					if self.grid[cur_X][cur_Y] == 1 - turn:
						self.grid[cur_X][cur_Y] = turn
						cur_X += dx[k]
						cur_Y += dy[k]
					else:
						break
		self.grid[i][j] = turn
