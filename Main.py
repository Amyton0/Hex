import pygame
import math
import sys
import random
import pickle
import os.path


class Hex:
    def __init__(self, x, y, side_length, coordinates_on_field):
        self.coordinates = hex_coords(x, y, side_length)
        self.center = (x - side_length / 2, y + math.sqrt(3) / 2 * side_length)
        self.side_length = side_length
        self.neighbours = []
        self.color = None
        self.coordinates_on_field = coordinates_on_field

    def draw(self):
        if self.color:
            pygame.draw.polygon(screen, self.color, self.coordinates)
        pygame.draw.polygon(screen, (0, 0, 0), self.coordinates, 1)

    def set_color(self, color):
        if self.color is None:
            self.color = color

    def add_neighbour(self, neighbour):
        if neighbour not in self.neighbours:
            self.neighbours.append(neighbour)
            neighbour.add_neighbour(self)

    def get_start_x_coord(self):
        return self.coordinates[0][0]

    def get_start_y_coord(self):
        return self.coordinates[0][1]

    def is_path(self):
        color = self.color
        self.color = None
        if color == 'red' and self.coordinates_on_field[0] == game.field_size - 1:
            return True
        elif color == 'blue' and self.coordinates_on_field[1] == game.field_size - 1:
            return True
        else:
            for neighbour in self.neighbours:
                if neighbour.color == color:
                    if neighbour.is_path():
                        return True
        return False


class Game:
    def __init__(self):
        self.player_color = 'red'
        self.computer_color = 'blue'

        self.color1 = 'blue'
        self.color2 = 'red'
        self.chosen_color = self.color1

        self.records_i = 0

        self.mode = EASY
        self.status = START

        self.number_of_steps = 0

        self.is_computer_turn = False

        self.is_left_wall = False
        self.is_right_wall = False

        self.field_size = 0

        self.records = {}
        self.sizes = None
        self.winning_text = ''

    def reset(self):
        self.records_i = 0
        self.number_of_steps = 0
        self.is_computer_turn = False
        self.field_size = 0
        self.sizes = None
        self.is_left_wall = False
        self.is_right_wall = False


def is_button(button_coordinates, event_pos):
    if button_coordinates[0] < event_pos[0] < button_coordinates[0] + button_coordinates[2]:
        if button_coordinates[1] < event_pos[1] < button_coordinates[1] + button_coordinates[3]:
            return True
    return False


def do_field(n, start_x, start_y, side_length):
    field = []

    for i in range(n):
        if len(field) == 0:
            field.append([Hex(start_x, start_y, side_length, (0, 0))])
        else:
            hex = Hex(field[-1][0].get_start_x_coord() + 3 * side_length / 2,
                      field[-1][0].get_start_y_coord() - side_length * math.sqrt(3) / 2,
                      side_length, (i, 0))
            field.append([hex])
            hex.add_neighbour(field[-2][0])
            hex.add_neighbour(field[-2][1])

        for j in range(n - 1):
            hex = Hex(field[-1][-1].get_start_x_coord() + 3 * side_length / 2,
                      field[-1][-1].get_start_y_coord() + side_length * math.sqrt(3) / 2,
                      side_length, (i, j + 1))
            field[-1].append(hex)
            hex.add_neighbour(field[-1][-2])
            if i != 0:
                hex.add_neighbour(field[-2][j + 1])
                if j + 2 < n:
                    hex.add_neighbour(field[-2][j + 2])

    return field


def find_coordinates(field, target_hex):
    for x in range(len(field)):
        for y in range(len(field[x])):
            if field[x][y] == target_hex:
                return (x, y)
    return None


def draw_field(field):
    for row in field:
        for hex in row:
            hex.draw()
    length = field[0][0].side_length
    corner1 = (field[0][0].coordinates[4][0] - 3 * length / 2, field[0][0].coordinates[4][1])
    corner2 = (field[0][-1].coordinates[2][0] - length / 2, field[0][-1].coordinates[2][1] + length / 2)
    corner3 = (field[-1][-1].coordinates[1][0] + 3 * length / 2, field[0][0].coordinates[4][1])
    corner4 = (field[-1][0].coordinates[0][0] - length / 2, field[-1][0].coordinates[0][1] - length / 2)
    pygame.draw.line(screen, 'red', corner1, corner2, 5)
    pygame.draw.line(screen, 'blue', corner2, corner3, 5)
    pygame.draw.line(screen, 'red', corner3, corner4, 5)
    pygame.draw.line(screen, 'blue', corner4, corner1, 5)


def hex_coords(x, y, l):
    sqrt3 = math.sqrt(3)
    return [(x, y), (x + l / 2, y + l * sqrt3 / 2), (x, y + l * sqrt3),
            (x - l, y + l * sqrt3), (x - 3 * l / 2, y + l * sqrt3 / 2), (x - l, y)]


def hex_containing_point(field, point):
    for row in field:
        for hex in row:
            if is_point_in_hex(point[0] - hex.center[0], point[1] - hex.center[1], hex.side_length):
                return hex
    return None


def is_point_in_hex(x, y, side_size):
    side_size_sqrt3 = side_size * math.sqrt(3)
    return (-1) * side_size_sqrt3 / 2 <= y <= side_size_sqrt3 / 2 and \
           (-1) * side_size_sqrt3 <= (-1) * math.sqrt(3) * x + y <= side_size_sqrt3 and \
           (-1) * side_size_sqrt3 <= math.sqrt(3) * x + y <= side_size_sqrt3


def is_game_finished(field, color):
    field_copy = do_field(game.field_size, 400 - 14.5 * game.hex_size, 300 - game.hex_size / 2, game.hex_size)
    for i in range(game.field_size):
        for j in range(game.field_size):
            field_copy[i][j].color = field[i][j].color
    if color == 'blue':
        for row in field_copy:
            hex = row[0]
            if hex.color == color:
                if hex.is_path():
                    return True
    if color == 'red':
        for hex in field_copy[0]:
            if hex.color == color:
                if hex.is_path():
                    return True
    return False


def get_copy_field(field):
    copy_field = [row[:] for row in field]
    for x in range(len(field)):
        for y in range(len(field)):
            copy_field[x][y] = field[x][y]
    return copy_field


def is_win_turn():
    for x in range(game.field_size):
        for y in range(game.field_size):
            copy_field = get_copy_field(game.field)
            if copy_field[x][y].color is None:
                copy_field[x][y].set_color(game.computer_color)
                if is_game_finished(copy_field, game.computer_color):
                    copy_field[x][y].color = None
                    return (x, y)
                copy_field[x][y].color = game.player_color
                if is_game_finished(copy_field, game.player_color):
                    copy_field[x][y].color = None
                    return (x, y)
                copy_field[x][y].color = None
    (x, y) = (-1, -1)
    return (x, y)
'''
def is_player_can_win():
    if game.computer_color == 'blue':
        for i in range(game.field_size):
            if game.field[i][game.field_size-2].color == game.player_color:
                return (i+1, game.field_size)
            if game.field[i][2].color == game.player_color:
                return (i, 0)
    else:
        for i in range(game.field_size):
            if game.field[i][game.field_size-2].color == game.player_color:
                return (i,game.field_size)
            if game.field[i][2].color == game.player_color:
                return (i,0)
    return (-1, -1)
'''

def find_closer(line):
    if game.computer_color == 'red':
        closer_left = (-1, -1)
        closer_right = (game.field_size, game.field_size)
        for i in line:
            if i[0]<closer_left[0]:
                closer_left = i
            if i[0]>closer_right[0]:
                closer_right = i
        return closer_left, closer_right
def do_line(field, computer_color, line):
    try:
        if line is not None:
            if computer_color == 'red':
                closer_left, closer_right = find_closer(line)
                if field[closer_left[0] - 1][closer_left[1]].neighbours is None and game.is_left_wall == False:
                    return (closer_left[0] - 1, closer_left[1])
#проверять левого соседа
                if field[closer_right[0] + 1][closer_right[1]].color is None and game.is_right_wall == False:
                    return (closer_right[0] + 1, closer_right[1])


                if field[closer_right[0] - 1][closer_right[1] - 1].color is None:
                    return (closer_right[0] + 1, closer_right[1] - 1)


                if field[closer_right[0] - 1][closer_right[1] + 1].color is None:
                    return (closer_right[0] + 1, closer_right[1] + 1)

                if field[closer_right[0] + 1][closer_right[1] - 1].color is None:
                    return (closer_right[0] + 1, closer_right[1] - 1)

                for i in reversed(line):
                        if field[i[0] + 1][i[1] + 1].color is None:
                            return (i[0] + 1, i[1] + 1)

            if computer_color == 'blue':
                for i in reversed(line):

                        if field[i[0]][i[1] - 1].color is None:
                            return (i[0], i[1] - 1)

                for i in reversed(line):

                        if field[i[0]][i[1] + 1].color is None:
                            return (i[0], i[1] + 1)

                for i in reversed(line):

                        if field[i[0] - 1][i[1] - 1].color is None:
                            return (i[0] - 1, i[1] - 1)

                for i in reversed(line):

                        if field[i[0] - 1][i[1] + 1].color is None:
                            return (i[0] - 1, i[1] + 1)

                for i in reversed(line):

                        if field[i[0] + 1][i[1] - 1].color is None:
                            return (i[0] + 1, i[1] - 1)

                for i in reversed(line):

                        if field[i[0] + 1][i[1] + 1].color is None:
                            return (i[0] + 1, i[1] + 1)
    except IndexError:
        return (-1, -1)
    return (-1, -1)


def random_coordinates(field):
    size = len(field)
    random_x, random_y = random.randint(0, size - 1), random.randint(0, size - 1)
    while field[random_x][random_y].color is not None:
        random_x, random_y = random.randint(0, size - 1), random.randint(0, size - 1)

    return random_x, random_y


def random_move(field, color):
    x, y = random_coordinates(field)
    field[x][y].set_color(color)


def change_color(player_color, color1, color2):
    if player_color == color1:
        return color2
    else:
        return color1


def get_winning_text(current_color, mode, player_color, color1):
    if mode != HOTSEAT:
        if current_color == player_color:
            return 'Вы победили!'
        return 'Вы проиграли'
    if current_color == color1:
        return 'Победил игрок 1'
    return 'Победил игрок 2'


def generate_text(font, text, color):
    return font.render(text, True, color)


def generate_records_text(sizes):
    text = []
    are_records = False

    if not sizes:
        sizes = game.records.keys()
    for size in sizes:
        text.append('Поле размера ' + str(size))
        for mode in game.records[size]:
            if len(game.records[size][mode]) != 0:
                if mode == EASY:
                    text.append('    ' + 'Лёгкий')
                elif mode == HARD:
                    text.append('    ' + 'Сложный')
                else:
                    text.append('    ' + '2 игрока')
                text.append('        Лучший результат — ' + str(min(game.records[size][mode])))
                are_records = True
    if are_records:
        return text
    else:
        return None


def save_game():
    with open("savegame.dat", "wb") as file:
        pickle.dump(game, file)


def load_game():
    if os.path.exists("savegame.dat"):
        with open("savegame.dat", "rb") as file:
            loaded_game = pickle.load(file)
            return loaded_game
    else:
        return Game()


pygame.init()

display_size = (800, 600)
screen = pygame.display.set_mode(display_size)

screen.fill((255, 255, 255))

START = 0
CHOOSING_MODE = 1
CHOOSING_COLOR = 2
CHOOSING_QUEUE = 3
CHOOSING_SIZE = 4
GAME = 5
END = 6
RECORDS = 7

EASY = 0
HARD = 1
HOTSEAT = 2

BLUE = (64, 128, 255)
WHITE = (250, 250, 250)

font1 = pygame.font.Font(None, 200)
font2 = pygame.font.Font(None, 90)
font3 = pygame.font.Font(None, 70)
font4 = pygame.font.Font(None, 40)
font5 = pygame.font.Font(None, 20)

number_of_records = 10

first_record_coordinates = (100, 100)

start_button_coordinates = (270, 310, 250, 100)
records_button_coordinates = (270, 450, 250, 100)
corner_button_coordinates = (650, 5, 145, 50)

button12_coordinates = (50, 310, 300, 100)
button22_coordinates = (450, 310, 300, 100)

button13_coordinates = (50, 310, 200, 100)
button23_coordinates = (300, 310, 200, 100)
button33_coordinates = (550, 310, 200, 100)

last_coord = (0, 0)
line = []

game = load_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_game()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.status == START:
                if is_button(start_button_coordinates, event.pos):
                    game.status = CHOOSING_MODE
                if is_button(records_button_coordinates, event.pos):
                    game.status = RECORDS

            elif game.status == CHOOSING_MODE:
                is_button1 = is_button(button13_coordinates, event.pos)
                is_button2 = is_button(button23_coordinates, event.pos)
                is_button3 = is_button(button33_coordinates, event.pos)
                if is_button1 or is_button2 or is_button3:
                    if is_button1:
                        game.mode = EASY
                    if is_button2:
                        game.mode = HARD
                    if is_button3:
                        game.mode = HOTSEAT
                    game.status = CHOOSING_COLOR

            elif game.status == CHOOSING_COLOR:
                is_button1 = is_button(button12_coordinates, event.pos)
                is_button2 = is_button(button22_coordinates, event.pos)
                if is_button1 or is_button2:
                    if is_button1:
                        if game.mode == HOTSEAT:
                            game.chosen_color = 'blue'
                        else:
                            game.player_color = 'blue'
                            game.computer_color = 'red'
                    if is_button2:
                        if game.mode == HOTSEAT:
                            game.chosen_color = 'red'
                        else:
                            game.player_color = 'red'
                            game.computer_color = 'blue'
                    game.status = CHOOSING_QUEUE

            elif game.status == CHOOSING_QUEUE:
                is_button1 = is_button(button12_coordinates, event.pos)
                is_button2 = is_button(button22_coordinates, event.pos)
                if is_button1 or is_button2:
                    if is_button1:
                        if game.mode == EASY or game.mode == HARD:
                            game.color1 = game.player_color
                            game.color2 = game.computer_color
                            game.is_computer_turn = False
                        else:
                            game.player_color = game.chosen_color
                    if is_button2:
                        if game.mode == EASY or game.mode == HARD:
                            game.color1 = game.computer_color
                            game.color2 = game.player_color
                            game.is_computer_turn = True
                        else:
                            game.player_color = change_color(game.chosen_color, 'red', 'blue')
                    game.status = CHOOSING_SIZE

            elif game.status == GAME:
                current_hex = hex_containing_point(game.field, event.pos)
                if current_hex:
                    if current_hex.color is None and not game.is_computer_turn:
                        current_hex.set_color(game.player_color)
                        if game.mode == EASY or game.mode == HARD:
                            game.is_computer_turn = True
                        if game.mode == HOTSEAT:
                            game.player_color = change_color(game.player_color, game.color1, game.color2)
                        game.number_of_steps += 1

            elif game.status == END:
                if (270, 310) < event.pos < (530, 410):
                    game.status = START
                    game.reset()
                if is_button(corner_button_coordinates, event.pos):
                    game.sizes = [game.field_size]
                    game.status = RECORDS

            elif game.status == RECORDS:
                if is_button(corner_button_coordinates, event.pos):
                    game.status = START
                    game.reset()

                if event.button == 4:
                    if game.records_i > 0:
                        game.records_i -= 1
                if event.button == 5:
                    text = generate_records_text(game.sizes)
                    if text:
                        if game.records_i < len(text) - number_of_records:
                            game.records_i += 1

        if event.type == pygame.KEYDOWN:
            if game.status == CHOOSING_SIZE:
                if event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6,
                                 pygame.K_7, pygame.K_8, pygame.K_9]:
                    game.field_size = game.field_size * 10 + int(pygame.key.name(event.key))
                    pygame.display.flip()
                else:
                    game.length_hexes_in_row = game.field_size * 2 + (game.field_size - 1)
                    game.hex_size = display_size[0] / (game.length_hexes_in_row + (game.field_size + 7) // 2)
                    game.field = do_field(game.field_size, display_size[0] / 2 -
                                          (game.length_hexes_in_row / 2 - 1.5) * game.hex_size,
                                          display_size[1] / 2 - game.hex_size * math.sqrt(3) / 2, game.hex_size)
                    game.status = GAME

    screen.fill((255, 255, 255))

    if game.status == START:
        pygame.draw.rect(screen, BLUE, (20, 70, 760, 150))
        pygame.draw.rect(screen, BLUE, start_button_coordinates)
        pygame.draw.rect(screen, BLUE, records_button_coordinates)
        screen.blit(generate_text(font1, "HEX", WHITE), (260, 80))
        screen.blit(generate_text(font2, "Старт", WHITE), (305, 330))
        screen.blit(generate_text(font3, "Рекорды", WHITE), (285, 475))

    elif game.status == CHOOSING_MODE:
        pygame.draw.rect(screen, BLUE, (20, 70, 760, 150))
        screen.blit(generate_text(font2, "Выберите режим:", WHITE), (120, 110))
        pygame.draw.rect(screen, BLUE, button13_coordinates)
        screen.blit(generate_text(font2, "EASY", WHITE), (60, 340))
        pygame.draw.rect(screen, BLUE, button23_coordinates)
        screen.blit(generate_text(font2, "HARD", WHITE), (310, 340))
        pygame.draw.rect(screen, BLUE, button33_coordinates)
        screen.blit(generate_text(font2, "2 PL", WHITE), (580, 340))

    elif game.status == CHOOSING_COLOR:
        pygame.draw.rect(screen, BLUE, (20, 70, 760, 150))
        screen.blit(generate_text(font2, "Выберите цвет:", WHITE), (160, 110))
        pygame.draw.rect(screen, BLUE, button12_coordinates)
        screen.blit(generate_text(font2, "Синий", WHITE), (80, 340))
        pygame.draw.rect(screen, BLUE, button22_coordinates)
        screen.blit(generate_text(font2, "Красный", WHITE), (470, 340))

    elif game.status == CHOOSING_QUEUE:
        pygame.draw.rect(screen, BLUE, (20, 70, 760, 150))
        screen.blit(generate_text(font2, "Ходить:", WHITE), (300, 110))
        pygame.draw.rect(screen, BLUE, button12_coordinates)
        screen.blit(generate_text(font2, "Первым", WHITE), (80, 340))
        pygame.draw.rect(screen, BLUE, button22_coordinates)
        screen.blit(generate_text(font2, "Вторым", WHITE), (470, 340))

    elif game.status == CHOOSING_SIZE:
        pygame.draw.rect(screen, BLUE, (20, 70, 760, 150))
        screen.blit(generate_text(font2, "Введите размер поля:", WHITE), (50, 110))
        if game.field_size != 0:
            text = font2.render(str(game.field_size), True, (0, 0, 0))
            screen.blit(text, (350, 300))

    elif game.status == GAME:
        draw_field(game.field)
        screen.blit(generate_text(font2, str(game.number_of_steps), BLUE), (720, 10))
        pygame.display.flip()
        if is_game_finished(game.field, game.color1):
            pygame.time.delay(400)
            game.winning_text = get_winning_text(game.color1, game.mode, game.player_color, game.color1)
            game.status = END
        if is_game_finished(game.field, game.color2):
            pygame.time.delay(400)
            game.winning_text = get_winning_text(game.color2, game.mode, game.player_color, game.color1)
            game.status = END
        if game.is_computer_turn and game.status != END and game.mode == EASY:
            pygame.time.delay(450)
            random_move(game.field, game.computer_color)
            game.is_computer_turn = False

        if game.is_computer_turn and game.status != END and game.mode == HARD:
            pygame.time.delay(450)
            coord = is_win_turn()
            coord1 = do_line(game.field, game.computer_color, line)
            if coord != (-1, -1):
                game.field[coord[0]][coord[1]].set_color(game.computer_color)
                if game.computer_color == 'red':
                    if coord[0] == 0:
                        game.is_left_wall = True
                    if coord[0] == game.field_size:
                        game.is_right_wall = True
                if game.computer_color == 'blue':
                    if coord[1] == 0:
                        game.is_left_wall = True
                    if coord[1] == game.field_size:
                        game.is_right_wall = True
                if coord[0] == 0 or coord[1] == 0 or coord[0] == game.field_size or coord[1] == game.field_size:
                    game.is_wall = True
                line.append(coord)
            elif coord1 != (-1, -1):
                game.field[coord1[0]][coord1[1]].set_color(game.computer_color)
                if game.computer_color == 'red':
                    if coord1[0] == 0:
                        game.is_left_wall = True
                    if coord1[0] == game.field_size:
                        game.is_right_wall = True
                if game.computer_color == 'blue':
                    if coord1[1] == 0:
                        game.is_left_wall = True
                    if coord1[1] == game.field_size:
                        game.is_right_wall = True
                line.append(coord1)
            else:
                last_coord = random_coordinates(game.field)
                if game.computer_color == 'red':
                    if last_coord[0] == 0:
                        game.is_left_wall = True
                    if last_coord[0] == game.field_size:
                        game.is_right_wall = True
                if game.computer_color == 'blue':
                    if last_coord[1] == 0:
                        game.is_left_wall = True
                    if last_coord[1] == game.field_size:
                        game.is_right_wall = True
                line.append(last_coord)
                if game.field[game.field_size//2][game.field_size//2].color is None:
                    last_coord = (game.field_size // 2, game.field_size // 2)
                game.is_left_wall = False
                game.is_right_wall = False
                game.field[last_coord[0]][last_coord[1]].set_color(game.computer_color)
            game.is_computer_turn = False

    elif game.status == END:
        if game.is_computer_turn or game.mode == HOTSEAT:
            if game.field_size in game.records:
                if game.mode in game.records[game.field_size]:
                    game.records[game.field_size][game.mode].append(game.number_of_steps)
                else:
                    game.records[game.field_size][game.mode] = [game.number_of_steps]
            else:
                game.records[game.field_size] = {}
                game.records[game.field_size][game.mode] = [game.number_of_steps]
            game.records[game.field_size][game.mode].sort()

        end_text = font2.render(game.winning_text, True, BLUE)

        screen.blit(end_text, (190, 220))
        pygame.draw.rect(screen, BLUE, (270, 310, 300, 100))
        screen.blit(generate_text(font2, "Ещё раз!", WHITE), (285, 330))

        pygame.draw.rect(screen, BLUE, corner_button_coordinates)
        screen.blit(generate_text(font4, "Рекорды", WHITE), (660, 15))

    elif game.status == RECORDS:
        text = generate_records_text(game.sizes)
        if text:
            for i in range(number_of_records):
                if game.records_i + i >= len(text):
                    break
                screen.blit(generate_text(font4, text[game.records_i + i], BLUE),
                            (first_record_coordinates[0], first_record_coordinates[1] + i * 40))
        else:
            screen.blit(generate_text(font4, 'Рекордов пока нет', BLUE), first_record_coordinates)

        pygame.draw.rect(screen, BLUE, corner_button_coordinates)
        screen.blit(generate_text(font4, "Назад", WHITE), (665, 15))

    pygame.display.flip()
