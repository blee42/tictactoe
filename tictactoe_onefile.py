import struct, copy, string

class TicTacToeMove:
	
	def __init__(self, col, row):
		self.col = col
		self.row = row

# find open spots
# Input - 
# board: the current game board
# Output -
# spaces: the list of all the open spots on the game board
# each value in the list is a TicTacToeMove object with col and row
def get_blanks(board):
	spaces = []
	for row in range(0,3):
		for col in range(0,3):
			if (board.get_square(col, row) == 'N'):
				# print board.get_square(col, row)
				blank = TicTacToeMove(col, row)
				# print blank
				spaces.append(blank)
	# print spaces
	return spaces

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
def get_next(nboard, player, alpha, beta):
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

	# if maximizing player
	if (player == 'X'):
		for move in blankList:
			nboard.play_square(move.col, move.row, player)
			val, next_move = get_next(nboard, nextPlayer, alpha, beta)
			valList.append(val)
			nboard.play_square(move.col, move.row, 'N')

			if val > alpha:
				return val, blankList[len(valList)-1]
			beta = min(beta, val)

		val, index = get_max(valList)
		return val, blankList[index]

	# if minimizing player
	else:
		for move in blankList:
			nboard.play_square(move.col, move.row, player)
			val, next_move = get_next(nboard, nextPlayer, alpha, beta) 
			valList.append(val)
			nboard.play_square(move.col, move.row, 'N')

			if val < beta:
				return val, blankList[len(valList)-1]
			alpha = max(val, alpha)

		val, index = get_min(valList)
		return val, blankList[index]

# make a smart next move
# Input - 
# board: the current game board
# cpuval: the value the cpu is playing as (X or O)
def make_smart_cpu_move(board, cpuval):
    nBoard = copy.deepcopy(board)
    winner, next_move = get_next(nBoard, cpuval, 0, 0)
    board.play_square(next_move.col, next_move.row, cpuval)

class TicTacToeBoard:

    def __init__(self):
        self.board = (['N']*3,['N']*3,['N']*3)
                                      
    def PrintBoard(self):
        print(self.board[0][0] + "|" + self.board[1][0] + "|" + self.board[2][0])
        
        print(self.board[0][1] + "|" + self.board[1][1] + "|" + self.board[2][1])
        
        print(self.board[0][2] + "|" + self.board[1][2] + "|" + self.board[2][2])
        
    def play_square(self, col, row, val):
        self.board[col][row] = val

    def get_square(self, col, row):
        return self.board[col][row]

    def full_board(self):
        for i in range(3):
            for j in range(3):
                if(self.board[i][j]=='N'):
                    return False

        return True
    
    #if there is a winner this will return their symbol (either 'X' or 'O'),
    #otherwise it will return 'N'
    def winner(self):
        #check the cols
        for col in range(3):
            if(self.board[col][0]!='N' and self.board[col][0] == self.board[col][1] and self.board[col][0]==self.board[col][2] ):
                return self.board[col][0]
        #check the rows
        for row in range(3):
            if(self.board[0][row]!='N' and self.board[0][row] == self.board[1][row] and self.board[0][row]==self.board[2][row] ):
                return self.board[0][row]
        #check diagonals
        if(self.board[0][0]!='N' and self.board[0][0] == self.board[1][1] and self.board[0][0]==self.board[2][2] ):
            return self.board[0][0]
        if(self.board[2][0]!='N' and self.board[2][0] == self.board[1][1] and self.board[2][0]==self.board[0][2]):
            return self.board[2][0]
        return 'N'

def make_simple_cpu_move(board, cpuval):
    for i in range(3):
        for j in range(3):
            if(board.get_square(i,j)=='N'):
                board.play_square(i,j,cpuval)
                return True
    return False

def play():
    Board = TicTacToeBoard()

    print ("who makes the first move?")
    print ("you = 0, computer = 1")
    first = int(input())

    print ["you are", "computer is"][first] + " going first!"

    if (first == 0):
        humanval =  'X'
        cpuval = 'O'
    else:
        humanval = 'O'
        cpuval = 'X'
        print "CPU Move"
        make_smart_cpu_move(Board, cpuval)

    Board.PrintBoard()
    
    while( Board.full_board()==False and Board.winner() == 'N'):
        print("your move, pick a row (0-2)")
        row = int(input())
        print("your move, pick a col (0-2)")
        col = int(input())

        if(Board.get_square(col,row)!='N'):
            print("square already taken!")
            continue
        else:
            Board.play_square(col,row,humanval)
            if(Board.full_board() or Board.winner()!='N'):
                break
            else:
                Board.PrintBoard()
                print("CPU Move")
                # make_simple_cpu_move(Board,cpuval)
                make_smart_cpu_move(Board, cpuval)
                Board.PrintBoard()

    print("")
    Board.PrintBoard()
    if(Board.winner()=='N'):
        print("Cat game :(")
    elif(Board.winner()==humanval):
        print("You Win!")
    elif(Board.winner()==cpuval):
        print("CPU Wins!")

def main():

    play()

main()
