import random
from copy import deepcopy
import time
import sys
# import old2

INFINITY = 10**18
SCORE_BLOCK  = 10**9
SCORE_CELL   = 10**6
SCORE_PAIR   = 10**3
SCORE_TRIPLE = 10**0
SCORE_GAME_CELL   = 10**6
SCORE_GAME_PAIR   = 10**3
SCORE_GAME_TRIPLE = 10**0
WEIGHT_ATTACK = 1000
WEIGHT_GAME = 1

class Player54():
    def __init__(self, max_depth = 3, max_breadth = 16**3, must_prune = True):
        self.max_depth = max_depth
        self.max_breadth = max_breadth
        self.must_prune = must_prune

        self.max_flag = None
        self.min_flag = None
        self.board = None
        self.heuristic_estimate = 0
        # self.count_template = [[3*[0] for i in xrange(4)] for i in xrange(4)]

        # heuristic scoring values
        self.my_block_score = [4*[0] for i in xrange(4)]
        self.opp_block_score = [4*[0] for i in xrange(4)]
        self.attack_score = 0

        # debug: timing
        # self.move_times = []
        # self.max_time = 0
        # self.total_time = 0
        # self.total_moves = 0
        self.ans = [0, 0, 0, 0]

        random.seed()

    def move(self, board, old_move, flag):
        self.state_count = 0
        # create copy and bind functions

        # debug: timing
        start_time = time.time()

        if self.board == None:
            opp_flag = 'x' if flag == 'o' else 'o'
            self.max_flag = flag
            self.min_flag = opp_flag
        self.board = board
        self.advance(old_move, self.min_flag, False)

        # search

        move_score, move_choice = self.minimax(old_move, flag, self.min_flag)

        # print move_score, move_choice

        self.advance(move_choice, flag, True)
        x, y = move_choice
        self.board.board_status[x][y] = '-'
        self.board.block_status[x >> 2][y >> 2] = '-'

        # debug: timing
        end_time = time.time()
        delta_time = end_time - start_time
        # self.max_time = max(self.max_time, delta_time)
        # self.total_time += delta_time
        # self.total_moves += 1
        # sys.stderr.write(">> Current move time " + str(delta_time) + "\n")
        # sys.stderr.write(">> Average move time " + str(self.total_time / self.total_moves) + "\n")
        # sys.stderr.write(">> Maximum move time " + str(self.max_time) + "\n\n")
        sys.stderr.write(">>> number of states " + str(self.state_count) + "\n")
        sys.stderr.write(">>> avg. time per state " + str(delta_time / self.state_count) + "\n\n")

        return move_choice

    def check(self):
        print "CHECK SHOULD NEVER BE CALLED !!"
        assert(False)
        if self.heuristic_estimate == INFINITY or self.heuristic_estimate == -INFINITY:
            return
        actual_heuristic = old2.evaluate(self.board, self.max_flag)
        hdiff = (self.heuristic_estimate - actual_heuristic)
        if hdiff != 0:
            print ">>>>>> estimate: %d, actual: %d" % (self.heuristic_estimate, actual_heuristic)
            self.board.print_board()
            assert(hdiff == 0)

    # search functions
    def minimax(self, prev_move, flag, opp_flag, depth = 0, breadth = 1, alpha = -INFINITY, beta = +INFINITY):
        if depth >= self.max_depth or breadth > self.max_breadth:
            return self.heuristic_estimate

        valid_moves = self.board.find_valid_move_cells(prev_move)
        if depth == 0: random.shuffle(valid_moves)

        final_score = None
        optimal_move = None
        next_breadth = breadth * len(valid_moves)

        for current_move in valid_moves:
            if self.advance(current_move, flag):
                current_score = self.heuristic_estimate
            else:
                current_score = self.minimax(current_move, opp_flag, flag, depth + 1, next_breadth, alpha, beta)

            self.backtrack(current_move, flag)

            if flag == self.max_flag:
                if final_score is None or final_score < current_score:
                    final_score = current_score
                    optimal_move = current_move
                alpha = max(alpha, final_score)
            else:
                if final_score is None or final_score > current_score:
                    final_score = current_score
                    optimal_move = current_move
                beta = min(beta, final_score)

            if self.must_prune and beta <= alpha: break

        if depth == 0: return final_score, optimal_move
        return final_score

    # play a move, and update the heuristic estimate
    def advance(self, current_move, flag, apply_move = True):
        self.state_count += 1
        if current_move[0] != -1:
            x, y = current_move
            row, col = x / 4, y / 4
            self.board.board_status[x][y] = flag
            x, y = x % 4, y % 4
            return self.update_heuristic(row, col, x, y)
        return False

    # undo a move, and update the heuristic estimate
    def backtrack(self, current_move, flag):
        if current_move[0] != -1:
            x, y = current_move
            row, col = x / 4, y / 4

            self.board.board_status[x][y] = '-'
            self.board.block_status[row][col] = '-'

            x, y = x % 4, y % 4
            self.update_heuristic(row, col, x, y)

    def update_heuristic(self, row, col, x, y):
        self.attack_score -= (self.my_block_score[row][col] - self.opp_block_score[row][col])

        # change
        my_block_count = self.count_attacks(self.board.board_status, self.max_flag, row, col)
        opp_block_count = self.count_attacks(self.board.board_status, self.min_flag, row, col)

        if my_block_count == True:
            self.my_block_score[row][col] = SCORE_BLOCK
            self.opp_block_score[row][col] = 0
            self.board.block_status[row][col] = self.max_flag
        elif opp_block_count == True:
            self.my_block_score[row][col] = 0
            self.opp_block_score[row][col] = SCORE_BLOCK
            self.board.block_status[row][col] = self.min_flag
        else:
            self.my_block_score[row][col] = self.get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, my_block_count)
            self.opp_block_score[row][col] = self.get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, opp_block_count)

        self.attack_score += (self.my_block_score[row][col] - self.opp_block_score[row][col])

        my_game_count = self.count_attacks(self.board.block_status, self.max_flag, 0, 0)
        opp_game_count = self.count_attacks(self.board.block_status, self.min_flag, 0, 0)

        if my_game_count == True:
            self.heuristic_estimate = INFINITY
            return True
        elif opp_game_count == True:
            self.heuristic_estimate = -INFINITY
            return True

        game_score = 0
        for i in xrange(4):
            for j in xrange(4):
                my_game_score  = self.my_block_score[i][j]*self.get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, my_game_count[i][j])
                opp_game_score = self.opp_block_score[i][j]*self.get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, opp_game_count[i][j])
                game_score += (my_game_score - opp_game_score)

        # end change
        self.heuristic_estimate = WEIGHT_ATTACK*self.attack_score + WEIGHT_GAME*game_score

        return False

    # scoring helpers
    def get_attack_score(self, score_cell, score_pair, score_triple, count):
        score = 0
        for i in xrange(4):
            for j in xrange(4):
                score += self.get_cell_score(score_cell, score_pair, score_triple, count[i][j])
        return score

    def get_cell_score(self, score_cell, score_pair, score_triple, count):
        if count[0] != 0:
            return score_cell
        else:
            return score_pair*(count[1]**2) + score_triple*(count[2]**2)

    def update_count(self, count, grid, flag, posList):
        ans = self.ans
        # [0,0,0,0]
        ln = 0
        for pos in posList:
            # print pos
            elem = grid[pos[0]][pos[1]]
            if elem == '-':
                # ans.append(pos)
                ans[ln] = pos
                ln += 1
            elif elem != flag:
                return False
        # if len(ans) == 0:
        if ln == 0:
            return True
        # elif len(ans) != 4:
        elif ln != 4:
            # for pos in ans:
            for i in xrange(ln):
                pos = ans[i]
                # count[pos[0] % 4][pos[1] % 4][len(ans) - 1] += 1
                count[pos[0] % 4][pos[1] % 4][ln - 1] += 1
        return False

    def count_attacks(self, grid, flag, row, col):
        l = 4*col
        r = l + 4
        u = 4*row
        d = u + 4
        # count = deepcopy(self.count_template)
        count = [[3*[0] for i in xrange(4)] for i in xrange(4)]

        # block_won = False
        # rows
        for i in xrange(u, d):
            if self.update_count(count, grid, flag, ((i, l), (i, l + 1), (i, l + 2), (i, l + 3))):
                return True

        # cols
        for j in xrange(l, r):
            if self.update_count(count, grid, flag, ((u, j), (u + 1, j), (u + 2, j), (u + 3, j))):
                return True

        # main diagonal
        if self.update_count(count, grid, flag, ((u, l + 3), (u + 1, l + 2), (u + 2, l + 1), (u + 3, l))):
            return True

        # back diagonal
        if self.update_count(count, grid, flag, ((u, l), (u + 1, l + 1), (u + 2, l + 2), (u + 3, l + 3))):
            return True

        return count
