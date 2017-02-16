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
    l = 4*col
    r = l + 3
    u = 4*row
    d = u + 3
    twos = 0
    threes = 0
    is_win_cell = [4*[False] for i in xrange(0, 4)]

    # rows
    for i in xrange(u, d):
        reqList = getWinReq(board.board_status, flag, [(i, l), (i, l + 1), (i, l + 2), (i, l + 3)])
        if len(reqList) == 2:
            twos += 1
        elif len(reqList) == 1:
            is_win_cell[reqList[0][0] - u][reqList[0][1] - l] = True

    # cols
    for j in xrange(l, r):
        reqList = getWinReq(board.board_status, flag, [(u, j), (u + 1, j), (u + 2, j), (u + 3, j)])
        if len(reqList) == 2:
            twos += 1
        elif len(reqList) == 1:
            is_win_cell[reqList[0][0] - u][reqList[0][1] - l] = True

    # main diagonal
    reqList = getWinReq(board.board_status, flag, [(u, r), (u + 1, r - 1), (u + 2, r - 2), (u + 3, r - 3)])
    if len(reqList) == 2:
        twos += 1
    elif len(reqList) == 1:
        is_win_cell[reqList[0][0] - u][reqList[0][1] - l] = True

    # reverse diagonal
    reqList = getWinReq(board.board_status, flag, [(u, l), (u + 1, l + 1), (u + 2, l + 2), (u + 3, l + 3)])
    if len(reqList) == 2:
        twos += 1
    elif len(reqList) == 1:
        is_win_cell[reqList[0][0] - u][reqList[0][1] - l] = True

    for row in is_win_cell:
        threes += row.count(True)

    return (twos, threes)

def backtrack_move(board, old_move, new_move):
    x, y = new_move
    board.board_status[x][y] = '-'
    board.block_status[x / 4][y / 4] = '-'
    return

def getWinReq(board, flag, posList):
    ans = []
    for pos in posList:
        elem = board[pos[0]][pos[1]]
        if elem == '-':
            ans.append(pos)
        elif elem != flag:
            ans = []
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
