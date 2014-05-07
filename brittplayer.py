import struct, copy

class TicTacToeMove:
	
	def __init__(self, col, row):
		self.col = col
		self.row = row

# find open spots
# Input - 
# board: the current game board
# Output -
# open: the list of all the open spots on the game board
# each value in the list is a TicTacToeMove object with col and row
def get_blanks(board):
	open = []
	for row in range(0,3):
		for col in range(0,3):
			if (board.get_square(col, row) == 'N'):
				# print board.get_square(col, row)
				blank = TicTacToeMove(col, row)
				# print blank
				open.append(blank)
	# print open
	return open

# find next player
# Input -
# player: the current game player
# Output -
# nextPlayer: the next game player
def get_next_player(player):
	if (player == 'X'):
		return 'O'
	else:
		return 'X'

# find max val
# Input - 
# valList: list of values
# Output -
# maxVal: the maximum value in the list
# index: the index of the maximum value
def get_max(valList):
	maxVal = max(valList)
	index = valList.index(maxVal)
	return maxVal, index

# find min val
# Input - 
# valList: list of values
# Output -
# minVal: the minimum value in the list
# index: the index of the minimum value
def get_min(valList):
	minVal = min(valList)
	index = valList.index(minVal)
	return minVal, index

# find next move (minimax-decision)
# Input - 
# nBoard: copy of the game board
# player: current player
# Output - 
# val: the predicted winner where 0 = tie, 1 = X wins, -1 = O wins
# next: -1 = game is finished, TicTacToeMove object with col and row
def get_next(nboard, player):
	# check if we found winner
	win = nboard.winner()
	if (win != 'N'):
		if (win == 'X'):
			return 1, -1
		else:
			return -1, -1

	valList = []

	# get the next player
	nextPlayer = get_next_player(player)

	# check if there are no more moves
	blankList = get_blanks(nboard)
	if (len(blankList) == 0):
		return 0, -1

	# recursively look at the results of each move
	for move in blankList:
		nboard.play_square(move.col, move.row, player)
		val, next = get_next(nboard, nextPlayer)
		valList.append(val)
		nboard.play_square(move.col, move.row, 'N')

	# if maximizing player
	if (player == 'X'):
		val, index = get_max(valList)
		return val, blankList[index]

	# if minimizing player
	else:
		val, index = get_min(valList)
		return val, blankList[index]

# make a smart next move
# Input - 
# board: the current game board
# cpuval: the value the cpu is playing as (X or O)
def make_smart_cpu_move(board, cpuval):
    nBoard = copy.deepcopy(board)
    winner, next = get_next(nBoard, cpuval)
    board.play_square(next.col, next.row, cpuval)

