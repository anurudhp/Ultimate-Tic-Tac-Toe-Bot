import simulator
infinity = 100000000000
ref_block = [[1 for i in xrange(4)] for j in xrange(4)]
ref_board = [[1 for i in xrange(16)] for j in xrange(16)]

for i in xrange(4):
        for j in xrange(4):
            if(i == j and (i == 3 or i == 0)):
                    ref_block[i][j] = 2
            elif ((i == 0 and  j == 3) or (i == 3 and j == 0) ):
                    ref_block[i][j] = 2
            elif((i == j and (i == 2 or i == 1)) or ((i == 1 and j == 2) or (j == 1 and i == 2))):
                    ref_block[i][j] = 3

            ref_board[4*i+1][4*j+1] = 3
            ref_board[4*i+2][4*j+1] = 3
            ref_board[4*i+1][4*j+2] = 3
            ref_board[4*i+2][4*j+2] = 3
            ref_board[4*i][4*j] = 2
            ref_board[4*i+3][4*j] = 2
            ref_board[4*i+3][4*j+3] = 2
            ref_board[4*i][4*j+3] = 2

class AI_BOT():
        # ref_block = [[1 for i in xrange(4)] for j in xrange(4)]
        # ref_board = [[1 for i in xrange(16)] for j in xrange(16)]
        #
        # for i in xrange(4):
        #         for j in xrange(4):
        #             if(i == j and (i == 3 or i == 0)):
        #                     ref_block[i][j] = 2
        #             elif ((i == 0 and  j == 3) or (i == 3 and j == 0) ):
        #                     ref_block[i][j] = 2
        #             elif((i == j and (i == 2 or i == 1)) or ((i == 1 and j == 2) or (j == 1 and i == 2))):
        #                     ref_block[i][j] = 3
        #
        #             ref_board[4*i+1][4*j+1] = 3
        #             ref_board[4*i+2][4*j+1] = 3
        #             ref_board[4*i+1][4*j+2] = 3
        #             ref_board[4*i+2][4*j+2] = 3
        #             ref_board[4*i][4*j] = 2
        #             ref_board[4*i+3][4*j] = 2
        #             ref_board[4*i+3][4*j+3] = 2
        #             ref_board[4*i][4*j+3] = 2

	def __init__(self,depth):
            self.d = depth



	def eval_fun(self,board,flag):
            score = 0
            if(flag == 'x'):
                nflag = 'o'
            else:
                nflag = 'x'
            for i in xrange(16):
                for j in xrange(16):
                    # print(i,j)
                    if (ref_board[i][j] == 3):
                        if(board.board_status[i][j] == flag):
                            score += 1000
                        else:
                            score -= 1000
                    elif (ref_board[i][j] == 2):
                        if(board.board_status[i][j] == flag):
                            score += 300
                        else:
                            score -= -300
                    else:
                        if(board.board_status[i][j] == flag):
                            score += 50
                        else:
                            score -= 50

            for i in xrange(4):
                for j in xrange(4):
                    if ( board.block_status[i][j] == flag):
                        if(ref_block[i][j] == 3):
                            score += 10000
                        elif(ref_block[i][j] == 2):
                            score += 800
                        elif(ref_block[i][j] == 1):
                            score += 40
                    else:
                        if(ref_block[i][j] == 3):
                            score -= 10000
                        elif(ref_block[i][j] == 2):
                            score -= 800
                        elif(ref_block[i][j] == 1):
                            score -= 40


            for l in xrange(4):
                for i in xrange(4):
                    for j in xrange(4):
                        fc = 0
                        nfc = 0
                        for k in xrange(4):
                            if(board.board_status[4*l + k][4*i + j] == flag):
                                fc += 1
                            elif(board.board_status[4*l + k][4*i + j] == nflag):
                                nfc += 1
                        if(fc == 2 and nfc == 0):
                            score += 3000
                        elif(fc == 3 and nfc == 0):
                            score += 6000
            for l in xrange(4):
                for i in xrange(4):
                    for j in xrange(4):
                        fc = 0
                        nfc = 0
                        for k in xrange(4):
                            if(board.board_status[4*l + j][4*i + k] == flag):
                                fc += 1
                            elif(board.board_status[4*l + j][4*i + k] == nflag):
                                nfc += 1
                        if(fc == 2 and nfc == 0):
                            score += 3000
                        elif(fc == 3 and nfc == 0):
                            score += 6000
                    

            return score


	def move(self,board,old_move,flag):
            if(flag == 'x'):
                cflag = 'o'
            else:
                cflag = 'x'
            temp,move = self.alpha_beta_search(old_move,self.d,-1*infinity,infinity,1,board,flag,cflag)
            return move



	def alpha_beta_search(self, parent , depth, alpha , beta  , maximizer,board,flag,cflag):
            # print(depth)
            is_terminal = board.find_terminal_state()
            term = is_terminal[0]
    #        print(maximizer)
            if(depth == 0 or term != "CONTINUE"):
                    x = self.eval_fun(board,flag)
                    return x
                #Calculate and return heuristics
            if(maximizer == 1):
        		#	print(parent)
        			v = -1 * infinity
        			maxval = v
        			maxmove =[]
        			children = board.find_valid_move_cells(parent)
        			for child in children :
        			        board.update(parent,child,flag)
        			        upd = self.alpha_beta_search(child,depth -1,alpha,beta,0,board,flag,cflag)
        			        v = max(v , upd )
        			        if(v > maxval):
        			            maxmove = child
        			        board.board_status[child[0]][child[1]] = '-'
        			        if board.block_status[child[0]/4][child[1]/4] != '-':
        			            board.block_status[child[0]/4][child[1]/4] = '-'

        			        alpha = max(alpha,v)
        			        if beta <= alpha:
        			                break
        			return v,maxmove
            else:
        			v = infinity
        			minval = v
        			minmove = []
        			children = board.find_valid_move_cells(parent)
        			for child in children :
        			         board.update(parent,child,cflag)
        			         upd = self.alpha_beta_search(child,depth -1,alpha,beta,1,board,flag,cflag)
        			         v = min(v,upd)
        			         if(v < minval):
        			                 minmove = child
        			         board.board_status[child[0]][child[1]] = '-'
        			         if board.block_status[child[0]/4][child[1]/4] != '-':
        			                 board.block_status[child[0]/4][child[1]/4] = '-'
        			         beta = min(beta,v)
        			         if beta <= alpha:
        			                 break
        			return v,minmove
