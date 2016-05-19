# defined chess board with all squares
from pieces import *
from square import *
from player import *


# square a1 is in left lower corner
SQUARES = 64
VERTICAL = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']     # files
HORIZONTAL = ['1', '2', '3', '4', '5', '6', '7', '8']   # ranks
BOARD_COLORS = ['dark goldenrod', 'light goldenrod']    # tkinter colors
PIECES_COLORS = ['white', 'black']
FRONT_ROW = [Pion, Pion, Pion, Pion, Pion, Pion, Pion, Pion]
BACK_ROW = [Wieża, Skoczek, Goniec, Hetman, Król, Goniec, Skoczek, Wieża]
INIT_DEPLOYMENT = [(HORIZONTAL[-1], VERTICAL, PIECES_COLORS[1], BACK_ROW),  # rank 8, row 7
                   (HORIZONTAL[-2], VERTICAL, PIECES_COLORS[1], FRONT_ROW), # rank 7, row 6
                   (HORIZONTAL[1], VERTICAL, PIECES_COLORS[0], FRONT_ROW),  # rank 2, row 1
                   (HORIZONTAL[0], VERTICAL, PIECES_COLORS[0], BACK_ROW),]  # rank 1, row 0

def get_list_pieces_in_row(row, color):
    lista = []
    if color == 'white':
        horiz_pos = '2'
    if color == 'black':
        horiz_pos = '7'
    #
    if row == 'front':
        pieces_list = FRONT_ROW
    if row == 'back':
        pieces_list = BACK_ROW
    #
    for vert_pos, piece in zip(VERTICAL, pieces_list):
        pos = vert_pos + horiz_pos  # pos: string
        lista.append(piece(pos))
    return lista


class Board:
    '''
    (columns: 0..7)
    a8 b8 c8 d8 e8 f8 g8 h8 	(row 7)
    a7 b7 c7 d7 e7 f7 g7 h7 	(row 6)
    a6 b6 c6 d6 e6 f6 g6 h6 	(row 5)
    a5 b5 c5 d5 e5 f5 g5 h5 	(row 4)
    a4 b4 c4 d4 e4 f4 g4 h4 	(row 3)
    a3 b3 c3 d3 e3 f3 g3 h3 	(row 2)
    a2 b2 c2 d2 e2 f2 g2 h2 	(row 1)
    a1 b1 c1 d1 e1 f1 g1 h1 	(row 0)
    '''

    def __init__(self, players):
        self.squares = []   # will fill below by square objects
        self.players = players
        self._name_offset_dict = {}     # squares dictionary

        # build all squares on board
        print('board, create board squares')
        for offset in range(SQUARES):
            col = offset % 8
            row = offset // 8
            file = VERTICAL[col]
            rank = HORIZONTAL[row]
            name = file + rank  # name: string 'a1'..
            color_index = (row+col) % 2
            self.squares.append(Square(offset, col, row, name, BOARD_COLORS[color_index]))

        # build {square name : offset} dictionary
        for square in self.squares:
            self._name_offset_dict[square.name] = square.offset

    def add(self, piece, field):
        square = self.get_square(field)
        if square:
            square.piece = piece
            square.piece.update_field(field) # update_field !!
            return True
        return False

    def deploy_pieces_in_start_position(self, players, INIT_DEPLOYMENT=INIT_DEPLOYMENT):
        for el in INIT_DEPLOYMENT:
            rank, columns, color, pieces_in_row = el
            for column, Piece in zip(columns, pieces_in_row): # 'Piece' from list of all pieces types
                field = str(column) + rank
                # add to players
                for player in players:
                    if color == player.color_pieces:
                        new_piece = Piece(player, field)
                        # add to player
                        player.add(new_piece)
                        # add on board
                        self.add(new_piece, field)

    def get_row(self, row):
        '''
        :param row: row number (integer: 0..len(HORIZONTAL)-1)
        :return:    list of square objects in one specified row
        '''
        begin = (len(VERTICAL) * (row))
        end = (len(VERTICAL) * (row + 1))
        _row = self.squares[begin:end]     # row is a list slice
        return _row

    def get_square(self, field):
        '''
        :param name: square position in format 'a1'
        :return:     square object at position 'name'
        '''
        return self.squares[self._name_offset_dict[field]]

    def give_piece(self, piece, destination):
        print('Board/give_piece:', piece.name_long, piece.field, destination.name)
        destination.piece = piece

    def move(self, piece, destination):
        print('Board/move:', piece.name_long, piece.field, destination.name)
        piece_ = self.take_piece(piece)
        self.give_piece(piece_, destination)
        destination.piece.update_field(destination.name)           # update board field in piece

    def is_empty(self, field):
        square = self.get_square(field)
        if square.piece:
            return False
        else:
            return True

    def is_in_board(self, col, row):
        if col < 0 or col > 7:        # is field beyond board ?
            return False
        if row < 0 or row > 7:
            return False
        return True

    def remove(self, piece):
        square = self.get_square(piece.field)
        removed = square.piece
        square.piece = None
        return removed

    def show(self):
        for n in reversed(range(len(HORIZONTAL))):
            for square in self.get_row(n):
                if not square.piece:
                    print(square.color[0:5].center(5), end=' ')
                else:
                    print(square.piece.name_short.center(5), end=' ')
            print()

    def take_piece(self, piece):
        temp = piece
        self.get_square(piece.field).piece = None
        return temp

# ------------------------------------------ main --------------------------------------


def test():
    pass


def main():
    test()
    pass

if __name__ == "__main__":
    main()