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
    r = l + 4
    u = 4*row
    d = u + 4
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
    update_count(count, board.board_status, flag, [(u, l + 3), (u + 1, l + 2), (u + 2, l + 1), (u + 3, l)])

    # back diagonal
    update_count(count, board.board_status, flag, [(u, l), (u + 1, l + 1), (u + 2, l + 2), (u + 3, l + 3)])

    for row in count[0]:
        win_cells += row.count(1)
    win_cells = win_cells**2

    for row in count[1]:
        for elem in row:
            win_pairs += elem*elem

    return (win_pairs, win_cells)

def backtrack_move(board, old_move, new_move):
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

class Player54():
    def __init__(self):
        random.seed()
        
    def move(self, board, old_move, flag):
        # bind functions
        board.backtrack_move = backtrack_move.__get__(board)
        board.evaluate = evaluate.__get__(board)
        board.count_attacks = count_attacks.__get__(board)

        # search
        play_move = self.minimax(board, old_move, flag, 0)
        print play_move
        return play_move[1]

    # search functions
    def minimax(self, board, old_move, flag, depth):
        INFINITY = 10**18
        terminal = board.find_terminal_state()
        if terminal[0] != 'CONTINUE':
            if terminal[0] == flag: return (INFINITY, old_move)
            if terminal[0] == 'NONE':
                return (board.evaluate(flag), old_move)
            return (-INFINITY, old_move)

        if depth >= 2:
            heu = board.evaluate(flag)
            return (heu, old_move)

        valid_moves = board.find_valid_move_cells(old_move)
        if (depth & 1) == 1:
            ret = INFINITY
        else:
            ret = -INFINITY
        optimal_moves = []
        for move in valid_moves:
            board.update(old_move, move, flag)
            curr = self.minimax(board, move, flag, depth + 1)
            board.backtrack_move(old_move, move)

            if ret == curr[0]:
                optimal_moves.append(move)
            elif (depth & 1) == 1:
                if curr[0] < ret:
                    optimal_moves = [move]
                    ret = curr[0]
            else:
                if curr[0] > ret:
                    optimal_moves = [move]
                    ret = curr[0]
        
        return (ret, random.choice(optimal_moves))
