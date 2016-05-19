from pieces import *
from square import *
from player import *
from board import *
from window import *


class Game():
    def __init__(self, board):
        self.board = board
        self.players = board.players
        self.current_player = self.players[0]
        self.pause_player = self.players[1]
        self.play = False
        self.last_move = []         # (source, destination, capture) / 3 x square

        self.en_passant = False
        self.valid_moves = []

        pass

    def end_game(self):
        pass

    def start_game(self):
        # clear player state
        for player in self.board.players:
            player.clear()

        self.en_passant = False
        self.valid_moves = []
        self.last_move = []

        self.current_player = self.players[0]
        self.pause_player = self.players[1]

        self.current_player.status = PLAYER_STATUS[1]   # 'moving'
        self.pause_player.status = PLAYER_STATUS[0]     # 'waiting'

        # clear pieces on board
        for square in self.board.squares:
            square.piece = None
        # deploy pieces in start position
        self.board.deploy_pieces_in_start_position(self.board.players)

        self.board.last_move = []

        self.play = True


    def get_valid_moves(self, piece):
        '''
        Return valid moves for current piece as list of tuples (destination_square, capture_square)
        :param piece:   piece object that valid moves are calculated
        :return:        list [(destination_square, capture_square), (destination_square, capture_square), ..]
        '''
        if self.valid_moves:
            return self.valid_moves
        else:
            self.set_valid_moves(piece)
            return self.valid_moves

    def is_check(self):
        pass

    def is_mate(self):
        pass

    def is_pawn_promotion(self):
        pass

    def is_valid_move(self, piece, destination):
        for move_data in self.valid_moves:
            valid_destination_square, valid_capture_square = move_data
            if destination == valid_destination_square:
                source_square = self.board.get_square(piece.field)
                if valid_capture_square:
                    valid_capture_piece = valid_capture_square.piece
                else:
                    valid_capture_piece = None
                return (source_square, valid_destination_square, valid_capture_piece)
        return (False, False, False)

    def move(self, piece, source, destination, capture_piece):

        # release capture & move on board
        if capture_piece:
            print('Game/move/capture:', capture_piece.name_long, capture_piece.color, capture_piece.field)
            taken_piece = self.board.take_piece(capture_piece)
            self.current_player.add_captured( taken_piece )
        self.board.move(piece, destination)

        # update some game state after move
        if capture_piece:
            self.last_move = [source, destination, capture_piece]
        else:
            self.last_move = [source, destination, None]
        self.en_passant = False
        self.valid_moves = []

        # set remember en passant for next move
        if isinstance(piece, Pion):
            if int(abs(source.row - destination.row)) == 2:
                self.en_passant = True

    def select(self, player, square):
        print('Game/select: ', 'player',player.name,'square',square.name)
        if self.play:
            if player == self.current_player:

                if player.is_touching():
                    # if player select second square (destination)
                    piece = player.get_touch()
                    source = self.board.get_square(piece.field)
                    destination = square

                    # if player select the same field that touched before
                    if source == destination:
                        self.set_untouching()
                        return None

                    #validate move
                    source, valid_destination, valid_capture_piece = self.is_valid_move(piece, destination)
                    if valid_destination == destination:
                        pass
                    else:
                        return None         # can't move on that field

                    # move
                    self.move(piece, source, valid_destination, valid_capture_piece)
                    # other settings
                    self.set_untouching()
                    # turn players
                    self.turn_players()

                else:
                    # if player select first square (source)
                    source = square
                    piece = source.piece
                    if piece:
                        if player.set_touch(piece):
                            # TODO check this down below:
                            piece.set_current_moves(self.get_valid_moves(piece))

    def set_untouching(self):
        self.current_player.set_untouching()
        self.valid_moves = []

    def set_valid_moves(self, piece):
        '''
        Set lists of all valid move and capture field offsets of squares in Board,
        :param piece:   piece object that valid moves are calculated
        :return:        -
        '''

        self.valid_moves = []
        source = self.board.get_square(piece.field)
        color = source.piece.color

        if isinstance(piece, Pion):
            move_vectors, capture_vectors = piece.getMoveVectors()

            # pawn move
            for direction in move_vectors:
                for colvec, rowvec in move_vectors[direction]:
                    target_col = source.col + colvec
                    target_row = source.row + rowvec
                    square_offset = target_row * 8 + target_col   # offset in list of board squares

                    if self.board.is_in_board(target_col, target_row):

                        destination = self.board.squares[square_offset]
                        if destination.piece:                       # any piece, no move
                            break
                        else:                                       # empty field
                            self.valid_moves.append((destination, False))

            # pawn capture
            for direction in capture_vectors:
                for colvec, rowvec in capture_vectors[direction]:
                    target_col = source.col + colvec
                    target_row = source.row + rowvec

                    if self.board.is_in_board(target_col, target_row):

                        square_offset = target_row * 8 + target_col   # offset in list of board squares
                        destination = self.board.squares[square_offset]
                        if destination.piece:
                            if destination.piece.color == color:    # self piece, no capture
                                break
                            else:                                   # opponent's piece, capture
                                capture = destination
                                self.valid_moves.append((destination, capture))
                                break
                        else:
                            if self.en_passant:
                                previous_destination = self.last_move[1]
                                previous_move_col = previous_destination.col
                                if previous_move_col == destination.col:
                                    if previous_destination.row == source.row:        # can realise en passant
                                        capture = previous_destination
                                        self.valid_moves.append((destination, capture))

        else:
            # other pieces
            vectors = piece.getMoveVectors()
            for direction in vectors:
                for colvec, rowvec in vectors[direction]:
                    target_col = source.col + colvec
                    target_row = source.row + rowvec

                    if self.board.is_in_board(target_col, target_row):

                        square_offset = target_row * 8 + target_col   # offset in list of board squares
                        destination = self.board.squares[square_offset]
                        if destination.piece:
                            if destination.piece.color == color:    # self piece
                                break
                            else:                                   # opponent's piece
                                capture = destination
                                self.valid_moves.append((destination, capture))
                                break
                        else:                                           # empty field
                            self.valid_moves.append((destination, False))

    def turn_players(self):
        # turn players
        temp = self.current_player
        self.current_player = self.pause_player
        self.pause_player = temp
        self.current_player.status = PLAYER_STATUS[1]
        self.pause_player.status = PLAYER_STATUS[0]


# ----------------------------------------- main ------------------------------------------

def get_players():
    return Player('Kowalski', PIECES_COLORS[0], 'N'), Player('Nowak', PIECES_COLORS[1], 'S')  # return tuple (player, player)


def test():
    pass


def game():

    players = get_players()

    board = Board(players)
    board.deploy_pieces_in_start_position(players)
    board.show()

    game = Game(board)
    window = Window(game)


def main():
    game()
    test()
    pass

if __name__ == "__main__":
    main()