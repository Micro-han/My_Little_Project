import pygame
import sys
import numpy
import interface2

color_light = (202, 203, 213 )
color_dark = (2, 6, 145)
def SixPlayers():
    pygame.init()
    matrix = numpy.ones((17, 25))
    matrix *= -1

    first_player = [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]]   #red
    second_player = [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]]    #yellow
    third_player = [[12, 18], [12, 20], [12, 22], [12, 24], [11, 19], [11, 21], [11, 23], [10, 20], [10, 22], [9, 21]] #orange
    forth_player = [[16, 12], [15, 11], [15, 13], [14, 10], [14, 12], [14, 14], [13, 9], [13, 11], [13, 13], [13, 15]] #green
    fifth_player = [[12, 0], [12, 2], [12, 4], [12, 6], [11, 1], [11, 3], [11, 5], [10, 2], [10, 4], [9, 3]]   #pink
    sixth_player = [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]]   #blue
    move_index = [[-1, -1], [-1, 1], [0, 2], [1, 1], [1, -1], [0, -2]]

    matrix_index = [1, 2, 3, 4, 13, 12, 11, 10, 9]
    for i in range(9):
        j = 12
        first_time = True
        while matrix_index[i] > 0:
            if (i % 2 == 0) and first_time:
                first_time = False
                # print(i,j)
                matrix[i][j] = matrix[16 - i][j] = 0

                matrix_index[i] -= 1
            else:
                j -= 1
                matrix[i][j] = matrix[i][24 - j] = matrix[16 - i][j] = matrix[16 - i][24 - j] = 0
                matrix_index[i] -= 2
            j -= 1

    def add_player(index):
        if index == 1:
            for i in range(len(first_player)):
                matrix[first_player[i][0]][first_player[i][1]] = index
        if index == 2:
            for i in range(len(second_player)):
                matrix[second_player[i][0]][second_player[i][1]] = index
        if index == 3:
            for i in range(len(third_player)):
                matrix[third_player[i][0]][third_player[i][1]] = index
        if index == 4:
            for i in range(len(forth_player)):
                matrix[forth_player[i][0]][forth_player[i][1]] = index
        if index == 5:
            for i in range(len(fifth_player)):
                matrix[fifth_player[i][0]][fifth_player[i][1]] = index
        if index == 6:
            for i in range(len(sixth_player)):
                matrix[sixth_player[i][0]][sixth_player[i][1]] = index

    class remplissage:
        def __init__(self):
            self_x = 0
            self_y = 0

        def pion(self):
            colors = [(240, 230, 230), "red", "yellow", "orange", "green", "pink", "blue"]
            for i in range(0, 17):
                for j in range(0, 25):
                    if matrix[i][j] >= 0:
                        rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pions_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))

    def valid_moves(coor):
        valid_index = []
        for i in range(len(move_index)):

            x = coor[0] + move_index[i][0]
            y = coor[1] + move_index[i][1]
            if -1 < x < 17 and -1 < y < 25:
                if matrix[x][y] == 0:
                    valid_index.append([x, y])
                elif matrix[x][y] != -1:
                    check_path(move_index[i], x, y, valid_index)

        return valid_index

    def check_path(path_coor, x, y, moves_array):
        # print('before:', x, y)
        x2 = x + path_coor[0]
        y2 = y + path_coor[1]
        if [x2, y2] not in moves_array:
            if -1 < x2 < 17 and -1 < y2 < 25:
                if matrix[x2][y2] == 0:
                    moves_array.append([x2, y2])
                    for j in range(len(move_index)):
                        x3 = x2 + move_index[j][0]
                        y3 = y2 + move_index[j][1]
                        if [x3, y3] not in moves_array:
                            if -1 < x3 < 17 and -1 < y3 < 25:
                                if matrix[x3][y3] > 0:
                                    check_path(move_index[j], x3, y3, moves_array)

    def move(pos, target):
        matrix[target[0]][target[1]] = matrix[pos[0]][pos[1]]
        matrix[pos[0]][pos[1]] = 0

    def get_token_coor(x, y):
            grid_width = 0
            grid_heigth = 0
            coor = [int((y - grid_heigth) / 20), int((x - grid_width) / 20)]
            return coor

    def animation(moves=[], clicked_token=None):
            colors = [(240, 230, 230), "red", "yellow", "orange", "green", "pink", "blue"]
            moves.append(clicked_token)
            for i in range(0, 17):
                for j in range(0, 25):
                    if matrix[i][j] >= 0:
                        rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        pions_rect.append(pygame.draw.rect(screen, colors[int(matrix[i][j])], rect, border_radius=20))
                    if [i, j] in moves:
                        test_cercle = pygame.image.load('imgs/cercle.png')
                        test_cercle = pygame.transform.scale(test_cercle, (CELL_SIZE, CELL_SIZE))
                        screen.blit(test_cercle, (j * CELL_SIZE, i * CELL_SIZE))

    def show_grille():
            for i in range(0, nb_col):
                for j in range(0, nb_ligne):
                    rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(screen, pygame.Color("white"), rect, width=1)

    def WriteText(text, text_pos_x, text_pos_y, text_size, col):
            text_font = pygame.font.SysFont(None, text_size)
            text_render = text_font.render(text, True, col)
            screen.blit(text_render, (text_pos_x, text_pos_y))

    def winner():
        first = True
        second = True
        third = True
        fourth = True
        fifth = True
        sixth = True
        for i in range(len(first_player)):
            if matrix[first_player[i][0]][first_player[i][1]] != 4:
                fourth = False
                break
        for i in range(len(forth_player)):
            if matrix[forth_player[i][0]][forth_player[i][1]] != 1:
                first = False
                break
        for i in range(len(second_player)):
            if matrix[second_player[i][0]][second_player[i][1]] != 5:
                fifth = False
                break
        for i in range(len(fifth_player)):
            if matrix[fifth_player[i][0]][fifth_player[i][1]] != 2:
                second = False
                break
        for i in range(len(third_player)):
            if matrix[third_player[i][0]][third_player[i][1]] != 6:
                sixth = False
                break
        for i in range(len(sixth_player)):
            if matrix[sixth_player[i][0]][sixth_player[i][1]] != 3:
                third = False
                break
        if fourth == True:
            WriteText('Player 4 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'green')
            return True
        elif (first == True):
            WriteText('Player 1 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'red')
            return True
        elif (fifth == True):
            WriteText('Player 5 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'pink')
            return True
        elif (second == True):
            WriteText('Player 2 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'yellow')
            return True
        elif (sixth == True):
            WriteText('Player 6 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'blue')
            return True
        elif (third == True):
            WriteText('Player 3 had won!', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100, 50, 'orange')
            return True
        else:
            return False


    add_player(1)
    add_player(2)
    add_player(3)
    add_player(4)
    add_player(5)
    add_player(6)

    nb_col = 25
    nb_ligne = 25
    CELL_SIZE = 20
    screen = pygame.display.set_mode(size=(nb_col * CELL_SIZE, nb_ligne * CELL_SIZE))
    timer = pygame.time.Clock()
    game_on = True
    pions_rect = []


    players = remplissage()


    screen.fill(pygame.Color("white"))
    players.pion()
    player_index = 1
    is_selecting = False
    player_valid_moves = []
    last_selected_token = []

    def text_objects(text, font):
        textsurface = font.render(text, True, "white")
        return textsurface, textsurface.get_rect()

    def button(msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))

            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))
        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(textSurf, textRect)
    while game_on:
        # player turn
        if player_index == 1: col = 'red'
        if player_index == 2: col = 'yellow'
        if player_index == 3: col = 'orange'
        if player_index == 4: col = 'green'
        if player_index == 5: col = 'pink'
        if player_index == 6: col = 'blue'
        # player turn
        if (winner() == False):
            WriteText('Player ' + str(player_index) + '\'s Turn', nb_col * CELL_SIZE - 370, nb_ligne * CELL_SIZE - 100,
                      50, col)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # get a list of all sprites that are under the mouse cursor
                clicked_sprites = [s for s in pions_rect if s.collidepoint(pos)]

                if clicked_sprites:
                    clicked_token = get_token_coor(clicked_sprites[0].x, clicked_sprites[0].y)
                    if matrix[clicked_token[0], clicked_token[1]] == player_index:
                        if clicked_token == last_selected_token:
                            is_selecting = False
                            last_selected_token = []
                            player_valid_moves = []
                            screen.fill(pygame.Color("white"))
                            animation()
                        else:
                            player_valid_moves = valid_moves(clicked_token)
                            last_selected_token = clicked_token
                            is_selecting = True
                            screen.fill(pygame.Color("white"))
                            animation(player_valid_moves,last_selected_token)
                    elif clicked_token in player_valid_moves:
                        move(last_selected_token, clicked_token)
                        winner()
                        is_selecting = False
                        last_selected_token = []
                        player_valid_moves = []
                        screen.fill(pygame.Color("white"))
                        player_index = (player_index+1) % 7
                        if player_index == 0:
                            player_index += 1


                        animation()


            button("back", 400, 430, 70, 30, color_dark, color_light, interface2.window2)
            rect2 = pygame.draw.rect(screen, color_dark, pygame.Rect(394, 424, 82, 42), 6, 20)



        pygame.display.update()
        timer.tick(60)
