
class Player54():
    def __init__(self):
        pass
    def move(self, board, old_move, flag):
        # bind functions
        board.backtrack_move = self.backtrack_move.__get__(board)
        board.evaluate = self.evaluate.__get__(board)

        play_move = self.minimax(board, old_move, flag, 0)

        while True: pass
        return play_move

    # search functions
    def minimax(self, board, old_move, flag, depth):
        if depth >= 5:
            return board.evaluate(flag)
        valid_moves = board.find_valid_move_cells(old_move)
        for move in valid_moves:


    # bind to board
    def evaluate(board, flag):
        SCORE_BLOCK_WIN = 1000
        SCORE_THREE = 200
        SCORE_TWO = 50
        score = 0

        oppflag = 'x' if flag == 'o' else 'x'

        bs = board.board_status
        for i in xrange(0, 4):
            for j in xrange(0, 4):
                if board.block_status[i][j] == flag:
                    score += SCORE_BLOCK_WIN
                else if board.block_status[i][j] == '-':
                    for i in xrange(0, 4):
                        for j in xrange(0, 2):
                            if bs[i][j] == flag and bs[i][j + 1] == flag:
                                score += SCORE_TWO
                            else if bs[i][j] ==
                else:
                    score -= SCORE_BLOCK_WIN
        pass
    def backtrack_move(board):
        pass
