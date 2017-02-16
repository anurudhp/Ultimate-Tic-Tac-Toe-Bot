import random

def evaluate(board, flag):
    SCORE_BLOCK_WIN = 1000
    SCORE_THREE = 200
    SCORE_TWO = 50
    score = 0

    oppflag = 'x' if flag == 'o' else 'x'

    for i in xrange(0, 4):
        for j in xrange(0, 4):
            if board.block_status[i][j] == flag:
                score += SCORE_BLOCK_WIN
            elif board.block_status[i][j] == '-':
                myAttacks = board.countAttacks(flag, i, j)
                score += SCORE_TWO*(myAttacks[0]**2) + SCORE_THREE*(myAttacks[1]**2)
                oppAttacks = board.countAttacks(oppflag, i, j)
                score -= SCORE_TWO*(oppAttacks[0]**2) + SCORE_THREE*(oppAttacks[1]**2)
            else:
                score -= SCORE_BLOCK_WIN
    return score

def countAttacks(board, flag, row, col):
    bs = board.board_status
    l = 4*col
    r = l + 3
    u = 4*row
    d = u + 3
    twos = 0
    threes = 0

    #rows and columns
    for i in xrange(u, d):
        for j in xrange(l, r):
            if j + 1 <= r and bs[i][j] == flag and bs[i][j + 1] == flag:
                if j + 2 <= r and bs[i][j + 2] == flag:
                    threes += 1
                    twos -= 1
                else:
                    twos += 1
            if i + 1 <= d and bs[i][j] == flag and bs[i + 1][j] == flag:
                if i + 2 <= d and bs[i + 2][j] == flag:
                    threes += 1
                    twos -= 1
                else:
                    twos += 1

    # diagonals
    for x in xrange(0, 2):
        i = u + x
        j = r - 1 - x
        if i + 1 <= d and l <= j - 1 and bs[i][j] == flag and bs[i + 1][j - 1] == flag:
            if i + 2 <= d and l <= j - 2 and bs[i + 2][j - 2] == flag:
                threes += 1
                twos -= 1
            else:
                twos += 1

        j = l + x
        if i + 1 <= d and j + 1 <= r and bs[i][j] == flag and bs[i + 1][j + 1] == flag:
            if i + 2 <= d and j + 2 <= r and bs[i + 2][j + 2] == flag:
                threes += 1
                twos -= 1
            else:
                twos += 1

    return (twos, threes)

def backtrack_move(board, old_move, new_move):
    x, y = new_move
    board.board_status[x][y] = '-'
    board.block_status[x / 4][y / 4] = '-'
    return

class Player54():
    def __init__(self):
        random.seed()
        
    def move(self, board, old_move, flag):
        # bind functions
        board.backtrack_move = backtrack_move.__get__(board)
        board.evaluate = evaluate.__get__(board)
        board.countAttacks = countAttacks.__get__(board)

        # search
        play_move = self.minimax(board, old_move, flag, 0)
        print play_move
        return play_move[1]

    # search functions
    def minimax(self, board, old_move, flag, depth):
        INFINITY = 10**9
        terminal = board.find_terminal_state()
        if terminal[0] != 'CONTINUE':
            if terminal[1] == flag: return (INFINITY, old_move)
            if terminal[1] == 'NONE':
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
            else:
                if curr[0] > ret:
                    optimal_moves = [move];
        return (ret, random.choice(optimal_moves))
