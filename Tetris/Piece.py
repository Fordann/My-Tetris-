import random
import mask_piece
import mask_board
import utils

LIST_OF_AVAILABLE_PIECE = ['L','T','square','straight']


class Piece:
    def __init__(self):
        self.name = random.choice(LIST_OF_AVAILABLE_PIECE)
        self.mask = self.get_mask_from_rotation('init_position')
        self.position_on_the_board = 0
        self.current_rotation = 0
   
    def get_piece_rotation(self, rotation):
        if (rotation == "init_position"):
            rotation = '0'
        else:
            rotation = str(int(rotation) % len(mask_piece.set_of_pieces[self.name]))
        return mask_piece.set_of_pieces[self.name][rotation]

    def get_mask_from_rotation(self, rotation):
        return utils.from_mask_to_string(self.get_piece_rotation(rotation))

    def move_mask_one_case_to_the_right(self):
        return self.mask >> 1

    def move_one_case_to_the_right(self):
        self.mask = self.move_mask_one_case_to_the_right()
        self.position_on_the_board +=1

    def move_mask_one_case_to_the_left(self):
        return self.mask << 1

    def move_one_case_to_the_left(self):
        self.mask = self.move_mask_one_case_to_the_left()
        self.position_on_the_board -=1

    def move_mask_one_case_to_the_bottom(self):
        return self.mask >> mask_board.SIZE_LINE_BOARD

    def move_one_case_to_the_bottom(self):
        self.mask = self.move_mask_one_case_to_the_bottom()
        self.position_on_the_board += mask_board.SIZE_LINE_BOARD 
    
    def rotate_mask(self):
        return self.get_mask_from_rotation(self.current_rotation + 1) >> self.position_on_the_board

    def rotate(self):
        self.mask = self.rotate_mask()
        self.current_rotation +=1
