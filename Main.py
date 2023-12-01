import pygame
import math
import sys
import random


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
        if color == 'red' and self.coordinates_on_field[0] == field_size - 1:
            return True
        elif color == 'blue' and self.coordinates_on_field[1] == field_size - 1:
            return True
        else:
            for neighbour in self.neighbours:
                if neighbour.color == color:
                    if neighbour.is_path():
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
    field_copy = do_field(field_size, 400 - 14.5 * hex_size, 300 - hex_size / 2, hex_size)
    for i in range(field_size):
        for j in range(field_size):
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


def winning_text(current_color, mode, player_color, color1):
    if mode != HOTSEAT:
        if current_color == player_color:
            return 'Вы победили!'
        return 'Вы проиграли'
    if current_color == color1:
        return 'Победил игрок 1'
    return 'Победил игрок 2'


pygame.init()

display_size = (800, 600)
screen = pygame.display.set_mode(display_size)

screen.fill((255, 255, 255))

field_size = 11
length_hexes_in_row = field_size * 2 + (field_size - 1)
hex_size = display_size[0] / (length_hexes_in_row + (field_size + 7) // 2)

START = 0
CHOOSING = 1
GAME = 2
END = 3

EASY = 0
HARD = 1
HOTSEAT = 2

player_color = 'red'
computer_color = 'blue'

color1 = 'blue'
color2 = 'red'

status = GAME
mode = EASY

is_computer_turn = False

field = do_field(field_size, display_size[0] / 2 - (length_hexes_in_row / 2 - 1.5) * hex_size,
                 display_size[1] / 2 - hex_size * math.sqrt(3) / 2, hex_size)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if status == GAME:
                hex = hex_containing_point(field, event.pos)
                if hex:
                    if hex.color is None and not is_computer_turn:
                        hex.set_color(player_color)
                        if mode == EASY or mode == HARD:
                            is_computer_turn = True
                        if mode == HOTSEAT:
                            player_color = change_color(player_color, color1, color2)

    if status == GAME:
        draw_field(field)
        pygame.display.flip()
        if is_game_finished(field, color1):
            winning_text = winning_text(color1, mode, player_color, color1)
            status = END
        if is_game_finished(field, color2):
            winning_text = winning_text(color2, mode, player_color, color1)
            status = END
        if is_computer_turn and status != END and mode == EASY:
            pygame.time.delay(450)
            random_move(field, computer_color)
            is_computer_turn = False
    if status == END:
        if winning_text:
            print(winning_text)
            winning_text = ''

    pygame.display.flip()
