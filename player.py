from pieces import *


PLAYER_STATUS = ['waiting', 'moving']


class Player():
    def __init__(self, name, pieces_color, forward):
        self.name = name
        self.color_pieces = pieces_color
        self.pieces_own = []
        self.pieces_captured = []
        self._touch = False          # piece object
        self.status = PLAYER_STATUS[0]      # status = string 'waiting' or 'moving'
        self.status_check_mate = '-'
        self.forward = forward     # direction, when pieces move forward (N)orth for white or (S)outh for balck
        self.king = None
        self.check_flag = None
        self.mate_flag = False

    def add(self, piece):
        if piece.color == self.color_pieces:
            self.pieces_own.append(piece)
            if isinstance(piece, Król):
                self.king = piece
            return True
        else:
            return False

    def add_captured(self, piece):
        if self.name == piece.player.name:
            return False
        else:
            self.pieces_captured.append(piece)
            return True

    def clear(self):
        self.pieces_own = []
        self.pieces_captured = []
        self._touch = False                 # piece object
        self.status = PLAYER_STATUS[0]      # status = string 'waiting' or 'moving'
        self.status_check_mate = '-'
        self.king = None
        self.check_flag = None
        self.mate_flag = False

    def get_touch(self):
        return self._touch

    def remove(self, piece):
        index = 0
        for piece_own in self.pieces_own:
            if piece_own.field == piece.field:
                return self.pieces_own.pop(index)
            index += 1
        return False

    def is_touching(self):
        if self._touch:
            return True
        return False

    def show(self):
        print('Player:', self.name, ', pieces color:', self.color_pieces)
        print('own:', len(self.pieces_own), ':', self.pieces_own)
        print('captured:', len(self.pieces_captured), ':', self.pieces_captured)
        print()

    def set_touch(self, piece):
        if piece:
            if piece.color == self.color_pieces:
                if self.is_touching():
                    return False
                else:
                    self._touch = piece
                    return True
            else:
                print('touch false, incompatible colors')
                return False

    def set_untouching(self):
        self._touch = False

# ----------------------------------------- main ------------------------------------------


def test():
    pass


def main():
    test()
    pass

if __name__ == "__main__":
    main()