class Piece:
    def __init__(self, player, field):
        self.player = player
        self.captured = False
        self.field = field
        self.color = player.color_pieces
        self.name_short = None
        self.name_long = None
        self.photo = None
        self.canvas_id = None
        self.first_move_vectors = {}
        self.move_vectors = {}

    def getMoveVectors(self):
            '''
            Return dictionary {direction : [vectors]} vectors when piece can move
            :return: dictionary
            '''
            return self.move_vectors

    def update_field(self, field):
        self.field = field

    def show(self):
        print(self.name_long, self.name_short, self.field, self.color)


class Pion(Piece):
    def __init__(self, player, field):
        super().__init__(player, field)
        self.name_short = 'P'
        self.name_long = 'Pion'
        self.possible_moves = [[0,0], [0,1]]
        self.start_field = field
        self.capture_vectors = []
        if self.player.forward == 'N':                              # 'white'
            self.first_move_vectors = {'N' : [[0, 1], [0, 2]]}
            self.move_vectors = {'N' : [[0, 1]]}
            self.capture_vectors = {'NW' : [[-1,1]],
                                    'NE' : [[1,1]]
                                    }
        else:                                                       # 'black'
            self.first_move_vectors = {'S': [[0, -1], [0, -2]]}
            self.move_vectors = {'S': [[0, -1]]}
            self.capture_vectors = {'SW' : [[-1,-1]],
                                    'SE' : [[1,-1]]
                                    }

    def getMoveVectors(self):
        if self.start_field == self.field:  # if first move, pawn moves one or two fields ahead,
                                            # next moves only one field
            return (self.first_move_vectors, self.capture_vectors)
        else:
            return (self.move_vectors, self.capture_vectors)


class Wieża(Piece):
    def __init__(self, player, field):
        super().__init__(player, field)
        self.name_short = 'W'
        self.name_long = 'Wieża'
        self.move_vectors = {'N' : [[0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7]],
                             'S' : [[0,-1], [0,-2], [0,-3], [0,-4], [0,-5], [0,-6], [0,-7]],
                             'W' : [[-1,0], [-2,0], [-3,0], [-4,0], [-5,0], [-6,0], [-7,0]],
                             'E' : [[1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0]],
                            }


class Skoczek(Piece):
    def __init__(self, player, field):
        super().__init__(player, field)
        self.name_short = 'S'
        self.name_long = 'Skoczek'
        self.move_vectors = {'N' : [[-1,2]],
                             'S' : [[-1,-2]],
                             'W' : [[-2,-1]],
                             'E' : [[2,-1]],
                             'N2' : [[1,2]],
                             'S2' : [[1,-2]],
                             'W2' : [[-2,1]],
                             'E2' : [[2,1]],
                            }


class Goniec(Piece):
    def __init__(self, player, field):
        super().__init__(player, field)
        self.name_short = 'G'
        self.name_long = 'Goniec'
        self.move_vectors = {'NW' : [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7]],
                             'NE' : [[1,-1], [2,-2], [3,-3], [4,-4], [5,-5], [6,-6], [7,-7]],
                             'SW' : [[-1,-1], [-2,-2], [-3,-3], [-4,-4], [-5,-5], [-6,-6], [-7,-7]],
                             'SE' : [[-1,1], [-2,2], [-3,3], [-4,4], [-5,5], [-6,6], [-7,7]],
                            }


class Hetman(Piece):
    def __init__(self, player, field):
        super().__init__(player, field)
        self.name_short = 'H'
        self.name_long = 'Hetman'
        self.move_vectors = {'N' : [[0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7]],
                             'S' : [[0,-1], [0,-2], [0,-3], [0,-4], [0,-5], [0,-6], [0,-7]],
                             'W' : [[-1,0], [-2,0], [-3,0], [-4,0], [-5,0], [-6,0], [-7,0]],
                             'E' : [[1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0]],
                             'NW' : [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7]],
                             'NE' : [[1,-1], [2,-2], [3,-3], [4,-4], [5,-5], [6,-6], [7,-7]],
                             'SW' : [[-1,-1], [-2,-2], [-3,-3], [-4,-4], [-5,-5], [-6,-6], [-7,-7]],
                             'SE' : [[-1,1], [-2,2], [-3,3], [-4,4], [-5,5], [-6,6], [-7,7]],
                            }


class Król(Piece):
    def __init__(self, player, field):
        super().__init__(player, field)
        self.name_short = 'K'
        self.name_long = 'Król'
        self.move_vectors = {'N' : [[0,1]],
                             'S' : [[0,-1]],
                             'W' : [[-1,0]],
                             'E' : [[1,0]],
                             'NW' : [[1,1]],
                             'NE' : [[1,-1]],
                             'SW' : [[-1,-1]],
                             'SE' : [[-1,1]],
                            }

        self.check_vectors = [

                    ([Wieża, Hetman],  {'S' : [[0,1], [0,2], [0,3], [0,4], [0,5], [0,6], [0,7]],
                                         'N' : [[0,-1], [0,-2], [0,-3], [0,-4], [0,-5], [0,-6], [0,-7]],
                                         'E' : [[-1,0], [-2,0], [-3,0], [-4,0], [-5,0], [-6,0], [-7,0]],
                                         'W' : [[1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0]]}),

                    ([Goniec, Hetman], {'SE' : [[1,1], [2,2], [3,3], [4,4], [5,5], [6,6], [7,7]],
                                         'SW' : [[1,-1], [2,-2], [3,-3], [4,-4], [5,-5], [6,-6], [7,-7]],
                                         'NE' : [[-1,-1], [-2,-2], [-3,-3], [-4,-4], [-5,-5], [-6,-6], [-7,-7]],
                                         'NW' : [[-1,1], [-2,2], [-3,3], [-4,4], [-5,5], [-6,6], [-7,7]]}),
                    ([Skoczek],         {'S' : [[-1,2]],
                                         'N' : [[-1,-2]],
                                         'E' : [[-2,-1]],
                                         'W' : [[2,-1]],
                                         'S2' : [[1,2]],
                                         'N2' : [[1,-2]],
                                         'E2' : [[-2,1]],
                                         'W2' : [[2,1]]})
                    ]

        self.check_vectors_pawn = {}
        if player.forward == 'N':        # king white
            self.check_vectors.append(([Pion], {'SE' : [[1,-1]],
                                                'SW' : [[1,1]]}))

        if player.forward == 'S':        # king black
            self.check_vectors.append(([Pion], {'NE' : [[-1,-1]],
                                                'NW' : [[-1,1]]}))

    def get_check_vectors(self):
        return self.check_vectors


# ----------------------------------------- main ------------------------------------------


def test():
    pass


def main():
    test()
    pass

if __name__ == "__main__":
    main()
