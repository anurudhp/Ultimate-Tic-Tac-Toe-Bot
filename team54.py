import random
import copy

# def evaluate(board, flag):
#     opp_flag = 'x' if flag == 'o' else 'o'
#     my_block_score = [4*[0] for i in xrange(4)]
#     opp_block_score = [4*[0] for i in xrange(4)]
#
#     my_game_count  = count_attacks(board.block_status, flag, 0, 0)
#     opp_game_count = count_attacks(board.block_status, opp_flag, 0, 0)
#
#     attack_score = 0
#     game_score = 0
#     for i in xrange(0, 4):
#         for j in xrange(0, 4):
#             if board.block_status[i][j] == flag:
#                 my_block_score[i][j] = SCORE_BLOCK
#                 opp_block_score[i][j] = 0
#             elif board.block_status[i][j] == opp_flag:
#                 opp_block_score[i][j] = SCORE_BLOCK
#             elif board.block_status[i][j] == '-':
#                 my_block_score[i][j]  = ...
#                 opp_block_score[i][j] = get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, count_attacks(board.board_status, opp_flag, i, j))
#
#             attack_score += my_block_score[i][j] - opp_block_score[i][j]
#
#             my_game_score  = my_block_score[i][j]*get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, my_game_count[i][j])
#             opp_game_score = opp_block_score[i][j]*get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, opp_game_count[i][j])
#             game_score += my_game_score - opp_game_score
#
#     return WEIGHT_ATTACK*attack_score + WEIGHT_GAME*game_score

INFINITY = 10**18
SCORE_BLOCK  = 10**9
SCORE_CELL   = 10**5
SCORE_PAIR   = 10**3
SCORE_TRIPLE = 10**0
SCORE_GAME_CELL   = 10**6
SCORE_GAME_PAIR   = 10**3
SCORE_GAME_TRIPLE = 10**0
WEIGHT_ATTACK = 10**7
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
        self.backtracking = False

        # heuristic scoring values
        count = [[3*[0] for i in xrange(4)] for i in xrange(4)]
        self.my_block_count = [[1*count for i in xrange(4)] for i in xrange(4)]
        self.opp_block_count = [[1*count for i in xrange(4)] for i in xrange(4)]
        self.my_block_score = [4*[0] for i in xrange(4)]
        self.opp_block_score = [4*[0] for i in xrange(4)]
        self.attack_score = 0

        self.my_game_count = 1*count
        self.opp_game_count = 1*count
        self.my_game_score = self.opp_game_score = 0
        self.game_score = 0

        random.seed()

    def move(self, board, old_move, flag):
        # create copy and bind functions
        opp_flag = 'x' if flag == 'o' else 'o'

        if self.board == None:
            self.board = board
            self.max_flag = flag
            self.min_flag = opp_flag

        self.advance(None, old_move, opp_flag, False)

        # search
        move_score, move_choice = self.minimax(old_move, flag, opp_flag)
        print move_score, move_choice

        self.advance(None, move_choice, flag, False)
        return move_choice

    # search functions
    def minimax(self, prev_move, flag, opp_flag, depth = 0, breadth = 1, alpha = -INFINITY, beta = +INFINITY):
        terminal = self.board.find_terminal_state()
        if terminal[0] != 'CONTINUE':
            if terminal[0] == self.max_flag: return INFINITY
            if terminal[0] == 'NONE':
                return self.heuristic_estimate
            return -INFINITY

        if depth > self.max_depth: # or breadth > self.max_breadth:
            return self.heuristic_estimate

        valid_moves = self.board.find_valid_move_cells(prev_move)
        if depth == 0: random.shuffle(valid_moves)

        final_score = -INFINITY if flag == self.max_flag else +INFINITY
        optimal_move = None
        next_breadth = breadth * len(valid_moves)

        for current_move in valid_moves:
            self.advance(prev_move, current_move, flag)
            current_score = self.minimax(current_move, opp_flag, flag, depth + 1, next_breadth, alpha, beta)
            self.backtrack(prev_move, current_move, flag)

            if flag == self.max_flag:
                if final_score <= current_score:
                    final_score = current_score
                    optimal_move = current_move
                alpha = max(alpha, final_score)
            else:
                if final_score >= current_score:
                    final_score = current_score
                    optimal_move = current_move
                beta = min(beta, final_score)

            if self.must_prune and beta <= alpha: break

        if depth == 0: return final_score, optimal_move
        return final_score

    # play a move, and update the heuristic estimate
    def advance(self, old_move, current_move, flag, apply_move = True):
        if apply_move:
            self.board.update(old_move, current_move, flag)
        self.backtracking = False
        self.update_heuristic(current_move)

    # undo a move, and update the heuristic estimate
    def backtrack(self, old_move, current_move, flag, apply_move = True):
        if apply_move:
            x, y = current_move
            self.board.board_status[x][y] = '-'
            self.board.block_status[x >> 2][y >> 2] = '-'
        self.backtracking = True
        self.update_heuristic(current_move)

    def update_heuristic(self, current_move):
        x, y = current_move
        row, col = x / 4, y / 4
        x, y = x % 4, y % 4

        self.attack_score -= (self.my_block_score[row][col] - self.opp_block_score[row][col])
        self.game_score -= (self.my_game_score - self.opp_game_score)

        # change
        if self.board.block_status[row][col] == self.max_flag:
            self.my_block_score[row][col] = SCORE_BLOCK
            self.opp_block_score[row][col] = 0
        elif self.board.block_status[row][col] == self.min_flag:
            self.my_block_score[row][col] = 0
            self.opp_block_score[row][col] = SCORE_BLOCK
        else:
            self.count_attacks(self.board.board_status, self.my_block_count[row][col], self.max_flag, row, col, x, y)
            self.my_block_score[row][col] = self.get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, self.my_block_count[row][col])
            self.count_attacks(self.board.board_status, self.opp_block_count[row][col], self.min_flag, row, col, x, y)
            self.opp_block_score[row][col] = self.get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, self.opp_block_count[row][col])

        self.count_attacks(self.board.block_status, self.my_game_count, self.max_flag, 0, 0, row, col)
        self.count_attacks(self.board.block_status, self.opp_game_count, self.min_flag, 0, 0, row, col)

        self.my_game_score  = self.my_block_score[row][col]*self.get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, self.my_game_count[row][col])
        self.opp_game_score = self.opp_block_score[row][col]*self.get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, self.opp_game_count[row][col])
        # end change

        self.attack_score += (self.my_block_score[row][col] - self.opp_block_score[row][col])
        self.game_score += (self.my_game_score - self.opp_game_score)

        self.heuristic_estimate = WEIGHT_ATTACK*self.attack_score + WEIGHT_GAME*self.game_score

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
            return score_pair*count[1]**2 + score_triple*count[2]**2

    def update_count(self, grid, count, flag, posList):
        ans = []
        for pos in posList:
            elem = grid[pos[0]][pos[1]]
            if elem == '-':
                ans.append(pos)
            elif elem != flag:
                ans = []
                break
        if len(ans) != 4:
            for pos in ans:
                count[pos[0] % 4][pos[1] % 4][len(ans) - 1] += (-1 if self.backtracking else +1)

    def count_attacks(self, grid, count, flag, row, col, x, y):
        l, u = 4 * row, 4 * col
        # row
        self.update_count(grid, count, flag, ((u + x, l), (u + x, l + 1), (u + x, l + 2), (u + x, l + 3)))
        # col
        self.update_count(grid, count, flag, ((u, l + y), (u + 1, l + y), (u + 2, l + y), (u + 3, l + y)))
        # main diagonal
        if x == y:
            self.update_count(grid, count, flag, ((u, l + 3), (u + 1, l + 2), (u + 2, l + 1), (u + 3, l)))
        # back diagonal
        if x + y == 3:
            self.update_count(grid, count, flag, ((u, l), (u + 1, l + 1), (u + 2, l + 2), (u + 3, l + 3)))
