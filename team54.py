import random

def evaluate(board, flag):
    SCORE_BLOCK_WIN = 10**16
    SCORE_WIN_CELL  = 10**8
    SCORE_WIN_PAIR  = 10**0

    score = 0
    oppflag = 'x' if flag == 'o' else 'o'

    for i in xrange(0, 4):
        for j in xrange(0, 4):
            if board.block_status[i][j] == flag:
                score += SCORE_BLOCK_WIN
            elif board.block_status[i][j] == '-':
                myAttacks = board.count_attacks(flag, i, j)
                score += SCORE_WIN_PAIR*(myAttacks[0]) + SCORE_WIN_CELL*(myAttacks[1])
                oppAttacks = board.count_attacks(oppflag, i, j)
                score -= SCORE_WIN_PAIR*(oppAttacks[0]) + SCORE_WIN_CELL*(oppAttacks[1])
            else:
                score -= SCORE_BLOCK_WIN
    return score

def count_attacks(board, flag, row, col):
    l = 4*col
    r = l + 3
    u = 4*row
    d = u + 3
    win_pairs = 0
    win_cells = 0
    count = [[4*[0] for i in xrange(0, 4)] for i in xrange(0, 3)]

    # rows
    for i in xrange(u, d):
        update_count(count, board.board_status, flag, [(i, l), (i, l + 1), (i, l + 2), (i, l + 3)])

    # cols
    for j in xrange(l, r):
        update_count(count, board.board_status, flag, [(u, j), (u + 1, j), (u + 2, j), (u + 3, j)])

    # main diagonal
    update_count(count, board.board_status, flag, [(u, r), (u + 1, r - 1), (u + 2, r - 2), (u + 3, r - 3)])

    # back diagonal
    update_count(count, board.board_status, flag, [(u, l), (u + 1, l + 1), (u + 2, l + 2), (u + 3, l + 3)])

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
    def __init__(self):
        random.seed()

    def move(self, board, old_move, flag):
        # bind functions
        board.backtrack_move = backtrack_move.__get__(board)
        board.evaluate = evaluate.__get__(board)
        board.count_attacks = count_attacks.__get__(board)

        # search
        play_move = self.minimax(board, old_move, flag)
        print play_move
        return play_move

    # search functions
    def minimax(self, board, old_move, flag, depth = 0, alpha = -INFINITY, beta = +INFINITY, isMaxPlayer = True):
        terminal = board.find_terminal_state()
        if terminal[0] != 'CONTINUE':
            if terminal[0] == flag: return INFINITY
            if terminal[0] == 'NONE':
                return board.evaluate(flag)
            return -INFINITY

        if depth >= 3:
            return board.evaluate(flag)

        valid_moves = board.find_valid_move_cells(old_move)
        final_score = -INFINITY if isMaxPlayer else +INFINITY

        if depth == 0: optimal_moves = []
        for move in valid_moves:
            board.update(old_move, move, flag)
            current_score = self.minimax(board, move, flag, depth + 1, alpha, beta, not isMaxPlayer)
            board.backtrack_move(old_move, move, flag)

            if isMaxPlayer:
                if final_score < current_score:
                    final_score = current_score
                    if depth == 0: optimal_moves = [move]
                elif depth == 0 and final_score == current_score:
                    optimal_moves.append(move)
                alpha = max(alpha, final_score)
            else:
                if final_score > current_score:
                    final_score = current_score
                    if depth == 0: optimal_moves = [move]
                elif depth == 0 and final_score == current_score:
                    optimal_moves.append(move)
                beta = min(beta, final_score)

            if beta <= alpha: break # cutoff

        if depth == 0: return random.choice(optimal_moves)
        return final_score
