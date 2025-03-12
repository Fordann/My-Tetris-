import pygame
import time
import curses
from pygame.locals import *
import Board

pygame.init()
screen = pygame.display.set_mode((1,1))          
pygame.time.set_timer(USEREVENT+1, 200)

def game_loop(stdscr):
    curses.curs_set(0)  
    stdscr.nodelay(1)  
    stdscr.timeout(100) 

    board = Board.Board()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == USEREVENT+1:
                if board.apply_gravity() == "LOST":
                    stdscr.addstr(0, 0, "GAME OVER!", curses.A_BOLD)
                    stdscr.refresh()
                    time.sleep(2)
                    return

                board.destroy_filled_lines()

            if event.type == QUIT:
                pygame.quit()
                running = False
                break            

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    running = False
                    break

                elif event.key == pygame.K_RIGHT and not board.is_current_piece_colliding_with("right"):
                    board.current_moving_piece.move_one_case_to_the_right()
                
                elif event.key == pygame.K_LEFT and not board.is_current_piece_colliding_with("left"):
                    board.current_moving_piece.move_one_case_to_the_left()

                elif event.key == pygame.K_UP and not board.is_current_piece_colliding_with("rotation"):
                    board.current_moving_piece.rotate()

        board.display(stdscr)

def main():
    curses.wrapper(game_loop)

if __name__ == "__main__":
    main()

