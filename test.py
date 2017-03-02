import team54
import old2
import simulator

board = simulator.Board()
grid='''
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
grid = grid.split()
for i in xrange(16):
    for j in xrange(16):
        board.board_status[i][j] = grid[16*i+j];
grid2='''
x x - x
- - - -
- - - -
- - - -
'''
grid2 = grid2.split()
for i in xrange(4):
    for j in xrange(4):
        board.block_status[i][j] = grid2[4*i+j]

old_move = (0,8)

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
