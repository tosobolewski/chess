class Square:
    def __init__(self, offset, col, row, field, color):
        self.offset = offset
        self.col = col
        self.row = row
        self.name = field    # 'a1', 'a2' ... 'h8'
        self.color = color
        self.piece = None
        self.canvas_center = None   # tuple: (canvasx, canvasy)

    def add(self, piece):
        if self.piece:
            return False
        else:
            self.piece = piece
            return True

    def give(self):
        if self.piece:
            _piece = self.piece
            self.piece = None
            return _piece
        return False

    def is_empty(self):
        if self.piece:
            return False
        else:
            return True

    def show(self):
        print(self.offset, self.col, self.row, self.name, self.col, self.piece)


# ----------------------------------------- main ------------------------------------------


def test():
    pass


def main():
    test()
    pass

if __name__ == "__main__":
    main()