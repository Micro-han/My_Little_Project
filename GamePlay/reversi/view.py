import pygame
import time
import common
from common import *


class game_interface:
    """
	The GUI class responsible for the game graphics
	and all (input / output) interactions.
	"""

    def __init__(self):

        pygame.init()

        # main colors
        self.BLACK_COLOR = (0, 0, 0)
        self.WHITE_COLOR = (255, 255, 255)
        self.BACKGROUND_COLOR = (0, 140, 90)
        self.BUTTON_INACTIVE_COLOR = (0, 250, 150)
        self.BUTTON_ACTIVE_COLOR = (0, 100, 100)
        self.BORDER_COLOR = (205, 133, 63)  ## peru -> #CD853F

        # display parameters
        self.SCREEN_SIZE = (700, 500)
        self.BOARD_SIZE = 400
        self.BORDER_SIZE = 20
        self.CELL_SIZE = 50

        # start the game screen
        self.game_display = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Reversi GAME")

    def intro_screen(self):
        """
		Show the intro screen and return either 
		user choose 1 player or two players mode
		"""

        while True:
            self.game_display.fill(self.BACKGROUND_COLOR)

            game_title_font = pygame.font.SysFont('comicsansms', 100)
            game_title = game_title_font.render("Reversi Game", True, self.WHITE_COLOR)
            game_title_pos = game_title.get_rect()
            game_title_pos.center = (self.SCREEN_SIZE[0] // 2, self.SCREEN_SIZE[1] // 2 - 50)

            self.game_display.blit(game_title, game_title_pos)

            mode1_clicked = self.add_button("1 Player", 100, 350, 100, 50, \
                                            self.BUTTON_INACTIVE_COLOR, self.BUTTON_ACTIVE_COLOR)
            mode2_clicked = self.add_button("Start", 300, 350, 100, 50, \
                                            self.BUTTON_INACTIVE_COLOR, self.BUTTON_ACTIVE_COLOR)
            exit_game_clicked = self.add_button("Exit", 500, 350, 100, 50, \
                                                self.BUTTON_INACTIVE_COLOR, self.BUTTON_ACTIVE_COLOR)

            if mode1_clicked == True:
                diff_level = self.get_diff_level()
                return ("Human", "Computer", diff_level)

            if mode2_clicked == True:
                return ("Human", "Human", "NONE")

            if exit_game_clicked == True:
                pygame.quit()
                quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()

    def result_screen(self, winner):
        """
		Show the result screen and return either 
		continue or it exits the game
		"""

        while True:
            self.game_display.fill(self.BACKGROUND_COLOR)

            game_title_font = pygame.font.SysFont('comicsansms', 100)
            if winner != "TIE":
                game_title = game_title_font.render(winner + " Wins", True, self.WHITE_COLOR)
            else:
                game_title = game_title_font.render("TIE", True, self.WHITE_COLOR)
            game_title_pos = game_title.get_rect()
            game_title_pos.center = (self.SCREEN_SIZE[0] // 2, self.SCREEN_SIZE[1] // 2 - 50)

            self.game_display.blit(game_title, game_title_pos)

            mode1_clicked = self.add_button("Continue", 200, 350, 100, 50, \
                                            self.BUTTON_INACTIVE_COLOR, self.BUTTON_ACTIVE_COLOR)
            exit_game_clicked = self.add_button("Exit", 400, 350, 100, 50, \
                                                self.BUTTON_INACTIVE_COLOR, self.BUTTON_ACTIVE_COLOR)

            if mode1_clicked == True:
                return "Continue"

            if exit_game_clicked == True:
                return "Exit"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()

    def get_diff_level(self):
        """
		Show the diff levels and return the selected
		"""

        while True:
            self.game_display.fill(self.BACKGROUND_COLOR)

            game_title_font = pygame.font.SysFont('comicsansms', 100)
            game_title = game_title_font.render("Reversi Game", True, self.WHITE_COLOR)
            game_title_pos = game_title.get_rect()
            game_title_pos.center = (self.SCREEN_SIZE[0] // 2, self.SCREEN_SIZE[1] // 2 - 50)

            self.game_display.blit(game_title, game_title_pos)

            diff_easy = self.add_button("Easy", 300, 300, 100, 50, \
                                        self.BUTTON_INACTIVE_COLOR, self.BUTTON_ACTIVE_COLOR)
            diff_hard = self.add_button("Hard", 300, 400, 100, 50, \
                                        self.BUTTON_INACTIVE_COLOR, self.BUTTON_ACTIVE_COLOR)

            if diff_easy == True:
                return "Easy"
            if diff_hard == True:
                return "Hard"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()

    def add_button(self, message, start_X, start_Y, width, height, inactive_col, active_col):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        is_clicked = False

        draw_color = inactive_col
        if start_X + width > mouse_pos[0] > start_X and start_Y + height > mouse_pos[1] > start_Y:
            draw_color = active_col
            if mouse_click[0] == 1:
                is_clicked = True

        pygame.draw.rect(self.game_display, draw_color, (start_X, start_Y, width, height))

        button_text_font = pygame.font.SysFont('comicsansms', 20)
        button_text = button_text_font.render(message, True, self.BLACK_COLOR)
        button_text_pos = button_text.get_rect()
        button_text_pos.center = (start_X + width // 2, start_Y + height // 2)

        self.game_display.blit(button_text, button_text_pos)

        return is_clicked

    def get_pressed_cell(self):
        pygame.event.get()  ## To flush
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if mouse_click[0] == 0:
            return (-1, -1)

        if 150 + self.BOARD_SIZE > mouse_pos[0] > 150 and 50 + self.BOARD_SIZE > mouse_pos[1] > 50:
            pos_X = mouse_pos[0] - 150
            pos_Y = mouse_pos[1] - 50
            pos_X = pos_X // self.CELL_SIZE
            pos_Y = pos_Y // self.CELL_SIZE
            return (pos_X, pos_Y)

        return (-1, -1)

    def game_screen(self, grid, need_click):
        """
		Main game screen
  		"""

        ## (start_X, start_Y, width, height)
        upper_border = (150 - self.BORDER_SIZE, 50 - self.BORDER_SIZE, \
                        self.BOARD_SIZE + 2 * self.BORDER_SIZE, self.BORDER_SIZE)
        right_border = (self.SCREEN_SIZE[0] - 150, 50 - self.BORDER_SIZE, \
                        self.BORDER_SIZE, self.BOARD_SIZE + 2 * self.BORDER_SIZE)
        lower_border = (150 - self.BORDER_SIZE, self.SCREEN_SIZE[1] - 50, \
                        self.BOARD_SIZE + 2 * self.BORDER_SIZE, self.BORDER_SIZE)
        left_border = (150 - self.BORDER_SIZE, 50 - self.BORDER_SIZE, \
                       self.BORDER_SIZE, self.BOARD_SIZE + 2 * self.BORDER_SIZE)

        horizontal_lines_start_X = 150
        horizontal_lines_start_Y = 100
        horizontal_lines_end_X = 700 - 150
        horizontal_lines_end_Y = 100

        vertical_lines_start_X = 200
        vertical_lines_start_Y = 50
        vertical_lines_end_X = 200
        vertical_lines_end_Y = 500 - 50

        while True:
            self.game_display.fill(self.BACKGROUND_COLOR)

            my_line_start_X = horizontal_lines_start_X
            my_line_start_Y = horizontal_lines_start_Y
            my_line_end_X = horizontal_lines_end_X
            my_line_end_Y = horizontal_lines_end_Y

            for i in range(common.SIDE_LEN - 1):
                pygame.draw.line(self.game_display, self.BLACK_COLOR, \
                                 (my_line_start_X, my_line_start_Y), (my_line_end_X, my_line_end_Y), 2)
                my_line_start_Y += self.CELL_SIZE
                my_line_end_Y += self.CELL_SIZE

            my_line_start_X = vertical_lines_start_X
            my_line_start_Y = vertical_lines_start_Y
            my_line_end_X = vertical_lines_end_X
            my_line_end_Y = vertical_lines_end_Y

            for i in range(common.SIDE_LEN - 1):
                pygame.draw.line(self.game_display, self.BLACK_COLOR, \
                                 (my_line_start_X, my_line_start_Y), (my_line_end_X, my_line_end_Y), 2)
                my_line_start_X += self.CELL_SIZE
                my_line_end_X += self.CELL_SIZE

            pygame.draw.rect(self.game_display, self.BORDER_COLOR, upper_border)
            pygame.draw.rect(self.game_display, self.BORDER_COLOR, right_border)
            pygame.draw.rect(self.game_display, self.BORDER_COLOR, lower_border)
            pygame.draw.rect(self.game_display, self.BORDER_COLOR, left_border)

            for i in range(common.SIDE_LEN):
                for j in range(common.SIDE_LEN):
                    if grid[i][j] == common.EMPTY_CELL:
                        continue
                    circle_color = self.BLACK_COLOR
                    if grid[i][j] == common.WHITE_CELL:
                        circle_color = self.WHITE_COLOR
                    pos_X = 150 + self.CELL_SIZE * i + self.CELL_SIZE / 2
                    pos_Y = 50 + self.CELL_SIZE * j + self.CELL_SIZE / 2
                    pygame.draw.circle(self.game_display, circle_color, (pos_X, pos_Y), 20)

            exit_game_clicked = self.add_button("Exit", 585, 400, 100, 50, \
                                                self.BUTTON_INACTIVE_COLOR, self.BUTTON_ACTIVE_COLOR)

            if exit_game_clicked == True:
                pygame.quit()
                quit()

            clicked_cell = self.get_pressed_cell()

            if clicked_cell[0] != -1 and clicked_cell[1] != -1:
                return clicked_cell

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            pygame.display.update()

            if need_click == False:
                break
