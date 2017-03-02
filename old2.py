import random
import copy
import sys

def evaluate(board, flag):
    SCORE_BLOCK  = 10**9
    SCORE_CELL   = 10**6
    SCORE_PAIR   = 10**3
    SCORE_TRIPLE = 10**0
    SCORE_GAME_CELL   = 10**6
    SCORE_GAME_PAIR   = 10**3
    SCORE_GAME_TRIPLE = 10**0
    WEIGHT_ATTACK = 10**3
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

    return (WEIGHT_ATTACK*attack_score + WEIGHT_GAME*game_score, my_block_score, opp_block_score)

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

def backtrack_move(board, old_move, new_move, flag):
    x, y = new_move
    board.board_status[x][y] = '-'
    board.block_status[x / 4][y / 4] = '-'
    return

INFINITY = 10**18
class Player54():
    def __init__(self, max_depth = 2, must_prune = True):
        self.max_depth = max_depth
        self.must_prune = must_prune
        print self.must_prune
        random.seed()

    def move(self, board, old_move, flag):
        # create copy and bind functions
        board = copy.deepcopy(board)
        board.backtrack = backtrack_move.__get__(board)
        board.evaluate = evaluate.__get__(board)
        # board.count_attacks = count_attacks.__get__(board)

        # search
        opp_flag = 'x' if flag == 'o' else 'o'
        play_move = self.minimax(board, old_move, flag, opp_flag, flag)

        print play_move
        return play_move[1]

    # search functions
    def minimax(self, board, old_move, flag, opp_flag, max_flag, depth = 0, alpha = -INFINITY, beta = +INFINITY):
        terminal = board.find_terminal_state()
        if terminal[0] != 'CONTINUE':
            if terminal[0] == max_flag: return INFINITY
            if terminal[0] == 'NONE':
                return board.evaluate(max_flag)
            return -INFINITY

        if depth >= self.max_depth:
            return board.evaluate(max_flag)

        valid_moves = board.find_valid_move_cells(old_move)
        if depth == 0: random.shuffle(valid_moves)
        final_score = -INFINITY if flag == max_flag else +INFINITY

        optimal_move = None
        for move in valid_moves:
            board.update(old_move, move, flag)
            current_score = self.minimax(board, move, opp_flag, flag, max_flag, depth + 1, alpha, beta)
            board.backtrack(old_move, move, flag)

            if flag == max_flag:
                if final_score <= current_score:
                    final_score = current_score
                    optimal_move = move
                alpha = max(alpha, final_score)
            else:
                if final_score >= current_score:
                    final_score = current_score
                    optimal_move = move
                beta = min(beta, final_score)

            if self.must_prune and beta <= alpha: break

        if depth == 0: return final_score, optimal_move
        return final_score
