import random

def evaluate(board, flag):
    SCORE_BLOCK_WIN = 10**10
    SCORE_THREE     = 10**5
    SCORE_TWO       = 10**0

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

    # rows
    for i in xrange(u, d):
        count = countElems(flag, [bs[i][l], bs[i][l + 1], bs[i][l + 2], bs[i][l + 3]])
        if count == 2:
            twos += 1
        elif count == 3:
            threes += 1

    # cols
    for j in xrange(l, r):
        count = countElems(flag, [bs[u][j], bs[u + 1][j], bs[u + 2][j], bs[u + 3][j]])
        if count == 2:
            twos += 1
        elif count == 3:
            threes += 1
    
    # main diagonal
    count = countElems(flag, [bs[u][r], bs[u + 1][r - 1], bs[u + 2][r - 2], bs[u + 3][r - 3]])
    if count == 2:
        twos += 1
    elif count == 3:
        threes += 1    

    count = countElems(flag, [bs[u][l], bs[u + 1][l + 1], bs[u + 2][l + 2], bs[u + 3][l + 3]])
    if count == 2:
        twos += 1
    elif count == 3:
        threes += 1

    return (twos, threes)

def backtrack_move(board, old_move, new_move):
    x, y = new_move
    board.board_status[x][y] = '-'
    board.block_status[x / 4][y / 4] = '-'
    return

def countElems(flag, elemList):
    ans = 0
    for elem in elemList:
        if elem == flag:
            ans += 1
        elif elem != '-':
            ans = 0
            break
    return ans

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
        INFINITY = 10**18
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
            # print ret, curr[0]
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
        # print ">>>>>>>> move list: ", optimal_moves
        return (ret, random.choice(optimal_moves))
