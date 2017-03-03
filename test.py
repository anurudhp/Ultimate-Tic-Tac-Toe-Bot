import team54
import old2
import simulator
from time import time

def test_state(grid, block, old_move):
	board = simulator.Board()

	P1 = team54.Player54()
	ev = old2.evaluate(board, 'x')
	P1.heuristic_estimate = ev[0]
	P1.my_block_score = ev[1]
	P1.opp_block_score = ev[2]
	P1.attack_score = ev[3]

	st = time()
	# try:
	P1.move(board, old_move, 'x')
	# except Exception as e:
		# print "caught excepting. ignoring..."
	en = time()
	print ">>> move time", en - st

def readFromFile(name):
	f = file(name)
	x, y = map(int, f.readline().split())
	old_move = (x, y)
	while f.readline()[0] != '=':
		pass
	f.readline()
	grid = []
	for i in xrange(16):
		row = ""
		while len(row) < 5:
			row = f.readline()
		row = row.split()
		grid.append(row)

	while f.readline()[0] != '=':
		pass
	block = []
	for i in xrange(4):
		row = f.readline()
		row = row.split()
		block.append(row)
	return grid, block, old_move

def testGrid(name):
	print "Testing grid ", name, ":"
	grid, block, old_move = readFromFile("./test_grids/" + name + ".txt")
	test_state(grid, block, old_move)

testGrid("tl1")
testGrid("tl2")
testGrid("tl3")
