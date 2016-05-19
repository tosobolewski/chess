from tkinter import *
from board import *

SQUARE_DIM = 50
OFFSET = SQUARE_DIM
PIECES = ['king', 'queen', 'rook', 'bishop', 'knight', 'pawn']
NAME_CONVERSION_DICT = {'K': 'king', 'H': 'queen', 'W': 'rook', 'G': 'bishop', 'S': 'knight', 'P': 'pawn'}
PATH_IMAGE_BIG = 'image/150x150px'
PATH_IMAGE_MEDIUM = 'image/40x40px'
PATH_IMAGE_SMALL ='image/26x26px'
PATH_UTILS_MEDIUM = 'image/40x40px'

IMAGE_SMALL_WIDTH = 26   # pixel
OFFSET_SMALL = IMAGE_SMALL_WIDTH


class Window():
    def __init__(self, game):

        self.game = game
        self.board = self.game.board

        self.square_selected = None  # square object
        self.play_game = False
        self.end_game = None
        self.current_player = self.board.players[0]
        self.pause_player = self.board.players[1]
        self.last_move_copy = []
        self.is_movable_fields_show = False
        self.utils_id = []

        # root window & frames
        self.root = Tk()
        self.frameCanvas = Frame(self.root)
        self.frameInfo = Frame(self.root)
        self.frameCanvas.pack(side=LEFT)
        self.frameInfo.pack(side=LEFT)

        # main Canvas Frame
        self.canvasMain = Canvas(self.frameCanvas, bg='cornsilk', width=SQUARE_DIM*10, height=SQUARE_DIM*10)
        self.canvasMain.pack()

        # create player panel for each players, remember it in player object
        for player in self.board.players:
            player.player_panel = PlayerPanel(self.frameInfo, player)

        # create button StartGame
        self.buttonStartGame = Button(self.frameInfo, text='Start Game', command=self.button_start_game)
        self.buttonStartGame.pack(fill=X, pady=50, padx=50)

        # # create button EndGame
        # self.buttonEndGame = Button(self.frameInfo, text='End Game', command=self.button_end_game)
        # self.buttonEndGame.pack(fill=X, pady=50, padx=50)

        # show board rectangles
        self.id_csquare_dict = {}
        self.rectangles = []
        self.show_squares(self.board)

        # create fields for canvas piece icons data
        # deploying pieces is in command connected to button StartGame
        self.photo = []
        self.canvasMain.pieces_id = []
        self.id_pieces_dict = {}

        # utilities
        name = 'cross-red'
        file_path = PATH_UTILS_MEDIUM + '/' + 'utils' + '/' + name + '.gif'
        self.photo_cross_red = PhotoImage(file=file_path)
        self.id_utils_dict = {}

        # mouse events
        Widget.bind(self.canvasMain, "<Button-1>", self.mouseDown)

        # run tkinter main loop
        self.root.mainloop()

    def button_start_game(self):
        self.game.start_game()

        self.canvasMain.delete('piece')
        # show pieces on board in start position
        for player in self.board.players:
            self.show_pieces(self.canvasMain, player.pieces_own, player)
            player.player_panel.clear()
            player.player_panel.update_status()

    def button_end_game(self):
        self.game.end_game()
        self.hide_touch_and_utils(self.canvasMain)

    def get_square(self, id):
        '''
        Return tuple (square object, piece object), based on board canvas id one of them
        :param id: board canvas id (square object or piece object bind to square)
        :return: tuple(square obj, piece obj)
        '''
        # if mouse select piece
        if id in self.id_pieces_dict:
            piece, player = self.id_pieces_dict[id]
            square = self.board.get_square(piece.field)
            return square
        # if mouse select square
        if id in self.id_csquare_dict:
            csquare = self.id_csquare_dict[id]
            field = csquare.name
            square = self.board.get_square(field)
            return square
        # if mouse select some utils, eg. cross icon
        if id in self.id_utils_dict:
            square, utils = self.id_utils_dict[id]
            return square

    def hide_touch_and_utils(self, canvas):
        canvas.delete('touch')
        canvas.delete('cross')
        self.is_movable_fields_show = False
        self.id_utils_dict = {}

    def mouseDown(self, event):
        canvasx = self.canvasMain.canvasx(event.x)
        canvasy = self.canvasMain.canvasx(event.y)
        id = self.canvasMain.find_closest(canvasx, canvasy)
        id = id[0]


        square = self.get_square(id)

        # remember here current player before game change it
        cp = self.game.current_player

        # send mouse selected field to Game, where Game state and Board state are update
        self.game.select(self.game.current_player, square.name)

        # if player touch first field show that field and possible moves
        if cp.is_touching():
            self.show_touch(self.canvasMain, cp.get_touch().field)
            self.show_movable_fields(self.canvasMain, cp.get_touch())
        else:
            self.hide_touch_and_utils(self.canvasMain)

        # if player captured opponent's piece, clear that piece on canvas board
        if cp.last_captured:
            if cp.last_captured.canvas_id:
                self.remove(self.canvasMain, cp.last_captured.canvas_id)
                cp.last_captured.canvas_id = None

        # if player move, move his pieces on canvas board
        if self.board.last_move == self.last_move_copy:
            pass
        else:
            self.update(self.canvasMain, self.board.last_move)
            self.last_move_copy = self.board.last_move

        # update player panel status
        for player in self.game.players:
            player.player_panel.update_status()
        cp.player_panel.update_captured()
        cp.last_captured = None

    def remove(self, canvas, id):
        canvas.delete(id)

    def set_square_selected(self, selected):
        if self.square_selected:
            return False
        else:
            self.square_selected = selected
            return True

    def show_touch(self, canvas, field):
        square = self.board.get_square(field)
        cx, cy = square.canvas_center
        dim = SQUARE_DIM /2 - 3
        top = cy + dim
        bottom = cy - dim
        left = cx - dim
        right = cx + dim
        canvas.create_rectangle(left, top, right, bottom, fill='', outline='yellow', width=3, tags='touch')

    def show_movable_fields(self,canvas, piece):
        if self.is_movable_fields_show:
            return False
        else:
            if piece.getCurrentMoves():
                for offset in piece.getCurrentMoves():
                    square = self.board.squares[offset]
                    x, y = square.canvas_center
                    id = canvas.create_image(x, y,image=self.photo_cross_red, tags='cross')
                    self.id_utils_dict[id] = (square, None)
                    pass

    def show_pieces(self, canvas, piece_list, player):
        for piece in piece_list:
            color = piece.color
            name = NAME_CONVERSION_DICT[piece.name_short]
            file_path = PATH_IMAGE_MEDIUM + '/' + color + '/' + name + '.gif'
            photo = PhotoImage(file=file_path)
            square = self.board.get_square(piece.field)
            col, row = square.col, square.row
            x = OFFSET + col * SQUARE_DIM + (SQUARE_DIM/2)
            y = OFFSET + (len(HORIZONTAL)-row) * SQUARE_DIM - (SQUARE_DIM/2)
            id = canvas.create_image(x, y,image=photo, tags='piece')
            self.id_pieces_dict[id] = (piece, player)
            piece.canvas_id = id
            piece.photo = photo

    def show_squares(self, board):
        for square in board.squares:
            col = square.col
            row = square.row
            name = square.name
            color = square.color
            left = OFFSET + col * SQUARE_DIM
            right = left + SQUARE_DIM
            top = (OFFSET) + (8 * SQUARE_DIM) - (row * SQUARE_DIM)
            bottom =  (top - SQUARE_DIM)
            box_coord = (left, top, right, bottom)
            canvassquare = CanvasSquare(self.canvasMain, box_coord, name, color)
            self.rectangles.append(canvassquare)
            self.id_csquare_dict[canvassquare.id] = canvassquare
            square.canvas_center = ((left+right)/2, (top+bottom)/2)

    def update(self, canvas, fields):
        '''
        Updates two fields on canvas board.
        :param fields: list of two fields (as string) changed after 'move' a piece; field_source and field_destination
        :return:
        '''
        for field in fields:
            square = self.board.get_square(field)
            if square.piece:
                id = square.piece.canvas_id
                new_canvasx, new_canvasy = square.canvas_center
                canvas.coords(id, new_canvasx, new_canvasy)


class CanvasSquare():
    def __init__(self, canvas, coordinates, name, color):
        self.name = name                # 'a1', 'a2' .. 'h8'
        self.color = color
        self.coordinates = coordinates  # (left, top, right, bottom)
        self.id = canvas.create_rectangle(coordinates, fill=color, tags='boardsquare')


class PlayerPanel():

    def __init__(self, frame, player):
        self.frame = frame
        self.player = player
        self.pieces_captured = player.pieces_captured
        self.captured_number = len(self.pieces_captured)
        self.player_name = player.name
        self.color_pieces = player.color_pieces
        self.id_pieces_dict = {}

        # create player name label with color pieces
        self.labelPlayer = Label(self.frame, text='Player ' + self.player_name +
                                                  ' / ' + 'pieces: ' + self.color_pieces)
        self.labelPlayer.pack()
        # create status label (is moving/waiting)
        self.labelStatus = Label(self.frame, text='Status: ' + self.player.status)
        self.labelStatus.pack()
        # create captured label
        self.labelCaptured = Label(self.frame, text='Player ' + self.player_name + ' captured:')
        self.labelCaptured.pack()
        # create canvas for showing captured pieces
        self.canvas = Canvas(self.frame, bg='cornsilk',
                             width=IMAGE_SMALL_WIDTH * 9,
                             height=IMAGE_SMALL_WIDTH * 3)
        self.canvas.pack()

    def clear(self):
        self.pieces_captured = self.player.pieces_captured
        self.captured_number = len(self.pieces_captured)
        self.id_pieces_dict = {}
        self.canvas.delete(ALL)

    def update_captured(self):
        '''
        Updates captured pieces icons on player canvas based on 'self.pieces list'.
        Updates player status.
        :return:
        '''
        self.pieces_captured = self.player.pieces_captured
        if len(self.pieces_captured) > self.captured_number:
            for i in range(self.captured_number, len(self.pieces_captured)):
                self._show(self.pieces_captured[i], i)
            self.captured_number = len(self.pieces_captured)

    def update_status(self):
        self.labelStatus.config(text='Status: ' + self.player.status)

    def _show(self, piece, index):
        '''
        Show one piece icon on canvas at position index
        :param piece: piece object
        :param index: int, nth position on canvas
        :return:
        '''
        color = piece.color
        name = NAME_CONVERSION_DICT[piece.name_short]
        file_path = PATH_IMAGE_SMALL + '/' + color + '/' + name + '.gif'
        photo = PhotoImage(file=file_path)

        col = index % 8
        row = index // 8

        x = OFFSET_SMALL + col * IMAGE_SMALL_WIDTH
        y = OFFSET_SMALL + row * IMAGE_SMALL_WIDTH
        id = self.canvas.create_image(x, y, image=photo)
        self.id_pieces_dict[id] = piece
        piece.canvas_id = id
        piece.photo = photo


# ----------------------------------------- main ------------------------------------------


def test():
    pass


def main():
    test()
    pass

if __name__ == "__main__":
    main()