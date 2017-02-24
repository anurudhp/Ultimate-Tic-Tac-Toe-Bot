import random
from copy import deepcopy
import old2

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
    def __init__(self, max_depth = 3, max_breadth = 16 ** 10, must_prune = True):
        self.max_depth = max_depth
        self.max_breadth = max_breadth
        self.must_prune = must_prune

        self.max_flag = None
        self.min_flag = None
        self.board = None
        self.heuristic_estimate = 0
        self.count_template = [[3*[0] for i in xrange(4)] for i in xrange(4)]

        # heuristic scoring values
        self.my_block_score = [4*[0] for i in xrange(4)]
        self.opp_block_score = [4*[0] for i in xrange(4)]
        self.attack_score = 0
        self.debug = False

        random.seed(1)

    def move(self, board, old_move, flag):
        # if old_move == (13, 6):
            # self.debug = True
            # self.must_prune = False

        # create copy and bind functions
        opp_flag = 'x' if flag == 'o' else 'o'

        if self.board == None:
            self.max_flag = flag
            self.min_flag = opp_flag
        self.board = board
        self.advance(old_move, opp_flag, self.debug, False)

        # search
        move_score, move_choice = self.minimax(old_move, flag, opp_flag)
        print move_score, move_choice

        self.advance(move_choice, flag, self.debug, True)
        x, y = move_choice
        self.board.board_status[x][y] = '-'
        self.board.block_status[x >> 2][y >> 2] = '-'

        self.debug = False

        return move_choice

    def check(self):
        return
        actual_heuristic = old2.evaluate(self.board, self.max_flag)
        hdiff = (self.heuristic_estimate - actual_heuristic)
        if hdiff != 0:
            print ">>>>>> estimate: %d, actual: %d" % (self.heuristic_estimate, actual_heuristic)
            self.board.print_board()
            assert(hdiff == 0)

    # search functions
    def minimax(self, prev_move, flag, opp_flag, depth = 0, breadth = 1, alpha = -INFINITY, beta = +INFINITY):
        terminal = self.board.find_terminal_state()

        if terminal[0] != 'CONTINUE':
            if terminal[0] == self.max_flag: return INFINITY
            if terminal[0] == 'NONE':
                return self.heuristic_estimate
            return -INFINITY

        if depth >= self.max_depth: # or breadth > self.max_breadth:
            # if self.debug:
                # print depth*'\t', "val =", self.heuristic_estimate
            return self.heuristic_estimate

        valid_moves = self.board.find_valid_move_cells(prev_move)
        if depth == 0: random.shuffle(valid_moves)

        # final_score = -INFINITY if flag == self.max_flag else +INFINITY
        final_score = None
        optimal_move = None
        next_breadth = breadth * len(valid_moves)

        for current_move in valid_moves:
            if self.debug and depth < 2:
                print depth*'\t',
            self.advance(current_move, flag, self.debug and depth < 2)
            current_score = self.minimax(current_move, opp_flag, flag, depth + 1, next_breadth, alpha, beta)
            if self.debug and depth < 2:
                print depth*'\t',
            self.backtrack(current_move, flag, self.debug and depth < 2)

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

        # if self.debug:
        #     print depth*'\t', 'min' if flag == self.min_flag else 'max', "at move:", final_score, optimal_move
        if depth == 0: return final_score, optimal_move
        return final_score

    # play a move, and update the heuristic estimate
    def advance(self, current_move, flag, debug, apply_move = True):
        # if debug:
        #     print ">>> ", current_move
        if apply_move:
            self.board.update((-1, -1), current_move, flag)
        if current_move[0] != -1:
            self.update_heuristic(current_move)
        self.check()

    # undo a move, and update the heuristic estimate
    def backtrack(self, current_move, flag, debug):
        # if debug:
        #     print "<<< ", current_move
        x, y = current_move
        self.board.board_status[x][y] = '-'
        self.board.block_status[x >> 2][y >> 2] = '-'

        self.update_heuristic(current_move)
        self.check()

    def update_heuristic(self, current_move):
        x, y = current_move
        row, col = x / 4, y / 4
        x, y = x % 4, y % 4

        self.attack_score -= (self.my_block_score[row][col] - self.opp_block_score[row][col])

        # change
        if self.board.block_status[row][col] == self.max_flag:
            self.my_block_score[row][col] = SCORE_BLOCK
            self.opp_block_score[row][col] = 0
        elif self.board.block_status[row][col] == self.min_flag:
            self.my_block_score[row][col] = 0
            self.opp_block_score[row][col] = SCORE_BLOCK
        else:
            my_block_count = self.count_attacks(self.board.board_status, self.max_flag, row, col)
            opp_block_count = self.count_attacks(self.board.board_status, self.min_flag, row, col)
            self.my_block_score[row][col] = self.get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, my_block_count)
            self.opp_block_score[row][col] = self.get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, opp_block_count)

        my_game_count = self.count_attacks(self.board.block_status, self.max_flag, 0, 0)
        opp_game_count = self.count_attacks(self.board.block_status, self.min_flag, 0, 0)

        game_score = 0
        for i in xrange(4):
            for j in xrange(4):
                my_game_score  = self.my_block_score[i][j]*self.get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, my_game_count[i][j])
                opp_game_score = self.opp_block_score[i][j]*self.get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, opp_game_count[i][j])
                game_score += (my_game_score - opp_game_score)
        # end change

        self.attack_score += (self.my_block_score[row][col] - self.opp_block_score[row][col])

        self.heuristic_estimate = WEIGHT_ATTACK*self.attack_score + WEIGHT_GAME*game_score

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
            return score_pair*(count[1]) + score_triple*(count[2])

    def update_count(self, count, grid, flag, posList):
        ans = []
        for pos in posList:
            # print pos
            elem = grid[pos[0]][pos[1]]
            if elem == '-':
                ans.append(pos)
            elif elem != flag:
                ans = []
                break
        if len(ans) != 4:
            for pos in ans:
                count[pos[0] % 4][pos[1] % 4][len(ans) - 1] += 1

    def count_attacks(self, grid, flag, row, col):
        l = 4*col
        r = l + 4
        u = 4*row
        d = u + 4
        count = deepcopy(self.count_template)

        # rows
        for i in xrange(u, d):
            self.update_count(count, grid, flag, ((i, l), (i, l + 1), (i, l + 2), (i, l + 3)))

        # cols
        for j in xrange(l, r):
            self.update_count(count, grid, flag, ((u, j), (u + 1, j), (u + 2, j), (u + 3, j)))

        # main diagonal
        self.update_count(count, grid, flag, ((u, l + 3), (u + 1, l + 2), (u + 2, l + 1), (u + 3, l)))

        # back diagonal
        self.update_count(count, grid, flag, ((u, l), (u + 1, l + 1), (u + 2, l + 2), (u + 3, l + 3)))

        return count
