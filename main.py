import sys
import random
import time

import pygame
from pprint import pprint


class Button:
    def __init__(self, x, y, width, height, text, color_button, color_font, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color_button = color_button
        self.color_font = color_font
        self.size = (width, height)
        self.font = font

    def draw(self, screen):
        pygame.draw.rect(screen,
                         self.color_button,
                         (self.x, self.y, *self.size), 1)
        text = self.font.render(self.text, True, self.color_font)
        rect = text.get_rect()
        rect.center = (int(self.x + self.width / 2), int(self.y + self.height / 2))
        screen.blit(text, rect)

    def is_clicked(self, mouse_x, mouse_y):
        return self.x < mouse_x < self.x + self.width \
               and self.y < mouse_y < self.y + self.height

    def __str__(self):
        return self.text


class Tetris:
    def __init__(self):
        self.FPS = 25

        self.WIDTH = 600
        self.HEIGHT = 500
        self.size = self.WIDTH, self.HEIGHT

        self.BLOCK = 20

        self.CUP_WIDTH = 10
        self.CUP_HEIGHT = 20
        self.CUP_X = self.WIDTH // 2 - (self.CUP_WIDTH // 2) * self.BLOCK
        self.CUP_Y = 50

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        self.colors = [self.GREEN, self.BLUE, self.RED, self.YELLOW]

        self.figures = {'S': [['     ',
                               '     ',
                               '  xx ',
                               ' xx  ',
                               '     '],
                              ['     ',
                               '  x  ',
                               '  xx ',
                               '   x ',
                               '     ']],
                        'Z': [['     ',
                               '     ',
                               ' xx  ',
                               '  xx ',
                               '     '],
                              ['     ',
                               '  x  ',
                               ' xx  ',
                               ' x   ',
                               '     ']],
                        'J': [['     ',
                               ' x   ',
                               ' xxx ',
                               '     ',
                               '     '],
                              ['     ',
                               '  xx ',
                               '  x  ',
                               '  x  ',
                               '     '],
                              ['     ',
                               '     ',
                               ' xxx ',
                               '   x ',
                               '     '],
                              ['     ',
                               '  x  ',
                               '  x  ',
                               ' xx  ',
                               '     ']],
                        'L': [['     ',
                               '   x ',
                               ' xxx ',
                               '     ',
                               '     '],
                              ['     ',
                               '  x  ',
                               '  x  ',
                               '  xx ',
                               '     '],
                              ['     ',
                               '     ',
                               ' xxx ',
                               ' x   ',
                               '     '],
                              ['     ',
                               ' xx  ',
                               '  x  ',
                               '  x  ',
                               '     ']],
                        'I': [['  x  ',
                               '  x  ',
                               '  x  ',
                               '  x  ',
                               '     '],
                              ['     ',
                               '     ',
                               'xxxx ',
                               '     ',
                               '     ']],
                        'O': [['     ',
                               '     ',
                               ' xx  ',
                               ' xx  ',
                               '     ']],
                        'T': [['     ',
                               '  x  ',
                               ' xxx ',
                               '     ',
                               '     '],
                              ['     ',
                               '  x  ',
                               '  xx ',
                               '  x  ',
                               '     '],
                              ['     ',
                               '     ',
                               ' xxx ',
                               '  x  ',
                               '     '],
                              ['     ',
                               '  x  ',
                               ' xx  ',
                               '  x  ',
                               '     ']]}

        self.pygame_init()

    @staticmethod
    def check_exit():
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    Tetris.exit()
            pygame.event.post(event)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Tetris.exit()
            pygame.event.post(event)

    def pygame_init(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def wait_press(arr):
        Tetris.check_exit()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in arr:
                    x, y = pygame.mouse.get_pos()
                    if button.is_clicked(x, y):
                        return button
        return None

    def start_window(self):
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        text = font.render("Выберите уровень сложности:", True, self.WHITE)
        rect = text.get_rect()
        rect.centerx = int(self.WIDTH / 2)
        rect.y = 100
        self.screen.blit(text, rect)

        button_lvl_1 = Button(int(self.WIDTH / 2) - 110,
                              int(self.HEIGHT / 3),
                              220, 50, "Лёгкий",
                              self.WHITE, self.GREEN, font)
        button_lvl_2 = Button(int(self.WIDTH / 2) - 110,
                              int(self.HEIGHT / 3) + 60,
                              220, 50, "Нормальный",
                              self.WHITE, self.YELLOW, font)
        button_lvl_3 = Button(int(self.WIDTH / 2) - 110,
                              int(self.HEIGHT / 3) + 120,
                              220, 50, "Сложный",
                              self.WHITE, self.RED, font)
        buttons_arr = [button_lvl_1, button_lvl_2, button_lvl_3]

        button_lvl_1.draw(screen=self.screen)
        button_lvl_2.draw(screen=self.screen)
        button_lvl_3.draw(screen=self.screen)

        btn = Tetris.wait_press(buttons_arr)

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)
        return btn

    def play(self):
        while True:
            level = self.start_window()
            self.run(level)

    def draw_title(self):
        font = pygame.font.SysFont('timesnewroman', 40)
        text = font.render("Tetris", True, self.WHITE)
        rect = text.get_rect()
        rect.centerx = int(self.WIDTH / 2)
        rect.y = 0
        self.screen.blit(text, rect)

    def get_figure(self):
        shape = random.choice(list(self.figures.keys()))
        rotation = random.choice(self.figures[shape])
        color = random.choice(self.colors)
        res = {'shape': shape,
               'fig': rotation,
               'color': color,
               'x': 3,
               'y': 0}
        return res

    def check_pos(self, cup, fig, deltax=0, deltay=0):
        fig_coor = []
        for i in range(5):
            for j in range(5):
                if fig['fig'][i][j] == 'x':
                    fig_coor.append([j, i])
        for i in range(len(fig_coor)):
            fig_coor[i][0] += fig['x'] + deltax
            fig_coor[i][1] += fig['y'] + deltay
        for x, y in fig_coor:
            if x < 0 or x > self.CUP_WIDTH - 1:
                return False
            if y < 0 or y > self.CUP_HEIGHT - 1:
                return False
            if cup[x][y] != ' ':
                return False
        return True

    def add_fig(self, cup, fig):
        for i in range(5):
            for j in range(5):
                if fig['fig'][j][i] != ' ':
                    cup[fig['x'] + i][fig['y'] + j] = self.colors.index(fig['color'])

    def draw_fig(self, fig):
        for x in range(5):
            for y in range(5):
                if fig['fig'][y][x] != ' ':
                    pygame.draw.rect(self.screen, fig['color'],
                                     (self.CUP_X + self.BLOCK * (fig['x'] + x) + 1,
                                      self.CUP_Y + self.BLOCK * (fig['y'] + y) + 1,
                                      self.BLOCK - 2, self.BLOCK - 2))

    def run(self, level):
        self.screen.fill(self.BLACK)
        cup = self.new_cup()

        self.draw_title()
        self.draw_cup(cup)

        fig = self.get_figure()
        next_fig = self.get_figure()

        last_fall = time.time()
        while True:
            self.check_exit()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.check_pos(cup, fig, -1):
                            fig['x'] -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.check_pos(cup, fig, 1):
                            fig['x'] += 1
                    elif event.key == pygame.K_UP:
                        rotations = self.figures[fig['shape']]
                        rotation = (rotations.index(fig['fig']) + 1) % len(rotations)
                        fig['fig'] = rotations[rotation]
                        if not self.check_pos(cup, fig):
                            rotation = (rotations.index(fig['fig']) - 1) % len(rotations)
                            fig['fig'] = rotations[rotation]
            if time.time() - last_fall > 0.5:
                if self.check_pos(cup, fig, 0, 1):
                    fig['y'] += 1
                    last_fall = time.time()
                else:
                    self.add_fig(cup, fig)
                    fig = next_fig
                    next_fig = self.get_figure()
                    if not self.check_pos(cup, fig):
                        return False

            self.screen.fill(self.BLACK)
            self.draw_title()
            self.draw_cup(cup)
            self.draw_fig(fig)
            pygame.display.update()
            self.clock.tick()

    def draw_cup(self, cup):
        pygame.draw.rect(self.screen,
                         self.WHITE,
                         (self.CUP_X, self.CUP_Y,
                          self.CUP_WIDTH * self.BLOCK,
                          self.CUP_HEIGHT * self.BLOCK,
                          ), 1)

        for x in range(self.CUP_WIDTH):
            for y in range(self.CUP_HEIGHT):
                if cup[x][y] != ' ':
                    pygame.draw.rect(self.screen, self.colors[cup[x][y]],
                                     (self.CUP_X + self.BLOCK * x + 1,
                                      self.CUP_Y + self.BLOCK * y + 1,
                                      self.BLOCK - 2, self.BLOCK - 2))

    def new_cup(self):
        cup = [[' ' for i in range(self.CUP_HEIGHT)] for j in range(self.CUP_WIDTH)]
        return cup


if __name__ == "__main__":
    game = Tetris()
    game.play()
