import pygame
import random
import reversi.view as view
import reversi.board as board
import reversi.common as common
from reversi.view import *
from reversi.board import *
from reversi.common import *


class game_manager:
    """
	The Main class which handle the overall game control
	"""

    def __init__(self):
        ## create a veiw and a model objects
        self.window = view.game_interface()
        self.board = board.game_model()

        ## Show the intro screen and get the initial game parameters
        self.game_mode = self.window.intro_screen()
        self.current_playing = 0  # 0 -> player_1, 1 -> player_2

    # The main game function handling the game loop
    def play(self):
        pygame.time.wait(300)
        clock = pygame.time.Clock()
        while True:
            if self.board.is_game_ended():
                count_white, count_black = self.board.get_cell_count()
                if count_black > count_white:
                    self.winner = "BLACK"
                elif count_white > count_black:
                    self.winner = "WHITE"
                else:
                    self.winner = "TIE"
                self.next_action = self.window.result_screen(self.winner)
                pygame.time.wait(300)
                if self.next_action == "Continue":
                    self.board.reset_game_board()
                    self.game_mode = self.window.intro_screen()
                else:
                    break

            if self.game_mode[self.current_playing] == "Human":
                valid_moves = self.board.get_valid_moves(self.current_playing)

                clicked_cell = self.window.game_screen(self.board.grid, True)
                while clicked_cell[0] * 8 + clicked_cell[1] not in valid_moves:
                    clicked_cell = self.window.game_screen(self.board.grid, True)

                self.board.make_move(clicked_cell, self.current_playing)


            else:  ## current player is the computer actor
                pygame.time.wait(300)

                if self.game_mode[2] == "Easy":  # Random move
                    ##########print "Easy"
                    valid_moves = self.board.get_valid_moves(self.current_playing)
                    rand_move = random.randint(0, len(valid_moves) - 1)
                    clicked_cell = (valid_moves[rand_move] // common.SIDE_LEN, \
                                    valid_moves[rand_move] % common.SIDE_LEN)
                    self.board.make_move(clicked_cell, self.current_playing)

            self.current_playing = 1 - self.current_playing  ## switch to te next player
            self.window.game_screen(self.board.grid, False)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()
            clock.tick(60)


# The main Function
def reversi():
    game = game_manager()  ## create a game instance
    game.play()  ## run the game


if __name__ == '__main__':
    reversi()
