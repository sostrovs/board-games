import copy
import sys
import random


class Connect4():

    winners = ('X-win', 'Draw', 'O-win')

    def __init__(self, row, col, max_path=4):
        self.cur_row = 0
        self.cur_col = 0
        self.max_path = max_path
        self.squares = self.create_board(row, col)
        self.row = row
        self.col = col
        self.players = {'computer':'0', 'player':'x'}

    def choosePlayer(self, player):
        if self.players['player'] != player:
            self.players['computer'] = self.players['player']
            self.players['player'] = player


    def create_board(self, r, c):
        squares = []
        for column in range(r):
            row = ['*'] * c
            squares.append(row)

        return squares


    def display_board(self, squares):
        for row in range(len(squares)):
            print ' '.join(str(v) for v in squares[row])


    def check_winner(self):
        for player in ['x', '0']:
            # squares = self.reduce_board(self.squares, self.cur_row, self.cur_col)
            squares = self.squares
            # check diagonal paths
            diagonal_paths = self.create_diagonal_paths(squares)
            for path in diagonal_paths:
                if path.count(player) == self.max_path:
                    # self.display_board(squares)
                    # print "-" * 100
                    return player

            # check row paths
            for i in range(len(squares)):
                for j in range(len(squares)- (self.max_path - 1)):
                    if squares[i][j:(j+self.max_path)].count(player) == self.max_path:
                        return player

            # check column paths
            column_board = zip(*squares)
            # column_board = self.create_column_board(squares)
            for i in range(len(column_board)):
                for j in range(len(column_board) - (self.max_path-1)):
                    if column_board[i][j:(j+self.max_path)].count(player) == self.max_path:
                        return player



        return None


    def available_moves(self):
        moves = []
        for i in xrange(len(self.squares)):
            for j in xrange(len(self.squares[i])):
                if self.squares[i][j] == '*':
                    moves.append([i, j])

        return moves


    def create_diagonal_paths(self, squares):
        diagonal_paths = []
        for i in range((self.max_path-1), len(squares)):
            for j in range(len(squares[i])-(self.max_path-1)):
                path = []
                for p in range(self.max_path):
                    path.append(squares[i-p][j+p])
                diagonal_paths.append(path)

        for i in range(len(squares)-(self.max_path-1)):
            for j in range(len(squares[i])-(self.max_path-1)):
                path = []
                for p in range(self.max_path):
                    path.append(squares[i+p][j+p])
                diagonal_paths.append(path)

        return diagonal_paths


    def reduce_board(self, squares, row, col):
        start_row = row - (self.max_path - 1)
        end_row = row + self.max_path
        start_col = col - (self.max_path - 1)
        end_col = col + self.max_path

        if start_row < 0:
            start_row = 0

        if start_col < 0:
            start_col = 0

        if end_row > len(squares[0]):
            end_row = len(squares[0])

        if end_col > len(squares):
            end_col = len(squares)

        hboard = squares[start_row:end_row]
        vboard = zip(*hboard)
        reduced_vboard = vboard[start_col:end_col]
        reduced_board = zip(*reduced_vboard)
        # print "-" * 100
        # self.display_board(reduced_board)
        return reduced_board


    def create_column_board(self, squares):
        column_board = self.create_board(self.row, self.col)
        for column in range(len(column_board)):
            for row in range(len(column_board[column])):
                column_board[column][row] = squares[row][column]

        return column_board


    def make_move(self, move, player):
        self.cur_row = move[0]
        self.cur_col = move[1]
        self.squares[self.cur_row][self.cur_col] = player


    def minimax(self, node, player, depth):
        result = node.check_winner()
        if result != None:
            if  result == node.players['computer']:
                return ((node.row * node.col +1) - depth)

            if result == node.players['player']:
                return (-(node.row * node.col +1) + depth)

        if len(node.available_moves()) == 0:
            return 0

        if player == node.players['computer']:
            best = -(node.row * node.col +1) * 100
        else:
            best = (node.row * node.col +1) * 100

        for move in node.available_moves():
            node.make_move(move, Connect4.get_enemy(player))
            val = self.minimax(node, Connect4.get_enemy(player), depth+1)
            node.make_move(move, '*')

            if player == node.players['player']:
                if val > best:
                    best = val
            else:
                if val < best:
                    best = val

        return best


    def alphabeta(self, node, player, depth, alpha, beta):
        result = node.check_winner()
        if result != None:
            if  result == node.players['computer']:
                return ((node.row * node.col +1) - depth)

            if result == node.players['player']:
                return (-(node.row * node.col +1) + depth)

        if len(node.available_moves()) == 0:
            return 0

        # if player == node.players['computer']:
        #     best = -(node.row * node.col +1) * 100
        # else:
        #     best = (node.row * node.col +1) * 100

        for move in node.available_moves():
            node.make_move(move, Connect4.get_enemy(player))
            val = self.alphabeta(node, Connect4.get_enemy(player), depth+1, alpha, beta)
            node.make_move(move, '*')

            if player == node.players['player']:
                # if val > best:
                #     best = val

                if val > alpha:
                    alpha = val
                if alpha >= beta:
                    return beta
            else:
                # if val < best:
                #     best = val

                if val < beta:
                    beta = val
                if beta <= alpha:
                    return alpha

        if player == node.players['player']:
            return alpha
        else:
            return beta


    @staticmethod
    def minimax(node, player, depth):
        result = node.check_winner()
        if result is not None:
            if  result == node.players['computer']:
                return ((node.row * node.col +1) - depth)

            if result == node.players['player']:
                return (-(node.row * node.col +1) + depth)

        if len(node.available_moves()) == 0:
            return 0


        if player == node.players['player']:
            best = -(node.row * node.col +1) * 100
            for move in node.available_moves():
                node.make_move(move, Connect4.get_enemy(player))
                moveVal = Connect4.minimax(node, Connect4.get_enemy(player), depth+1)
                best = max(best, moveVal)
                node.make_move(move, '*')
            return best
        else:
            best = (node.row * node.col +1) * 100
            for move in node.available_moves():
                node.make_move(move, Connect4.get_enemy(player))
                moveVal = Connect4.minimax(node, Connect4.get_enemy(player), depth+1)
                best = min(best, moveVal)
                node.make_move(move, '*')
            return best

    @staticmethod
    def alphabeta(node, player, depth, alpha, beta):
        result = node.check_winner()
        if result is not None:
            if result == node.players['computer']:
                return ((node.row * node.col + 1) - depth)

            if result == node.players['player']:
                return (-(node.row * node.col + 1) + depth)

        if len(node.available_moves()) == 0:
            return 0

        if player == node.players['player']:
            best = -(node.row * node.col + 1) * 100
            for move in node.available_moves():
                node.make_move(move, Connect4.get_enemy(player))
                moveVal = Connect4.alphabeta(node, Connect4.get_enemy(player), depth + 1, alpha, beta)
                best = max(best, moveVal)
                node.make_move(move, '*')
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = (node.row * node.col + 1) * 100
            for move in node.available_moves():
                node.make_move(move, Connect4.get_enemy(player))
                moveVal = Connect4.alphabeta(node, Connect4.get_enemy(player), depth + 1, alpha, beta)
                best = min(best, moveVal)
                node.make_move(move, '*')
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best


    @staticmethod
    def get_enemy(player):
        if player == 'x':
            return '0'
        return 'x'


    @staticmethod
    def determine(board, player):
        alpha = 9999999999
        beta = -9999999999
        bestVal = -(board.row * board.col +1) * 100
        choices = []
        if len(board.available_moves()) == board.row * board.col:
            return [board.row/2, board.col/2]
        for move in board.available_moves():
            board.make_move(move, player)
            moveVal = board.alphabeta(board, player, 0, alpha, beta)
            # moveVal = board.minimax(board, player, 0)
            print moveVal, move
            board.make_move(move, '*')
            if moveVal > bestVal:
                bestVal = moveVal
                choices = [move]
            elif moveVal == bestVal:
                choices.append(move)

        print choices

        return random.choice(choices)


    @staticmethod
    def findBestMovce(board, player):
        alpha = 9999999999
        beta = -9999999999
        bestVal = -(board.row * board.col +1) * 100
        choices = []
        if len(board.available_moves()) == board.row * board.col:
            return [board.row/2, board.col/2]
        for move in board.available_moves():
            board.make_move(move, player)
            # moveVal = Connect4.minimax(board, player, 0)
            moveVal = Connect4.alphabeta(board, player, 0, alpha, beta)
            print moveVal, move
            board.make_move(move, '*')
            if(moveVal > bestVal):
                bestVal = moveVal
                choices = [move]
            elif moveVal == bestVal:
                choices.append(move)

        print choices
        return random.choice(choices)


if __name__ == "__main__":
    row = 0
    col = 0

    board = Connect4(3, 3, 3)
    board.display_board(board.squares)
    print "-" * 100

    board.choosePlayer('0')
    computer_move = True
    player = board.players['player']

    while True:
        if computer_move:
            player = board.players['computer']
            row, col = Connect4.determine(board, player)
            # row, col = Connect4.findBestMovce(board, player)
            board.make_move([row,col], board.players['computer'])
            computer_move = False
        else:
            move = raw_input("Please, enter coordinates for player %s separated by space: " % player)
            if move == "q":
                sys.exit()

            coords = move.split(' ')
            row = int(coords[0])
            col = int(coords[1])
            board.make_move([row, col], board.players['player'])
            computer_move = True

        board.display_board(board.squares)
        print "-" * 100
        winer = board.check_winner()
        if winer is not None:
            print "Player %s is winner!" % winer
            sys.exit()
        else:
            if len(board.available_moves()) == 0:
                print "Draw!"
                sys.exit()

        # switch players
        player = Connect4.get_enemy(player)