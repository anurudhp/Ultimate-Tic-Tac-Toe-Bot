import team54
import old2
import simulator

def test_state(grid, block):
	board = simulator.Board()
	grid = grid.split()
	for i in xrange(16):
		for j in xrange(16):
			board.board_status[i][j] = grid[16*i+j];
	block = block.split()
	for i in xrange(4):
		for j in xrange(4):
			board.block_status[i][j] = block[4*i+j]

	old_move = (0,8)
	old_move = (15,9)

	P1 = team54.Player54()
	ev = old2.evaluate(board, 'x')
	P1.heuristic_estimate = ev[0]
	P1.my_block_score = ev[1]
	P1.opp_block_score = ev[2]

	from time import time
	st = time()
	try:
		P1.move(board, old_move, 'x')
	except Exception as e:
		print "caught excepting. ignoring..."
	en = time()
	print ">>> move time", en - st

grid1='''
- - - x - - x - o o - o o - - -
- - x - - - - o - - - x - - - -
- x - - x x x x - - - - - - - -
x o - - - - - - - x - x x x x x
o - - - - - - - - o - o o - x -
- - x - o - o - - x x - - - - -
- - - - o - - - - - - - - - - -
x - - - - - - - - o - - - - x o
x o - - - - - o o o - - - - o x
- x - - - - - - - - - - x - - x
- - - - - - - o - - - - - - - -
- - - - - - - - - - - - - - - -
- - - o - - o o - - - - - x - x
- - - o - x - - - - - - o - o -
- - - - - - x - o - - o - - - -
- - - o - - - - - - - - - - - -
'''
block1='''
x x - x
- - - -
- - - -
- - - -
'''

grid2='''
o - x x  o o - -  - - - o  - o - -
- - x x  - x - -  - - o x  - - - -
x o x -  x x x x  o o - x  x - - -
x - x -  o x - -  o - - x  x x x x

- x - -  o o - x  o - x o  - - - o
o o - o  - o - -  - - - -  x - - o
- x - -  x x o x  o o x -  x o - -
o x - -  x - - -  - - x -  o - x x

x o x o  - o - -  o o - -  - - o -
o x x x  o o - -  - x - o  - - o -
o o x o  x o - -  o o x o  x - o -
x x o o  x x x x  x o o -  o - x -

o x x o  o - o -  x x x o  - - o -
x x - o  x - - -  - o - x  x - o -
x o o x  o - x -  o x x -  o - x -
x o o x  o - o -  o o o -  o - o -
'''
block2='''
x x o x
- - - -
d x - -
- - - -
'''

test_state(grid1, block1)
test_state(grid2, block2)