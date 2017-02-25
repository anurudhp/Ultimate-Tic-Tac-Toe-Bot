# Bot with minimax and alpha-beta with hashing, dynamic depth-setting, updated heuristics -> global boards
import random
import signal
import time
import copy
import datetime

class aiBot():
    def __init__(self, depth):
        self.max_depth = depth
        self.player = 'x'
        self.hashboard = [[0 for x in xrange(4)] for y in xrange(4)]
        self.exp3 = [3**x for x in xrange(16)]
        self.hashval = {}

    def board_update(self, board, new_move, ply):
        board.board_status[new_move[0]][new_move[1]] = ply
        x = new_move[0]/4
        y = new_move[1]/4
        fl = 0
        bs = board.board_status
        #checking if a block has been won or drawn or not after the current move
        for i in range(4):
            #checking for horizontal pattern(i'th row)
            if (bs[4*x+i][4*y] == bs[4*x+i][4*y+1] == bs[4*x+i][4*y+2] == bs[4*x+i][4*y+3]) and (bs[4*x+i][4*y] == ply):
                board.block_status[x][y] = ply
                return 'SUCCESSFUL'
            #checking for vertical pattern(i'th column)
            if (bs[4*x][4*y+i] == bs[4*x+1][4*y+i] == bs[4*x+2][4*y+i] == bs[4*x+3][4*y+i]) and (bs[4*x][4*y+i] == ply):
                board.block_status[x][y] = ply
                return 'SUCCESSFUL'
        # print "in update", new_move

        #checking for diagnol pattern
        if (bs[4*x][4*y] == bs[4*x+1][4*y+1] == bs[4*x+2][4*y+2] == bs[4*x+3][4*y+3]) and (bs[4*x][4*y] == ply):
            board.block_status[x][y] = ply
            return 'SUCCESSFUL'
        if (bs[4*x+3][4*y] == bs[4*x+2][4*y+1] == bs[4*x+1][4*y+2] == bs[4*x][4*y+3]) and (bs[4*x+3][4*y] == ply):
            board.block_status[x][y] = ply
            return 'SUCCESSFUL'

        #checking if a block has any more cells left or has it been drawn
        for i in range(4):
            for j in range(4):
                if bs[4*x+i][4*y+j] =='-':
                    return 'SUCCESSFUL'
        board.block_status[x][y] = 'd'

    def board_undo(self, board, new_move):
        # print "NEW_MOVE = ", new_move
        board.board_status[new_move[0]][new_move[1]] = '-'
        board.block_status[new_move[0]/4][new_move[1]/4] = '-'

    def addscore(self, cntx, cnto):
        single, double, triple, win = 1, 12, 80, 100000 #When won, it goes over 720, and so, in the calcheuristics, it goes to 720 
        score = 0
        if(cntx == 0):
            if(cnto == 1):
                score -= single
            elif(cnto == 2):
                score -= double
            elif(cnto == 3):
                score -= triple
            elif(cnto == 4):
                score -= win
        if(cnto == 0):
            if(cntx == 1):
                score += single
            elif(cntx == 2):
                score += double
            elif(cntx == 3):
                score += triple
            elif(cntx == 4):
                score += win
        return score

    def addscore2(self, cntx, cnto):
        single, double, triple, win = 1500, 4000, 28000, 1000000
        score = 0
        if(cntx == 0):
            if(cnto == 1):
                score -= single
            elif(cnto == 2):
                score -= double
            elif(cnto == 3):
                score -= triple
            elif(cnto == 4):
                score -= win

        if(cnto == 0):
            if(cntx == 1):
                score += single
            elif(cntx == 2):
                score += double
            elif(cntx == 3):
                score += triple
            elif(cntx == 4):
                score += win

        return score

    def calcheuristics(self, board, move, ply):
        score = 0
        multiplier = 1
        if(self.player == 'o'):
            multiplier = -1
        bs = board.board_status
        cntx, cnto = 0, 0
        block_scores = [[0 for i in xrange(4)] for j in xrange(4)]
        block_coefficients = [[4 for i in xrange(4)] for j in xrange(4)]
        for x_offset in xrange(0, 16, 4):
            for y_offset in xrange(0, 16, 4):
                board_score = 0
                if(self.hashboard[x_offset/4][y_offset/4] in self.hashval):
                    board_score = self.hashval[self.hashboard[x_offset/4][y_offset/4]]
                else:
                    for x in xrange(4):
                        cntx, cnto = 0, 0
                        for y in xrange(4):
                            if(bs[x_offset + x][y_offset + y] == 'x'):
                                cntx += 1
                            elif(bs[x_offset + x][y_offset + y] == 'o'):
                                cnto += 1
                        board_score += multiplier*self.addscore(cntx, cnto)

                    for y in xrange(4):
                        cntx, cnto = 0, 0
                        for x in xrange(4):
                            if(bs[x_offset + x][y_offset + y] == 'x'):
                                cntx += 1
                            elif(bs[x_offset + x][y_offset + y] == 'o'):
                                cnto += 1
                        board_score += multiplier*self.addscore(cntx, cnto)

                    cntx, cnto = 0, 0
                    for x in xrange(4):
                        if(bs[x_offset + x][y_offset + x] == 'x'):
                                cntx += 1
                        elif(bs[x_offset + x][y_offset + x] == 'o'):
                            cnto += 1
                    board_score += multiplier*self.addscore(cntx, cnto)

                    cntx, cnto = 0, 0
                    for x in xrange(4):
                        if(bs[x_offset + x][y_offset + 3 - x] == 'x'):
                                cntx += 1
                        elif(bs[x_offset + x][y_offset + 3 - x] == 'o'):
                            cnto += 1
                    board_score += multiplier*self.addscore(cntx, cnto)
                    if(board_score > 720):
                        board_score = 720
                    if(board_score < -720):
                        board_score = -720
                    self.hashval[self.hashboard[x_offset/4][y_offset/4]] = board_score
                block_scores[x_offset/4][y_offset/4] = board_score

        bs = board.block_status

        coeff1, coeff2, coeff3, coeff4, coeffm1 = 4, 8, 16, 32, 2

        totscore = 0
        for x in xrange(4):
            cntx, cnto = 0, 0
            currscore, val = 0, 0
            for y in xrange(4):
                currscore += block_scores[x][y]
                if(bs[x][y] == 'x'):
                    cntx += 1
                elif(bs[x][y] == 'o'):
                    cnto += 1

            # print "TESTME"
            totscore += multiplier*self.addscore2(cntx, cnto)
            # print multiplier*self.addscore2(cntx, cnto)

            if(cntx == 0 or cnto == 0):
                if(abs(currscore) >= 600):
                    val += coeff1
                elif(abs(currscore) >= 1200):
                    val += coeff2
                elif(abs(currscore) >= 1800):
                    val += coeff3
                elif(abs(currscore) >= 2160):
                    val += coeff4
            else:
                val -= coeffm1
            for y in xrange(4):
                block_coefficients[x][y] += val
                  
            # totscore += multiplier*self.addscore2(cntx, cnto)

        for y in xrange(4):
            cntx, cnto = 0, 0
            currscore, val = 0, 0
            for x in xrange(4):
                currscore += block_scores[x][y]
                if(bs[x][y] == 'x'):
                    cntx += 1
                elif(bs[x][y] == 'o'):
                    cnto += 1

            totscore += multiplier*self.addscore2(cntx, cnto)
            if(cntx == 0 or cnto == 0):
                if(abs(currscore) >= 600):
                    val += coeff1
                elif(abs(currscore) >= 1200):
                    val += coeff2
                elif(abs(currscore) >= 1800):
                    val += coeff3
                elif(abs(currscore) >= 2160):
                    val += coeff4
            else:
                val -= coeffm1
            for x in xrange(4):
                block_coefficients[x][y] += val
            # totscore += multiplier*self.addscore2(cntx, cnto)


        cntx, cnto = 0, 0
        currscore, val = 0, 0
        for x in xrange(4):
            currscore += block_scores[x][x]
            if(bs[x][x] == 'x'):
                cntx += 1
            elif(bs[x][x] == 'o'):
                cnto += 1
        
        totscore += multiplier*self.addscore2(cntx, cnto)
        if(cntx == 0 or cnto == 0):
            if(abs(currscore) >= 600):
                val += coeff1
            elif(abs(currscore) >= 1200):
                val += coeff2
            elif(abs(currscore) >= 1800):
                val += coeff3
            elif(abs(currscore) >= 2160):
                val += coeff4
        else:
            val -= coeffm1
        for x in xrange(4):
            block_coefficients[x][x] += val


        cntx, cnto = 0, 0
        currscore, val = 0, 0
        for x in xrange(4):
            currscore += block_scores[x][3-x]
            if(bs[x][3-x] == 'x'):
                cntx += 1
            elif(bs[x][3-x] == 'o'):
                cnto += 1
        totscore += multiplier*self.addscore2(cntx, cnto)
        if(cntx == 0 or cnto == 0):
            if(abs(currscore) >= 600):
                val += coeff1
            elif(abs(currscore) >= 1200):
                val += coeff2
            elif(abs(currscore) >= 1800):
                val += coeff3
            elif(abs(currscore) >= 2160):
                val += coeff4
        else:
            val -= coeffm1
        for x in xrange(4):
            block_coefficients[x][3-x] += val

        for i in xrange(4):
            for j in xrange(4):
                score += block_coefficients[i][j] * block_scores[i][j]

        if(totscore > 100000):
            totscore = 100000
        if(totscore < -100000):
            totscore = -100000

        score += totscore
        # cntx, cnto = 0, 0
        # for x in xrange(4):
        #     if(bs[x][3 - x] == 'x'):
        #         cntx += 1
        #     elif(bs[x][3 - x] == 'o'):
        #         cnto += 1
        # totscore += multiplier*self.addscore2(cntx, cnto)
        
        # if(totscore > 100000):
        #     totscore = 100000
        # if(totscore < -100000):
        #     totscore = -100000

        # score += totscore

        openboard_coeff = 1000

        if(board.block_status[move[0]%4][move[1]%4] != '-'):
            if(ply != self.player):
                score -= openboard_coeff
            else:
                score += openboard_coeff

        # print score

        return score

    def minimax(self, board, flag, old_move, current_depth, ismax, alpha, beta):

        # print current_depth

        if current_depth == self.max_depth:
            # print current_depth
            temp = ((-1, -1), self.calcheuristics(board, old_move, flag))
            # print "calcheuristics = ", temp
            return temp

        elif ismax == 1:
            legal = board.find_valid_move_cells(old_move)

            random.shuffle(legal)
            maxval = -1000000
            if(len(legal) == 0):
                return ((-1, -1), self.calcheuristics(board, old_move, flag))

            for move in legal:
                # print "TEST"
                # print move
                self.board_update(board, move, flag)
                val = 0
                if(flag == 'x'):
                    val = 1
                elif(flag == 'o'):
                    val = 2

                self.hashboard[move[0]/4][move[1]/4] += val*self.exp3[4*(move[0]%4) + move[1]%4]
                # print "move again", move
                # board.print_board()
                if flag == 'x':
                    temp = self.minimax(board, 'o', move, current_depth+1, 0, alpha, beta)
                else:
                    temp = self.minimax(board, 'x', move, current_depth+1, 0, alpha, beta)

                self.board_undo(board, move)
                self.hashboard[move[0]/4][move[1]/4] -= val*self.exp3[4*(move[0]%4) + move[1]%4]

                if temp[1] > maxval:
                    maxval = temp[1]
                    retmove = move

                alpha = max(alpha, maxval)

                if beta <= alpha:
                    break

                # board.print_board()

            return (retmove, maxval)

        else:
            legal = board.find_valid_move_cells(old_move)
            random.shuffle(legal)
            minval = 1000000
            if(len(legal) == 0):
                return ((-1, -1), self.calcheuristics(board, old_move, flag))
            for move in legal:
                self.board_update(board, move, flag)

                val = 0
                if(flag == 'x'):
                    val = 1
                elif(flag == 'o'):
                    val = 2

                self.hashboard[move[0]/4][move[1]/4] += val*self.exp3[4*(move[0]%4) + move[1]%4]
                # print move
                if flag == 'x':
                    temp = self.minimax(board, 'o', move, current_depth+1, 1, alpha, beta)
                else:
                    temp = self.minimax(board, 'x', move, current_depth+1, 1, alpha, beta)

                self.board_undo(board, move)
                self.hashboard[move[0]/4][move[1]/4] -= val*self.exp3[4*(move[0]%4) + move[1]%4]

                if temp[1] < minval:
                    minval = temp[1]
                    retmove = move

                beta = min(minval, beta)
                if beta <= alpha:
                    break

                
                # print "AFTER = ", (retmove, min)

            return (retmove, minval)

    def sethash(self, board):
        for x_offset in xrange(4):
            for y_offset in xrange(4):
                for x in xrange(4):
                    for y in xrange(4):
                        val = 0
                        if(board.board_status[4*x_offset + x][4*y_offset + y] == 'x'):
                            val = 1
                        elif(board.board_status[4*x_offset + x][4*y_offset + y] == 'o'):
                            val = 2    
                        self.hashboard[x_offset][y_offset] += val*self.exp3[4*x + y]


    def move(self, board, old_move, flag):
        #You have to implement the move function with the same signature as this
        #Find the list of valid cells allowed
        # cells = board.find_valid_move_cells(old_move)
        # x = cells[random.randrange(len(cells))]
        # print "TEST"

        self.player = flag

        self.sethash(board)

        # begin = datetime.datetime.utcnow()
        # for i in xrange(37732311):
        #     x = board.board_status[0][0]
        #     # for j in xrange(16):
        #     #     x = board.board_status[0][j]
        # print datetime.datetime.utcnow() - begin
        legal = board.find_valid_move_cells(old_move)
        if(len(legal) > 16):
            self.max_depth = 5
        temp = self.minimax(board, flag, old_move, 1, 1, -1000000, +1000000)
        self.max_depth = 6
        # print "FINAL = "
        print temp[0]
        # print x
        return temp[0]