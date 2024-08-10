import sys, pygame
import random
import copy, math
import os


WIDTH = 8*70
HEIGHT = 8*70

# Board dimensions
COLS = 8
ROWS = 8
SQSIZE = WIDTH // COLS


class Theme:


    def __init__(self, light_bg, dark_bg, 
                       light_trace, dark_trace, 
                       light_moves, dark_moves):
                       
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)


class Square:

    ALPHACOLS = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h' }

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacol = self.ALPHACOLS[col]

    def __str__(self):
        return '(' + str(self.row) + ', ' + str(self.col) + ')'

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def has_piece(self):
        return self.piece != None

    def has_team_piece(self, color):
        return self.piece != None and self.piece.color == color

    def has_rival_piece(self, color):
        return self.piece != None and self.piece.color != color
    
    def isempty(self):
        return self.piece == None

    def isempty_or_rival(self, color):
        return self.piece == None or self.piece.color != color

    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7: return False
        return True
    
    @staticmethod
    def get_alphacol(col):
        alphacols = { 0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h' }
        return alphacols[col]

class Sound:

    
    def __init__(self, path):
        self.path = path
        self.sound = pygame.mixer.Sound(path)
        
    def play(self):
        pygame.mixer.Sound.play(self.sound)

class Piece:

    def __init__(self, name, color, value, texture_rect=None):
        value_sign = 1 if color == 'white' else -1
        self.name = name
        self.color = color
        self.value = value * value_sign
        self.moved = False
        self.moves = []
        self.set_texture()
        self.texture_rect = texture_rect

    def __str__(self):
        return self.color[0] + self.name[0].upper() + self.name[1].upper()

    # -------------
    # CLASS METHODS
    # -------------

    def add_move(self, move):
        self.moves.append(move)

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png')


class Pawn(Piece):

    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1
        super().__init__('pawn', color, 1.0)

class Knight(Piece):


    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):


    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):


    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):


    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):


    def __init__(self, color):
        super().__init__('king', color, 10000.0)



class Color:
    
    def __init__(self, light, dark):
        self.light = light
        self.dark = dark


class Book:
    
    def __init__(self):
        self.head = Node()
        self._create()

    def next_move(self, game_moves, weighted=True):
        for i, move in enumerate(game_moves):
            if i == 0: node = self.head

            for child in node.children:
                if move == child.value:
                    if len(game_moves)-1 == i:
                        move = child.choose_child(weighted) # weighted (from popular moves)
                        return move
                    else:
                        node = child

    def _create(self):

        self.head.add_children(
            Node(Move(Square(6, 4), Square(4, 4)), 1365473), # e4
            Node(Move(Square(6, 3), Square(4, 3)), 1050119), # d4
            Node(Move(Square(7, 6), Square(5, 5)), 299548), # right knight
            Node(Move(Square(6, 2), Square(4, 2)), 211850), # c4
        )
        
        # -------
        # ROUND 2
        # -------

        # e4 - 4 logs
        self.head.children[0].add_children(
            Node(Move(Square(1, 2), Square(3, 2)), 607220),
            Node(Move(Square(1, 4), Square(3, 4)), 296972),
            Node(Move(Square(1, 4), Square(2, 4)), 175686),
            Node(Move(Square(1, 2), Square(2, 2)), 106332),
        )

        #  d4 - 3 logs
        self.head.children[1].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 624094),
            Node(Move(Square(1, 3), Square(3, 3)), 264257),
            Node(Move(Square(1, 4), Square(2, 4)), 47288),
        )

        # right knight - 2 logs
        self.head.children[2].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 139857),
            Node(Move(Square(1, 3), Square(3, 3)), 79598),
        )

        # c4 - 3 logs
        self.head.children[3].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 64235),
            Node(Move(Square(1, 4), Square(3, 4)), 45546),
        )

        # -------
        # ROUND 3
        # -------

        # 3.1.1
        self.head.children[0].children[0].add_children(
            Node(Move(Square(7, 6), Square(5, 5)), 483773),
            Node(Move(Square(7, 1), Square(5, 2)), 55647),
        )

        # 3.1.2
        self.head.children[0].children[1].add_children(
            Node(Move(Square(7, 6), Square(5, 5)), 262867),
        )

        # 3.1.3
        self.head.children[0].children[2].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 156673)
        )

        # 3.1.4
        self.head.children[0].children[3].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 83980)
        )

        # -----------------------------------------------------

        # 3.2.1
        self.head.children[1].children[0].add_children(
            Node(Move(Square(6, 2), Square(4, 2)), 430542),
            Node(Move(Square(7, 6), Square(5, 5)), 160061),
        )

        # 3.2.2
        self.head.children[1].children[1].add_children(
            Node(Move(Square(6, 2), Square(4, 2)), 191778),
            Node(Move(Square(7, 6), Square(5, 5)), 78389),
        )

        # 3.2.3
        self.head.children[1].children[2].add_children(
            Node(Move(Square(6, 4), Square(4, 4)), 155950)
        )

        # -----------------------------------------------------

        # 3.3.1
        self.head.children[2].children[0].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 158564),
            Node(Move(Square(6, 2), Square(4, 2)), 89892),
        )

        # 3.3.2
        self.head.children[2].children[1].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 77741),
            Node(Move(Square(6, 6), Square(5, 6)), 32694),
        )

        # -----------------------------------------------------

        # 3.4.1
        self.head.children[3].children[0].add_children(
            Node(Move(Square(6, 3), Square(4, 3)), 417701),
            Node(Move(Square(7, 6), Square(5, 5)), 88843),
        )

        # 3.4.2
        self.head.children[3].children[1].add_children(
            Node(Move(Square(7, 1), Square(5, 2)), 29415),
            Node(Move(Square(6, 6), Square(5, 6)), 15373),
        )

        # -------
        # ROUND 4
        # -------

        # 4.1.1.1
        self.head.children[0].children[0].children[0].add_children(
            Node(Move(Square(1, 3), Square(2, 3)), 196457),
            Node(Move(Square(0, 1), Square(2, 2)), 135043),
            Node(Move(Square(1, 4), Square(2, 4)), 127503),
        )

        # 4.1.1.2
        self.head.children[0].children[0].children[1].add_children(
            Node(Move(Square(0, 1), Square(2, 2)), 32756),
            Node(Move(Square(1, 4), Square(2, 4)), 8897),
        )

        # -----------------------------------------------------

        # 4.1.2.1
        self.head.children[0].children[1].children[0].add_children(
            Node(Move(Square(0, 1), Square(2, 2)), 226645),
        )

        # -----------------------------------------------------

        # 4.1.3.1
        self.head.children[0].children[2].children[0].add_children(
            Node(Move(Square(1, 3), Square(3, 3)), 153961),
        )

        # -----------------------------------------------------

        # 4.1.4.1
        self.head.children[0].children[3].children[0].add_children(
            Node(Move(Square(1, 3), Square(3, 3)), 80928),
        )

        # -----------------------------------------------------
        # -----------------------------------------------------

        # 4.2.1.1
        self.head.children[1].children[0].children[0].add_children(
            Node(Move(Square(1, 4), Square(2, 4)), 211046),
            Node(Move(Square(1, 6), Square(2, 6)), 154877),
            Node(Move(Square(1, 2), Square(3, 2)), 48947),
        )

        # 4.2.1.2
        self.head.children[1].children[0].children[1].add_children(
            Node(Move(Square(1, 3), Square(3, 3)), 70523),
            Node(Move(Square(1, 6), Square(2, 6)), 65729),
            Node(Move(Square(1, 4), Square(3, 4)), 58615),
        )

        # -----------------------------------------------------

        # 4.2.2.1
        self.head.children[1].children[1].children[0].add_children(
            Node(Move(Square(1, 2), Square(2, 2)), 92378),
            Node(Move(Square(1, 4), Square(2, 4)), 75340),
            Node(Move(Square(3, 3), Square(4, 2)), 23649), # !CAPTURE
        )

        # 4.2.2.2
        self.head.children[1].children[1].children[1].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 69781),
        )

        # ------------------------------------------------------

        # 4.2.3.1
        self.head.children[1].children[2].children[0].add_children(
            Node(Move(Square(1, 3), Square(3, 3)), 153961),
        )

        # -----------------------------------------------------
        # -----------------------------------------------------

        # 4.3.1.1
        self.head.children[2].children[0].children[0].add_children(
            Node(Move(Square(1, 3), Square(2, 3)), 196457),
            Node(Move(Square(0, 1), Square(2, 2)), 135043),
            Node(Move(Square(1, 4), Square(2, 4)), 127503),
        )

        # 4.3.1.2
        self.head.children[2].children[0].children[1].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 23080),
            Node(Move(Square(0, 1), Square(2, 2)), 13414),
            Node(Move(Square(1, 6), Square(2, 6)), 23080),
        )

        # ------------------------------------------------------
        # -----------------------------------------------------
        
        # 4.4.1.1
        self.head.children[3].children[0].children[0].add_children(
            Node(Move(Square(1, 4), Square(2, 4)), 211046),
            Node(Move(Square(1, 6), Square(2, 6)), 154877),
            Node(Move(Square(1, 2), Square(3, 2)), 48947),
        )

        # 4.4.1.2
        self.head.children[3].children[0].children[1].add_children(
            Node(Move(Square(1, 6), Square(2, 6)), 33861),
            Node(Move(Square(1, 4), Square(2, 4)), 32507),
            Node(Move(Square(1, 2), Square(3, 2)), 23128),
        )

        # -----------------------------------------------------
        
        # 4.4.2.1
        self.head.children[3].children[1].children[0].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 7508),
            Node(Move(Square(0, 1), Square(2, 2)), 4443),
            Node(Move(Square(1, 6), Square(2, 6)), 2706),
        )

        # 4.4.2.2
        self.head.children[3].children[1].children[1].add_children(
            Node(Move(Square(0, 6), Square(2, 5)), 7988),
            Node(Move(Square(0, 1), Square(2, 2)), 4463),
        )

        # -----------------------------------------------------
        # -----------------------------------------------------



class AI:

    def __init__(self, engine='book', depth=3):
        self.engine = engine
        self.depth = depth
        self.book = Book()
        self.color = 'black'
        self.game_moves = []
        self.explored = 0



    def book_move(self):
        move = self.book.next_move(self.game_moves, weighted=True)
        return move



    def heatmap(self, piece, row, col):
        hmp = 0
        if piece.name == 'pawn':
            if piece.color == 'black':
                hmp = [ 
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02],
                    [0.01, 0.01, 0.03, 0.06, 0.06, 0.03, 0.01, 0.01],
                    [0.02, 0.02, 0.04, 0.07, 0.07, 0.04, 0.02, 0.02],
                    [0.03, 0.03, 0.05, 0.08, 0.08, 0.05, 0.03, 0.03],
                    [0.07, 0.07, 0.08, 0.09, 0.09, 0.08, 0.07, 0.07],
                    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
                    [9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00],
            ]
            elif piece.color == 'white':
                hmp = [ 
                    [9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00, 9.00],
                    [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10],
                    [0.07, 0.07, 0.08, 0.09, 0.09, 0.08, 0.07, 0.07],
                    [0.03, 0.03, 0.05, 0.08, 0.08, 0.05, 0.03, 0.03],
                    [0.02, 0.02, 0.04, 0.07, 0.07, 0.04, 0.02, 0.02],
                    [0.01, 0.01, 0.03, 0.06, 0.06, 0.03, 0.01, 0.01],
                    [0.02, 0.01, 0.00, 0.00, 0.00, 0.00, 0.01, 0.02],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            ]

        elif piece.name == 'knight':
            hmp = [ 
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
                    [0.00, 0.02, 0.06, 0.05, 0.05, 0.06, 0.02, 0.00],
                    [0.00, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.00],
                    [0.00, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.00],
                    [0.00, 0.02, 0.06, 0.05, 0.05, 0.06, 0.02, 0.00],
                    [0.00, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            ]

        elif piece.name == 'bishop':
            hmp = [ 
                    [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02],
                    [0.01, 0.05, 0.03, 0.03, 0.03, 0.03, 0.05, 0.01],
                    [0.01, 0.03, 0.07, 0.05, 0.05, 0.07, 0.03, 0.01],
                    [0.01, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.01],
                    [0.01, 0.03, 0.05, 0.10, 0.10, 0.05, 0.03, 0.01],
                    [0.01, 0.03, 0.07, 0.05, 0.05, 0.07, 0.03, 0.01],
                    [0.01, 0.05, 0.03, 0.03, 0.03, 0.03, 0.05, 0.01],
                    [0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.02],
            ]
        
        elif piece.name == 'king':
            if piece.color == 'black':
                hmp = [ 
                    [0.05, 0.50, 0.10, 0.00, 0.00, 0.00, 0.10, 0.05],
                    [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                ]
            
            elif piece.color == 'white':
                hmp = [ 
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.02, 0.02, 0.00, 0.00, 0.00, 0.00, 0.02, 0.02],
                    [0.05, 0.50, 0.10, 0.00, 0.00, 0.00, 0.10, 0.05],
                ]

        else :
            hmp = [ 
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            ]

        eval = -hmp[row][col] if piece.color == 'black' else hmp[row][col]
        return eval

    def threats(self, board, piece):
        eval = 0
        for move in piece.moves:
            attacked = board.squares[move.final.row][move.final.col]
            if attacked.has_piece():
                if attacked.piece.color != piece.color:
                    # checks
                    if attacked.piece.name == 'king':
                        eval += attacked.piece.value / 10500
                    
                    # threat
                    else:
                        eval += attacked.piece.value / 45

        return eval

    def static_eval(self, board):
        # var
        eval = 0

        for row in range(ROWS):
            for col in range(COLS):
                if board.squares[row][col].has_piece():
                    # piece
                    piece =  board.squares[row][col].piece
                    # white - black
                    eval += piece.value
                    # heatmap
                    eval += self.heatmap(piece, row, col)
                    # moves
                    if piece.name != 'queen': eval += 0.01 * len(piece.moves)
                    else: eval += 0.003 * len(piece.moves)
                    # checks
                    eval += self.threats(board, piece)
        
        eval = round(eval, 5)
        return eval

    def get_moves(self, board, color):
        moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_team_piece(color):
                    board.calc_moves(square.piece, square.row, square.col)
                    moves += square.piece.moves
        
        return moves

    def minimax(self, board, depth, maximizing, alpha, beta):
        if depth == 0:
            return self.static_eval(board), None # eval, move
        
        # white
        if maximizing:
            max_eval = -math.inf
            moves = self.get_moves(board, 'white')
            for move in moves:
                self.explored += 1
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth-1, False, alpha, beta)[0] # eval, mov
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, max_eval)
                if beta <= alpha: break

            if not best_move:
                best_move = moves[0]

            return max_eval, best_move # eval, move
        
        # black
        elif not maximizing:
            min_eval = math.inf
            moves = self.get_moves(board, 'black')
            for move in moves:
                self.explored += 1
                piece = board.squares[move.initial.row][move.initial.col].piece
                temp_board = copy.deepcopy(board)
                temp_board.move(piece, move)
                piece.moved = False
                eval = self.minimax(temp_board, depth-1, True, alpha, beta)[0] # eval, move
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, min_eval)
                if beta <= alpha: break
            
            if not best_move:
                idx = random.randrange(0, len(moves))
                best_move = moves[idx]

            return min_eval, best_move # eval, move



    def eval(self, main_board):
        self.explored = 0

        # add last move
        last_move = main_board.last_move
        self.game_moves.append(last_move)

        # book engine
        if self.engine == 'book':
            move = self.book_move()

            # no more book moves ?
            if move is None:
                self.engine = 'minimax'

        # minimax engine
        if self.engine == 'minimax':
            # printing
            print('\nFinding best move...')
                        
            # minimax initial call
            eval, move = self.minimax(main_board, self.depth, False, -math.inf, math.inf) # eval, move
            
            # printing
            print('\n- Initial eval:',self.static_eval(main_board))
            print('- Final eval:', eval)
            print('- Boards explored', self.explored)
            if eval >= 5000: print('* White MATE!')
            if eval <= -5000: print('* Black MATE!')
            
        # append
        self.game_moves.append(move)
        
        return move


class Node:

    def __init__(self, value=None, weight=0, prob=0):
        self.value = value
        self.weight = weight
        self.prob = prob
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
        self.calc_prob()

    def add_children(self, *nodes):
        for node in nodes:
            self.add_child(node)

    def calc_prob(self):
        weights = 0
        for child in self.children:
            weights += child.weight
        
        for child in self.children:
            child.prob = (child.weight / weights) * 100

    def get_child(self, idx):
        return self.children[idx]

    def choose_child(self, weighted=True):
        if not weighted: return self.children[0]
        
        rnd = random.randint(1, 100)

        c = 0
        for child in self.children:
            if rnd <= child.prob + c:
                return child.value
        
            c += child.prob

class Board:

    def __init__(self):
        self.squares = []
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move = None

    def __str__(self):
        s = '\n'
        for row in range(ROWS):
            s += '[ '
            for col in range(COLS):
                sqr = self.squares[row][col]
                s += '[ ]' if sqr.isempty() else str(sqr.piece)
                s += ' '
            s += ']\n'
        return s



    def move(self, piece, move):
        initial = move.initial
        final = move.final
        # console squares update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # castling ?
        if piece.name == 'king':
            row = 0 if piece.color == 'black' else 7 
            diff = initial.col - final.col
            if diff == 2:
                lRook = self.squares[row][0].piece
                if isinstance(lRook, Rook):
                    # erase king prev moves
                    piece.moved = True
                    piece.moves = []
                    # move left rook
                    piece2 = self.squares[row][0].piece
                    initial = Square(row, 0)
                    final = Square(row, 3)
                    move2 = Move(initial, final)
                    self.move(piece2, move2)
            elif diff == -2:
                # erase king prev moves
                piece.moved = True
                piece.moves = []
                # move right rook
                piece2 = self.squares[row][7].piece
                initial = Square(row, 7)
                final = Square(row, 5)
                move2 = Move(initial, final)
                self.move(piece2, move2)

        # promoting ?
        if piece.name == 'pawn':
            self.check_promotion(piece, final)

        piece.moved = True
        piece.moves = []

        self.last_move = move

    def check_promotion(self, piece, final):
        promote_row = 0 if piece.color == 'white' else 7

        if final.row == promote_row:
            # promote
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):

        def pawn():
            piece = self.squares[row][col].piece
            if piece.color == 'black':
                if row != 1: piece.moved = True
            if piece.color == 'white':
                if row != 6: piece.moved = True
            # steps
            steps = 1 if piece.moved else 2

            # vertical move
            start = row + piece.dir
            end = row + piece.dir * (1 + steps)
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, col, self.squares[move_row][col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: break
                else: break
            
            # diagonal
            move_cols = [col - 1, col + 1]
            move_row = row + piece.dir
            for move_col in move_cols:
                if Square.in_range(move_col):
                    if self.squares[move_row][move_col].has_rival_piece(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
        
        def knight():
            # possible moves
            possible_moves = [
            (row - 2, col + 1),
            (row - 1, col + 2),
            (row + 1, col + 2),
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row + 1, col - 2),
            (row - 1, col - 2),
            (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                move_row, move_col = possible_move
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline(incrs):
            for incr in incrs:
                row_inc, col_inc = incr
                move_row = row + row_inc
                move_col = col + col_inc
                while True:
                    if Square.in_range(move_row, move_col):
                        # move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        # empty
                        if self.squares[move_row][move_col].isempty():
                            # new move
                            piece.add_move(move)
                        # piece
                        else: 
                            if self.squares[move_row][move_col].has_rival_piece(piece.color):
                                # new move and stop
                                piece.add_move(move)
                            break
                    else: # not in range
                        break
                
                    # incr
                    move_row, move_col = move_row + row_inc, move_col + col_inc

        def king():
            adjs = [
                (row - 1, col + 0),
                (row - 1, col + 1),
                (row + 0, col + 1),
                (row + 1, col + 1),
                (row + 1, col + 0),
                (row + 1, col - 1),
                (row + 0, col - 1),
                (row - 1, col - 1),
            ]

            # normal moves
            for adj in adjs:
                move_row, move_col = adj
                
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].isempty_or_rival(piece.color):
                        # new move
                        initial = Square(row, col)
                        final = Square(move_row, move_col, self.squares[move_row][move_col].piece)
                        move = Move(initial, final)
                        piece.add_move(move)
                
            # castling
            if not piece.moved:
                # queenside castling
                lRook = self.squares[row][0].piece
                if isinstance(lRook, Rook):
                    if not lRook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece(): break
                            if c == 3:
                                # new move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)

                # kingside castling
                rRook = self.squares[row][7].piece
                if isinstance(rRook, Rook):
                    if not rRook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece(): break
                            if c == 6:
                                # new move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)

        if piece.name == 'pawn': 
            pawn()

        elif piece.name == 'knight': 
            knight()

        elif piece.name == 'bishop': 
            straightline([(-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif piece.name == 'rook': 
            straightline([(-1, 0), (0, 1), (1, 0), (0, -1)])

        elif piece.name == 'queen': 
            straightline([(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (-1, -1), (1, -1), (1, 1)])

        elif piece.name == 'king': 
            king()
                        


    def _create(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # KNIGHTS
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # BISHOPS
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # ROOKS
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # QUEEN
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # KING
        self.squares[row_other][4] = Square(row_other, 4, King(color))

class Config:

    def __init__(self):
        self._add_themes()
        self.idx = 0
        self.theme = self.themes[self.idx]
        self.font = pygame.font.SysFont('monospace', 18, bold=True)
        self.move_sound = Sound(os.path.join('assets/sounds/move.wav'))
        self.capture_sound = Sound(os.path.join('assets/sounds/capture.wav'))

    def change_theme(self):
        self.idx += 1
        self.idx %= len(self.themes)
        self.theme = self.themes[self.idx]


    
    def _add_themes(self):

        green = Theme((234, 235, 200), (119, 154, 88), (244, 247, 116), (172, 195, 51), '#C86464', '#C84646')
        brown = Theme((235, 209, 166), (165, 117, 80), (245, 234, 100), (209, 185, 59), '#C86464', '#C84646')
        blue = Theme((229, 228, 200), (60, 95, 135), (123, 187, 227), (43, 119, 191), '#C86464', '#C84646')
        gray = Theme((120, 119, 118), (86, 85, 84), (99, 126, 143), (82, 108, 128), '#C86464', '#C84646')

        self.themes = [
            green,
            brown,
            blue,
            gray,
        ]


class Dragger:
    '''
        Responsable of dragging the pieces through screen
    '''

    def __init__(self):
        self.dragging = False
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
    




    def update_blit(self, surface):
        # texture
        self.piece.set_texture(size=128)
        texture = self.piece.texture
        # image
        img = pygame.image.load(texture)
        # rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        # blit
        surface.blit(img, self.piece.texture_rect)



    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False

class Move:


    def __init__(self, initial, final):
        self.initial = initial # Square
        self.final = final # Square

    def __str__(self):
        return str(self.initial) + ', ' + str(self.final)

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final


class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.config = Config()
        self.dragger = Dragger()
        self.next_player = 'white'
        self.gamemode = 'ai'
        self.selected_piece = None
        self.hovered_square = None



    def show_bg(self, surface):
        theme = self.config.theme

        for row in range(ROWS):
            for col in range(COLS):
                # tiles
                # color
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                # rect
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                # draw
                pygame.draw.rect(surface, color, rect)

                # row coordinates
                if col == 0:
                    # color
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    # coordinates
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    surface.blit(lbl, (5, 5 + row * SQSIZE))
                
                # col coordinates
                if row == 7:
                    # coordinates
                    # color
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    # coordinates
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    surface.blit(lbl, (col * SQSIZE + SQSIZE - 20, HEIGHT - 20))
        
        if self.board.last_move:
            self.show_last_move(surface)

        if self.selected_piece:
            self.show_moves(surface)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # for dragger
                    if piece is not self.selected_piece:
                        piece.set_texture()
                        texture = piece.texture
                        img = pygame.image.load(texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        if self.selected_piece:
            theme = self.config.theme

            for move in self.selected_piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                # rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                # draw
                pygame.draw.rect(surface, color, rect)

    def show_last_move(self, surface):
        if self.board.last_move:
            theme = self.config.theme

            iniGtial = self.board.last_move.initial
            final = self.board.last_move.final

            # color
            for pos in [initial, final]:
                # color
                color = theme.trace.light if (pos.col + pos.row) % 2 == 0 else theme.trace.dark
                # rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # draw
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        if self.hovered_square:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
            # draw
            pygame.draw.rect(surface, color, rect, 3)



    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured):
        if captured: self.config.capture_sound.play()
        else: self.config.move_sound.play()

    def next_turn(self):
        self.next_player = 'black' if self.next_player == 'white' else 'white'

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def set_hover(self, row, col):
        self.hovered_square = self.board.squares[row][col]

    def select_piece(self, piece):
        self.selected_piece = piece
    
    def unselect_piece(self):
        self.selected_piece = None

    def reset(self):
        self.__init__()

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
        pygame.display.set_caption('Chess')
        self.game = Game()

    def mainloop(self):

        screen = self.screen
        game = self.game
        board = self.game.board
        ai = self.game.ai
        dragger = self.game.dragger

        while True:
            
            if not game.selected_piece:
                game.show_bg(screen)
                game.show_pieces(screen)

            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                
                # mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    pos = event.pos
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # valid piece ?
                        if piece.color == game.next_player:
                            game.select_piece(piece)
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.drag_piece(piece)
                            dragger.save_initial(pos)
                            # show
                            game.show_bg(screen)
                            game.show_pieces(screen)

                # mouse release
                elif event.type == pygame.MOUSEBUTTONUP:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # released pos
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE

                        # new move object
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        # valid move -> move ?
                        if board.valid_move(dragger.piece, move):
                            # capture
                            captured = board.squares[released_row][released_col].has_piece()
                            # move
                            board.move(dragger.piece, move)
                            game.sound_effect(captured)
                            # draw
                            game.show_bg(screen)
                            game.show_pieces(screen)
                            # next -> AI
                            game.next_turn()
                            
                            # --------------
                            # >>>>> AI >>>>>
                            # --------------

                            if game.gamemode == 'ai':
                                # update
                                game.unselect_piece()
                                game.show_pieces(screen)
                                pygame.display.update()
                                # optimal move
                                move = ai.eval(board)
                                initial = move.initial
                                final = move.final
                                # piece
                                piece = board.squares[initial.row][initial.col].piece
                                # capture
                                captured = board.squares[final.row][final.col].has_piece()
                                # move
                                board.move(piece, move)
                                game.sound_effect(captured)
                                # draw
                                game.show_bg(screen)
                                game.show_pieces(screen)
                                # next -> AI
                                game.next_turn()
                    
                    game.unselect_piece()
                    dragger.undrag_piece()

                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    pos = event.pos
                    motion_row = pos[1] // SQSIZE
                    motion_col = pos[0] // SQSIZE

                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show
                        game.show_bg(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # key press
                elif event.type == pygame.KEYDOWN:
                    
                    # gamemode
                    if event.key == pygame.K_a:
                        game.change_gamemode()
                    
                    # depth
                    if event.key == pygame.K_3:
                        ai.depth = 3

                    if event.key == pygame.K_4:
                        ai.depth = 4
                        
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    
if __name__ == '__main__':
    m = Main()
    m.mainloop()