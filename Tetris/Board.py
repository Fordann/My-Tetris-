import mask_board
import Piece
import utils

class Board:
    def __init__(self):
        self.current_moving_piece = Piece.Piece()
        self.mask = mask_board.board

    def board_mask_combined_with_current_moving_piece_mask(self):
        return [
            int(byte) for 
            byte in str("{0:b}".format(utils.from_mask_to_string(self.mask) ^ self.current_moving_piece.mask))
        ]

    def add_current_piece_to_mask_board(self):  
        self.mask = self.board_mask_combined_with_current_moving_piece_mask()

    def is_current_piece_colliding_with(self, direction_to_check_collision):
        if direction_to_check_collision == "right":
            return utils.from_mask_to_string(self.mask) & self.current_moving_piece.move_mask_one_case_to_the_right()

        if direction_to_check_collision == "left":
            return utils.from_mask_to_string(self.mask) & self.current_moving_piece.move_mask_one_case_to_the_left()

        if direction_to_check_collision == "bottom":
            return utils.from_mask_to_string(self.mask) & self.current_moving_piece.move_mask_one_case_to_the_bottom()

        if direction_to_check_collision == "rotation":
            return utils.from_mask_to_string(self.mask) & self.current_moving_piece.rotate_mask()

        if direction_to_check_collision == "limit":
            return utils.from_mask_to_string(self.mask) & utils.from_mask_to_string(mask_board.board_limit)

    def apply_gravity(self):
        if self.is_current_piece_colliding_with("limit"):
            return "LOST"

        if not self.is_current_piece_colliding_with("bottom"):
            self.current_moving_piece.move_one_case_to_the_bottom()
        else:
            self.add_current_piece_to_mask_board()
            self.current_moving_piece = Piece.Piece()


    
    def destroy_filled_lines(self):
        for line in range(mask_board.SIZE_COLUMN_BOARD - 1):
            starting_line_index = line * mask_board.SIZE_LINE_BOARD
            line_mask = self.mask[starting_line_index: starting_line_index + mask_board.SIZE_LINE_BOARD]
            if sum(line_mask) == mask_board.SIZE_LINE_BOARD:
                del self.mask[starting_line_index: starting_line_index + mask_board.SIZE_LINE_BOARD]
                self.mask = [1]+[0]*(mask_board.SIZE_LINE_BOARD - 2)+[1] + self.mask
                break

    def display(self, stdscr):
        combined_mask = self.board_mask_combined_with_current_moving_piece_mask()
        board_width = mask_board.SIZE_LINE_BOARD

        stdscr.clear()
        for i, bit in enumerate(combined_mask):
            if i % board_width == 0 and i > 0:
                stdscr.addstr("\n")
            stdscr.addstr("█" if bit == 1 else " ")
        stdscr.refresh()
