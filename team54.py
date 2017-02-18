import random
import copy
import sys

def evaluate(board, flag):
    SCORE_BLOCK_WIN = 10**15
    SCORE_WIN_CELL  = 10**10
    SCORE_WIN_PAIR  = 10**0
    SCORE_GAME_WIN_CELL = 10**12
    SCORE_GAME_WIN_PAIR = 10**7

    score = 0
    oppflag = 'x' if flag == 'o' else 'o'

    for i in xrange(0, 4):
        for j in xrange(0, 4):
            if board.block_status[i][j] == flag:
                score += SCORE_BLOCK_WIN
            elif board.block_status[i][j] == '-':
                myAttacks = count_attacks(board.board_status, flag, i, j)
                oppAttacks = count_attacks(board.board_status, oppflag, i, j)

                score += SCORE_WIN_PAIR*(myAttacks[0]) + SCORE_WIN_CELL*(myAttacks[1])
                score -= SCORE_WIN_PAIR*(oppAttacks[0]) + SCORE_WIN_CELL*(oppAttacks[1])
            else:
                score -= SCORE_BLOCK_WIN

    # block level
    myAttacks = count_attacks(board.block_status, flag, 0, 0)
    oppAttacks = count_attacks(board.block_status, oppflag, 0, 0)

    score += SCORE_GAME_WIN_PAIR*(myAttacks[0]) + SCORE_GAME_WIN_CELL*(myAttacks[1])
    score -= SCORE_GAME_WIN_PAIR*(oppAttacks[0]) + SCORE_GAME_WIN_CELL*(oppAttacks[1])

    return score

def count_attacks(board, flag, row, col):
    l = 4*col
    r = l + 4
    u = 4*row
    d = u + 4
    win_pairs = 0
    win_cells = 0
    count = [[4*[0] for i in xrange(0, 4)] for i in xrange(0, 3)]

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

    for row in count[0]:
        win_cells += row.count(1)
    win_cells = win_cells**2

    for row in count[1]:
        for elem in row:
            win_pairs += elem*elem

    return (win_pairs, win_cells)

def backtrack_move(board, old_move, new_move, flag):
    x, y = new_move
    board.board_status[x][y] = '-'
    board.block_status[x / 4][y / 4] = '-'
    return

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
            count[len(ans) - 1][pos[0] % 4][pos[1] % 4] += 1

INFINITY = 10**18
class Player54():
    def __init__(self, max_depth = 3, must_prune = True):
        self.max_depth = max_depth
        self.must_prune = must_prune
        print self.must_prune
        random.seed()

    def move(self, board, old_move, flag):
        # create copy and bind functions
        board = copy.deepcopy(board)
        board.backtrack_move = backtrack_move.__get__(board)
        board.evaluate = evaluate.__get__(board)
        # board.count_attacks = count_attacks.__get__(board)

        # search
        opp_flag = 'x' if flag == 'o' else 'o'
        play_move = self.minimax(board, old_move, flag, opp_flag, flag)
        # self.must_prune = not self.must_prune
        # play_move2 = self.minimax(board, old_move, flag, opp_flag, flag)
        # self.must_prune = not self.must_prune

        # diff_len = len(play_move[1]) - len(play_move2[1])
        # if diff_len != 0: sys.stderr.write(str(diff_len) + '\n')
        # assert (play_move[0] == play_move2[0])
        print play_move
        return play_move[1]

    # search functions
    def minimax(self, board, old_move, flag, opp_flag, max_flag, depth = 0, alpha = -INFINITY, beta = +INFINITY):
        terminal = board.find_terminal_state()
        heuristic_estimate = board.evaluate(max_flag)
        if terminal[0] != 'CONTINUE':
            if terminal[0] == flag: return INFINITY
            if terminal[0] == 'NONE':
                return heuristic_estimate
            return -INFINITY

        if depth >= self.max_depth:
            return heuristic_estimate

        valid_moves = board.find_valid_move_cells(old_move)
        random.shuffle(valid_moves)
        final_score = -INFINITY if flag == max_flag else +INFINITY

        optimal_move = None
        for move in valid_moves:
            board.update(old_move, move, flag)
            current_score = self.minimax(board, move, opp_flag, flag, max_flag, depth + 1, alpha, beta)
            board.backtrack_move(old_move, move, flag)

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
