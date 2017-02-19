import random
import copy

def evaluate(board, flag):
    SCORE_BLOCK  = 10**9
    SCORE_CELL   = 10**5
    SCORE_PAIR   = 10**3
    SCORE_TRIPLE = 10**0
    SCORE_GAME_CELL   = 10**6
    SCORE_GAME_PAIR   = 10**3
    SCORE_GAME_TRIPLE = 10**0
    WEIGHT_ATTACK = 10**7
    WEIGHT_GAME = 1

    opp_flag = 'x' if flag == 'o' else 'o'
    my_block_score = [4*[0] for i in xrange(4)]
    opp_block_score = [4*[0] for i in xrange(4)]

    my_game_count  = count_attacks(board.block_status, flag, 0, 0)
    opp_game_count = count_attacks(board.block_status, opp_flag, 0, 0)

    attack_score = 0
    game_score = 0
    for i in xrange(0, 4):
        for j in xrange(0, 4):
            if board.block_status[i][j] == flag:
                my_block_score[i][j] = SCORE_BLOCK
            elif board.block_status[i][j] == opp_flag:
                opp_block_score[i][j] = SCORE_BLOCK
            elif board.block_status[i][j] == '-':
                my_block_score[i][j]  = get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, count_attacks(board.board_status, flag, i, j))
                opp_block_score[i][j] = get_attack_score(SCORE_CELL, SCORE_PAIR, SCORE_TRIPLE, count_attacks(board.board_status, opp_flag, i, j))

            # assert(my_block_score[i][j] >= 0 and opp_block_score[i][j] >= 0)
            attack_score += my_block_score[i][j] - opp_block_score[i][j]

            my_game_score  = my_block_score[i][j]*get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, my_game_count[i][j])
            opp_game_score = opp_block_score[i][j]*get_cell_score(SCORE_GAME_CELL, SCORE_GAME_PAIR, SCORE_GAME_TRIPLE, opp_game_count[i][j])
            # assert(my_game_score >= 0 and opp_game_score >= 0)
            game_score += my_game_score - opp_game_score

    return WEIGHT_ATTACK*attack_score + WEIGHT_GAME*game_score

def get_attack_score(score_cell, score_pair, score_triple, count):
    score = 0
    for i in xrange(4):
        for j in xrange(4):
            score += get_cell_score(score_cell, score_pair, score_triple, count[i][j])

    return score

def get_cell_score(score_cell, score_pair, score_triple, count):
    if count[0] != 0:
        return score_cell
    else:
        return score_pair*count[1]**2 + score_triple*count[2]**2

def count_attacks(board, flag, row, col):
    l = 4*col
    r = l + 4
    u = 4*row
    d = u + 4
    count = [[3*[0] for i in xrange(4)] for i in xrange(4)]

    # rows
    for i in xrange(u, d):
        update_count(count, board, flag, ((i, l), (i, l + 1), (i, l + 2), (i, l + 3)))

    # cols
    for j in xrange(l, r):
        update_count(count, board, flag, ((u, j), (u + 1, j), (u + 2, j), (u + 3, j)))

    # main diagonal
    update_count(count, board, flag, ((u, l + 3), (u + 1, l + 2), (u + 2, l + 1), (u + 3, l)))

    # back diagonal
    update_count(count, board, flag, ((u, l), (u + 1, l + 1), (u + 2, l + 2), (u + 3, l + 3)))

    return count

def update_count(count, board, flag, posList):
    ans = []
    for pos in posList:
        elem = board[pos[0]][pos[1]]
        if elem == '-':
            ans.append(pos)
        elif elem != flag:
            ans = []
            break
    if len(ans) != 4:
        for pos in ans:
            count[pos[0] % 4][pos[1] % 4][len(ans) - 1] += 1

INFINITY = 10**18
class Player54():
    def __init__(self, max_depth = 3, max_breadth = 1, must_prune = True):
        self.max_depth = max_depth
        self.max_breadth = max_breadth
        self.must_prune = must_prune

        self.max_flag = None
        self.board = None
        self.heuristic_estimate = 0

        random.seed()

    def move(self, board, old_move, flag):
        # create copy and bind functions
        self.board = copy.deepcopy(board)
        self.board.backtrack = backtrack_move.__get__(board)
        self.board.evaluate = evaluate.__get__(board)

        # search
        self.max_flag = flag
        # self.heuristic_estimate = evaluate()
        opp_flag = 'x' if flag == 'o' else 'o'
        move_choice = self.minimax(old_move, flag, opp_flag)

        print move_choice
        return move_choice[1]

    # search functions
    def minimax(self, prev_move, flag, opp_flag, depth = 0, breadth = 1, alpha = -INFINITY, beta = +INFINITY):
        terminal = board.find_terminal_state()
        if terminal[0] != 'CONTINUE':
            if terminal[0] == self.max_flag: return INFINITY
            if terminal[0] == opp_flag: return
            if terminal[0] == 'NONE':
                return board.heuristic_estimate
            return -INFINITY

        if depth > self.max_depth or breadth > self.max_breadth:
            return board.heuristic_estimate

        valid_moves = self.board.find_valid_move_cells(old_move)
        if depth == 0: random.shuffle(valid_moves)

        final_score = -INFINITY if flag == max_flag else +INFINITY
        optimal_move = None
        next_breadth = breadth * len(valid_moves)

        for current_move in valid_moves:
            self.advance(old_move, current_move, flag)

            current_score = self.minimax(board, current_move, opp_flag, flag, depth + 1, next_breadth, alpha, beta)
            self.backtrack(old_move, current_move, flag)

            if flag == max_flag:
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
    def advance(self, old_move, current_move, flag):
        self.board.update(old_move, current_move, flag)

    # undo a move, and update the heuristic estimate
    def backtrack(self, old_move, current_move, flag):
        x, y = current_move
        self.board.board_status[x][y] = '-'
        self.board.block_status[x >> 2][y >> 2] = '-'
