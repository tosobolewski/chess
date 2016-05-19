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
        self.last_move = [None, None, None, None]
        pass

    def end_game(self):
        pass

    def start_game(self):
        # clear player state
        for player in self.board.players:
            player.clear_pieces()
            player.clear_touch()
            player.last_captured = None

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
        Return list of all valid offsets of squares in list 'self.squares=[]' in Board,
        that piece can move on or captured
        :param piece:   piece object that valid moves are calculated
        :return:        list [int, int, ..]
        '''
        square = self.board.get_square(piece.field)
        square_col = square.col
        square_row = square.row
        square_offset = square.offset
        vectors_all = piece.getMoveVectors()
        color = square.piece.color

        valid_offsets = []
        for direction in vectors_all:
            for c, r in vectors_all[direction]:
                move_col = square_col + c
                move_row = square_row + r
                move_offset = move_row * 8 + move_col

                if move_col < 0 or move_col > 7:
                    break                           # break appending offsets in current direction
                if move_row < 0 or move_row > 7:
                    break

                square_dest = self.board.squares[move_offset]
                if square_dest.piece:
                    if square_dest.piece.color == color:    # self piece
                        break
                    else:
                        valid_offsets.append(move_offset)
                        break
                else:
                    valid_offsets.append(move_offset)
        return valid_offsets



    def is_valid_move(self, piece, dest_field):
        destination_square = self.board.get_square(dest_field)
        if destination_square.offset in self.get_valid_moves(piece):
            return True
        else:
            return False


    def select(self, player, field):

        if self.play:
            if player == self.current_player:
                # if player select second field
                if player.is_touching():
                    dest_square = self.board.get_square(field)

                    # if player select the same field that touch before
                    if player.get_touch().field == field:
                        player.clear_touch()
                        return None

                    #validate move
                    touch_piece = player.get_touch()
                    if self.is_valid_move(touch_piece, field) != True:
                        return None

                    # if player select empty second field
                    if dest_square.is_empty():
                        # update board state
                        self.board.move(touch_piece, field)
                        # update player state
                        player.clear_touch()
                        # turn players
                        self.turn_players()
                    else:
                        # if player select second field owned by opponent's piece
                        capture_piece = dest_square.piece
                        if player != capture_piece.player:
                            # captured: removes & move
                            # give piece from other player
                            player.capture(capture_piece)
                            # update board state
                            self.board.remove(capture_piece)
                            self.board.move(touch_piece, field)
                            # update player state
                            player.clear_touch()
                            # turn players in game
                            self.turn_players()

                else:
                    # if player select first field
                    piece = self.board.get_square(field).piece
                    if piece:
                        if player.set_touch(piece):
                            piece.set_current_moves(self.get_valid_moves(piece))



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