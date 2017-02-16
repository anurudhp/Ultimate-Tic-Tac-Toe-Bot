
class Player54():
    def __init__(self):
        pass
    def move(self, board, old_move, flag):
        # bind functions
        board.backtrack_move = self.backtrack_move.__get__(board)
        board.evaluate = self.evaluate.__get__(board)
        board.countAttacks = self.countAttacks.__get__(board)

        play_move = self.minimax(board, old_move, flag, 0)

        while True: pass
        return play_move

    # search functions
    def minimax(self, board, old_move, flag, depth):
        if depth >= 5:
            return board.evaluate(flag)
        valid_moves = board.find_valid_move_cells(old_move)
        if (depth & 1) == 1:
            ret = 1000000000
        else:
            ret = 0
        for move in valid_moves:
            board.update(old_move, move, flag)
            curr = self.minimax(board, move, flag, depth + 1)
            board.backtrack_move(old_move, move)
            if (depth & 1) == 1:
                ret = min(ret, curr)
            else:
                ret = max(ret, curr)
        return ret
    # bound to board
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
                else if board.block_status[i][j] == '-':
                    myAttacks = countAttacks(flag, i, j)
                    score += SCORE_TWO*myAttacks[0] + SCORE_THREE*myAttacks[1]
                    oppAttacks = countAttacks(oppflag, i, j)
                    score -= SCORE_TWO*oppAttacks[0] + SCORE_THREE*oppAttacks[1]
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

    def backtrack_move(board):
        pass
