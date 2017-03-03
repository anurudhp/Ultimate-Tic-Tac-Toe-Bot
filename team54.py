import random
from copy import deepcopy
from time import time


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
TIME_OUT = 13.0
START_DEPTH = 2

class Player54():
    def __init__(self):
        self.max_depth = 0

        self.max_flag = None
        self.min_flag = None
        self.board = None
        self.heuristic_estimate = 0

        # heuristic scoring values
        self.my_block_score = [4*[0] for i in xrange(4)]
        self.opp_block_score = [4*[0] for i in xrange(4)]
        self.attack_score = 0

        self.ans = [0, 0, 0, 0]
        self.start_time = 0

        random.seed()

    def move(self, board, old_move, flag):
        self.start_time = time()
        print old_move[0], old_move[1]

        if self.board == None:
            opp_flag = 'x' if flag == 'o' else 'o'
            self.max_flag = flag
            self.min_flag = opp_flag
        self.board = board
        self.advance(old_move, self.min_flag, False)

        # search
        self.max_depth = 1
        for i in xrange(256):
            current_ans = self.minimax(old_move, flag, self.min_flag)
            if current_ans == None:
                break
            move_score, move_choice = current_ans
            self.max_depth += 1

        self.advance(move_choice, flag, True)
        x, y = move_choice
        self.board.board_status[x][y] = '-'
        self.board.block_status[x >> 2][y >> 2] = '-'

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
    def minimax(self, prev_move, flag, opp_flag, depth = 0, alpha = -INFINITY, beta = +INFINITY):
        if depth >= self.max_depth:
            return self.heuristic_estimate
        if time() - self.start_time > TIME_OUT:
            return None

        valid_moves = self.board.find_valid_move_cells(prev_move)
        if len(valid_moves) == 0:
            return self.heuristic_estimate
        if depth == 0: random.shuffle(valid_moves)

        final_score = None
        optimal_move = None

        for current_move in valid_moves:
            if self.advance(current_move, flag):
                current_score = self.heuristic_estimate
            else:
                current_score = self.minimax(current_move, opp_flag, flag, depth + 1, alpha, beta)

            self.backtrack(current_move, flag)
            if current_score == None:
                return None

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

            if beta <= alpha: break

        if depth == 0: return final_score, optimal_move
        return final_score

    # play a move, and update the heuristic estimate
    def advance(self, current_move, flag, apply_move = True):
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
        ln = 0
        # for pos in posList:
        #     elem = grid[pos[0]][pos[1]]
        #     if elem == '-':
        #         ans[ln] = pos
        #         ln += 1
        #     elif elem != flag:
        #         return False
        elem = grid[posList[0][0]][posList[0][1]]
        if elem == '-':
            ans[ln] = posList[0]
            ln += 1
        elif elem != flag:
            return False

        elem = grid[posList[1][0]][posList[1][1]]
        if elem == '-':
            ans[ln] = posList[1]
            ln += 1
        elif elem != flag:
            return False

        elem = grid[posList[2][0]][posList[2][1]]
        if elem == '-':
            ans[ln] = posList[2]
            ln += 1
        elif elem != flag:
            return False

        elem = grid[posList[3][0]][posList[3][1]]
        if elem == '-':
            ans[ln] = posList[3]
            ln += 1
        elif elem != flag:
            return False

        if ln == 0:
            return True
        elif ln != 4:
            if ln > 0:
                pos = ans[0]
                count[pos[0] % 4][pos[1] % 4][ln - 1] += 1
            if ln > 1:
                pos = ans[1]
                count[pos[0] % 4][pos[1] % 4][ln - 1] += 1
            if ln > 2:
                pos = ans[2]
                count[pos[0] % 4][pos[1] % 4][ln - 1] += 1
        return False

    def count_attacks(self, grid, flag, row, col):
        l = 4*col
        r = l + 4
        u = 4*row
        d = u + 4
        # count = deepcopy(self.count_template)
        count = [[3*[0] for i in xrange(4)] for i in xrange(4)]

        update_count = self.update_count

        # rows
        # for i in xrange(u, d):
            # if self.update_count(count, grid, flag, ((i, l), (i, l + 1), (i, l + 2), (i, l + 3))):
                # return True
        if update_count(count, grid, flag, ((u, l), (u, l + 1), (u, l + 2), (u, l + 3))): return True
        if update_count(count, grid, flag, ((u+1, l), (u+1, l + 1), (u+1, l + 2), (u+1, l + 3))): return True
        if update_count(count, grid, flag, ((u+2, l), (u+2, l + 1), (u+2, l + 2), (u+2, l + 3))): return True
        if update_count(count, grid, flag, ((u+3, l), (u+3, l + 1), (u+3, l + 2), (u+3, l + 3))): return True

        # cols
        # for j in xrange(l, r):
        #     if update_count(count, grid, flag, ((u, j), (u + 1, j), (u + 2, j), (u + 3, j))):
        #         return True
        if update_count(count, grid, flag, ((u, l), (u + 1, l), (u + 2, l), (u + 3, l))): return True
        if update_count(count, grid, flag, ((u, l+1), (u + 1, l+1), (u + 2, l+1), (u + 3, l+1))): return True
        if update_count(count, grid, flag, ((u, l+2), (u + 1, l+2), (u + 2, l+2), (u + 3, l+2))): return True
        if update_count(count, grid, flag, ((u, l+3), (u + 1, l+3), (u + 2, l+3), (u + 3, l+3))): return True

        # main diagonal
        if update_count(count, grid, flag, ((u, l + 3), (u + 1, l + 2), (u + 2, l + 1), (u + 3, l))):
            return True

        # back diagonal
        if update_count(count, grid, flag, ((u, l), (u + 1, l + 1), (u + 2, l + 2), (u + 3, l + 3))):
            return True

        return count
