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
        self.valid_moves = {}       # dictionary {piece : [list of valid moves], .. }

        self.check_flag = None
        self.mate_flag = False

        pass

    def add_valid_moves(self, piece):
        '''
        Set lists of all valid move and capture field offsets of squares in Board,
        :param piece:   piece object that valid moves are calculated
        :return:        -
        '''

        # del: self.valid_moves = {}

        vm = [] # list of valid moves
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

                    if self.board.is_valid(target_col, target_row):

                        destination = self.board.squares[square_offset]
                        if destination.piece:                       # any piece, no move
                            break
                        else:                                       # empty field
                            vm.append((destination, False))

            # pawn capture
            for direction in capture_vectors:
                for colvec, rowvec in capture_vectors[direction]:
                    target_col = source.col + colvec
                    target_row = source.row + rowvec

                    if self.board.is_valid(target_col, target_row):

                        square_offset = target_row * 8 + target_col   # offset in list of board squares
                        destination = self.board.squares[square_offset]
                        if destination.piece:
                            if destination.piece.color == color:    # self piece, no capture
                                break
                            else:                                   # opponent's piece, capture
                                capture = destination
                                vm.append((destination, capture))
                                break
                        else:
                            if self.en_passant:
                                previous_destination = self.last_move[1]
                                previous_move_col = previous_destination.col
                                if previous_move_col == destination.col:
                                    if previous_destination.row == source.row:        # can realise en passant
                                        capture = previous_destination
                                        vm.append((destination, capture))
        else:
            # other pieces
            vectors = piece.getMoveVectors()
            for direction in vectors:
                for colvec, rowvec in vectors[direction]:
                    target_col = source.col + colvec
                    target_row = source.row + rowvec

                    if self.board.is_valid(target_col, target_row):

                        square_offset = target_row * 8 + target_col   # offset in list of board squares
                        destination = self.board.squares[square_offset]
                        if destination.piece:
                            if destination.piece.color == color:    # self piece
                                break
                            else:                                   # opponent's piece
                                capture = destination
                                vm.append((destination, capture))
                                break
                        else:                                           # empty field
                            vm.append((destination, False))

        self.valid_moves[piece] = vm

    def clear_check(self, player):
        self.check_flag = False
        player.check_flag = False
        player.status_check_mate = '-'


    def end_game(self):
        if self.check_flag:
            # check end game

            pass
        else:
            # player end game

            pass

    def start_game(self):
        # clear player state
        for player in self.board.players:
            player.clear()

        self.en_passant = False
        self.valid_moves = {}
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
        if piece in self.valid_moves:
            return self.valid_moves[piece]
        else:
            self.add_valid_moves(piece)
            return self.valid_moves[piece]

    def is_check(self, king, square = None):
        print ('-------------------------------------------')
        print('1 king: ', king.field)
        king_square = self.board.get_square(king.field)

        check = False

        for e in king.get_check_vectors():
            print ('-------------------------------------------')
            #print('1', e)
            classes, dictionary = e
            #print('2', classes)
            #print('3', dictionary)
            for direction, vectors in dictionary.items():
                print('4', direction)
                #print('5', vectors)
                for v in vectors:
                    #print('6', v)
                    board_square = self.board.get_square_cr(king_square.col + v[0], king_square.row + v[1])
                    if board_square:
                        print('7', 'test board_square', board_square.name)
                        piece = board_square.piece
                        if piece:
                            print('8', 'test_piece', piece.name_long, piece.field)
                            if piece.color == king.color:
                                print('the same color')
                                if isinstance(piece, Król):     # self King (for test when next move square != king square)
                                    continue
                                else:                           # self piece
                                    break
                            else:                       # opponents piece
                                for class_piece in classes:
                                    # test
                                    #print('Game/is_check:', class_piece,'\nin', classes, '\nis_i:',isinstance(piece, class_piece))

                                    if isinstance(piece, class_piece):
                                        return True
                                break
                    else:
                        break



        # pieces = last_move_player.pieces_own    # list pieces active on board
        # king_square = self.board.get_square(king_owner.king)                  # King square object
        #
        # for piece in pieces:
        #     for k,v in self.get_valid_moves(piece):
        #         for record in v:
        #             destination, capture = record
        #             if capture:
        #                 if king_square == capture:
        #                     return True
        # return False

    def is_mate(self, last_move_player, king_owner):

        moves = [[-1,1], [0,1], [1,1], [-1,0], [1,0], [-1,-1], [0,-1], [-1,-1]]
        pieces = last_move_player.pieces_own    # list pieces active on board
        king_square = self.board.get_square(king_owner.king)                  # King square object

        for colvec, rowvec in moves:
            target_col = king_square.col + colvec
            target_row = king_square.row + rowvec

            if self.board.is_valid(target_col, target_row):
                square_offset = target_row * 8 + target_col   # offset in list of board squares
                destination = self.board.squares[square_offset] # destination = new king square, possible in next move
                if destination.piece:                       # any piece, no move
                    if destination.piece.color == king_owner.king:  # self piece
                        break
            else:
                break

            flag = False
            for piece in pieces:
                if piece.field == destination.name:
                    break   # piece could be capture by king
                for k,v in self.get_valid_moves(piece):
                    for record in v:
                        destination, capture = record
                        if capture:
                            if destination == capture:  # move king to this destination will not avoid check
                                flag = False
                            break



                pass

    def is_pawn_promotion(self):
        pass

    def is_valid_move(self, piece, destination):
        for move_data in self.valid_moves[piece]:
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

        # move & capture
        if capture_piece:
            # mate
            if isinstance(capture_piece, Król):
                self.set_mate(self.pause_player)
            # regular capture
            print('Game/move/capture:', capture_piece.name_long, capture_piece.color, capture_piece.field)
            taken_piece = self.board.take_piece(capture_piece)
            self.current_player.add_captured( taken_piece )
        self.board.move(piece, destination)

        # update self.last_move after move
        if capture_piece:
            self.last_move = [source, destination, capture_piece]
        else:
            self.last_move = [source, destination, None]

        self.en_passant = False                             # clear en passant after every move
        if isinstance(piece, Pion):
            if int(abs(source.row - destination.row)) == 2: # if condition true, set remember en passant for next move
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

                    # move & capture if any
                    self.move(piece, source, valid_destination, valid_capture_piece)

                    # check
                    for player in self.players:
                        if player.king:
                            if self.is_check(player.king):
                                self.set_check(player)
                            else:
                                self.clear_check(player)



                    # # check mate
                    # if self.is_mate():
                    #     self.mate_flag = True
                    #     self.end_game()
                    # else:
                    #     pass

                    # # check check
                    # if self.is_check(self.current_player, self.pause_player):
                    #     self.check_flag = True
                    # else:
                    #     self.check_flag = False

                    # other settings
                    self.set_untouching()
                    # clear last moves calculation
                    self.valid_moves = {}
                    # turn players
                    self.turn_players()

                else:
                    # if player select first square (source)
                    source = square
                    piece = source.piece
                    if piece:
                        if player.set_touch(piece):
                            pass
                            # # TODO check this down below:
                            # piece.set_current_moves(self.get_valid_moves(piece))

    def set_check(self, player):
        self.check_flag = True
        player.check_flag = True
        player.status_check_mate = 'Check!'

    def set_mate(self, player):
        self.mate_flag = True
        player.mate_flag = True
        player.king = False
        player.status_check_mate = 'Mate!'
        self.play = False

    def set_untouching(self):
        self.current_player.set_untouching()

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