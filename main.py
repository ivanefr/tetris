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
                        'I': [['     ',
                               '  x  ',
                               '  x  ',
                               '  x  ',
                               '  x  '],
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
        self.screen.fill(self.BLACK)
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
        d = {'Лёгкий': 1, "Нормальный": 2, "Сложный": 3}
        return d[str(btn)]

    @staticmethod
    def get_record(level):
        with open('records.txt') as f:
            text = f.read()
        return int(text.strip().split(',')[level - 1])

    @staticmethod
    def set_record(level, record):
        with open('records.txt') as f:
            text = f.read()
        text = text.strip().split(',')
        text[level - 1] = str(record)
        with open('records.txt', mode='w') as f:
            f.write(','.join(text))

    def end_window(self, level):
        self.screen.fill(self.BLACK)
        self.draw_title()

        if self.score > Tetris.get_record(level):
            text = "Вы побили свой рекорд!"
            Tetris.set_record(level, self.score)
        else:
            text = "Вы проиграли."

        font = pygame.font.SysFont('timesnewroman', 40)
        text1 = font.render(text, True, self.WHITE)
        rect1 = text1.get_rect()
        rect1.centerx = int(self.WIDTH / 2)
        rect1.y = 50

        text2 = font.render(f'Счёт: {self.score}', True, self.WHITE)
        rect2 = text2.get_rect()
        rect2.centerx = int(self.WIDTH / 2)
        rect2.y = 100

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)

        button_repeat = Button(int(self.WIDTH / 2) - 110, 150,
                               220, 50, 'Повторить',
                               self.WHITE, self.WHITE, font)
        button_menu = Button(int(self.WIDTH / 2) - 110, 210,
                             220, 50, 'Меню',
                             self.WHITE, self.WHITE, font)
        button_exit = Button(int(self.WIDTH / 2) - 110, 270,
                             220, 50, 'Выйти',
                             self.WHITE, self.WHITE, font)

        buttons_arr = [button_repeat, button_menu, button_exit]

        for btn in buttons_arr:
            btn.draw(self.screen)

        btn = Tetris.wait_press(buttons_arr)

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)
        d = {'Повторить': 1, "Меню": 2, "Выйти": 3}
        return d[str(btn)]

    def play(self, level=None):
        if level is None:
            level = self.start_window()
        self.run(level)
        ans = self.end_window(level)
        if ans == 3:
            Tetris.exit()
        if ans == 2:
            self.play()
        elif ans == 1:
            self.play(level)

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
               'y': -1}
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
        c = 0
        for y in range(0, 20):
            for x in range(10):
                if cup[x][y] == ' ':
                    break
            else:
                for x in range(10):
                    cup[x].pop(y)
                    cup[x].insert(0, ' ')
                c += 1
        if c == 1:
            self.score += 100
        elif c == 2:
            self.score += 200
        elif c == 3:
            self.score += 700
        elif c == 4:
            self.score += 1500
        self.lines += c

    def draw_fig(self, fig):
        for x in range(5):
            for y in range(5):
                if fig['fig'][y][x] != ' ':
                    pygame.draw.rect(self.screen, fig['color'],
                                     (self.CUP_X + self.BLOCK * (fig['x'] + x) + 1,
                                      self.CUP_Y + self.BLOCK * (fig['y'] + y) + 1,
                                      self.BLOCK - 2, self.BLOCK - 2))

    @staticmethod
    def get_speed(level):
        if level == 1:
            return 0.4
        if level == 2:
            return 0.25
        return 0.15

    def draw_next_fig(self, fig):
        font = pygame.font.SysFont('arial', 30)
        text = font.render('Next shape:', True, self.WHITE)
        rect = text.get_rect()
        rect.x = 425
        rect.y = 100
        self.screen.blit(text, rect)
        pygame.draw.rect(self.screen, self.WHITE,
                         (440, 150,
                          self.BLOCK * 5, self.BLOCK * 5), 1)
        for x in range(5):
            for y in range(5):
                if fig['fig'][y][x] != ' ':
                    pygame.draw.rect(self.screen, fig['color'],
                                     (440 + self.BLOCK * x + 1,
                                      150 + self.BLOCK * y + 1,
                                      self.BLOCK - 2, self.BLOCK - 2))

    def draw_info(self):
        font = pygame.font.SysFont('arial', 20)

        text1 = font.render("esc - exit", True, self.WHITE)
        rect1 = text1.get_rect()
        rect1.x = 20
        rect1.y = 50

        text2 = font.render("space - pause", True, self.WHITE)
        rect2 = text2.get_rect()
        rect2.x = 20
        rect2.y = 100

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)

    def draw_stat(self, level):
        font_stat = pygame.font.SysFont('arial', 40, bold=True)
        stat = font_stat.render('Statistic:', True, self.WHITE)
        stat_rect = stat.get_rect()
        stat_rect.centerx = 100
        stat_rect.y = 200

        self.screen.blit(stat, stat_rect)
        pygame.draw.rect(self.screen, self.WHITE,
                         (10, 250, 170, 200), 1)

        font = pygame.font.SysFont('timesnewroman', 20, italic=True)
        lines_text = font.render(f"Lines: {self.lines}", True, self.WHITE)
        lines_rect = lines_text.get_rect()
        lines_rect.x = 15
        lines_rect.y = 260

        score_text = font.render(f"Score: {self.score}", True, self.WHITE)
        score_rect = score_text.get_rect()
        score_rect.x = 15
        score_rect.y = 300

        record_text = font.render(f"Record: {self.get_record(level)}", True, self.WHITE)
        record_rect = record_text.get_rect()
        record_rect.x = 15
        record_rect.y = 340

        self.screen.blit(record_text, record_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(lines_text, lines_rect)


    def pause(self):
        ...

    def run(self, level):
        self.screen.fill(self.BLACK)
        cup = self.new_cup()

        self.score = 0
        self.lines = 0

        self.draw_title()
        self.draw_cup(cup)
        self.draw_stat(level)

        fig = self.get_figure()
        next_fig = self.get_figure()

        last_fall = time.time()
        speed = self.get_speed(level)
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
                    elif event.key == pygame.K_RETURN:
                        for i in range(1, 20):
                            if not self.check_pos(cup, fig, deltay=i):
                                fig['y'] += i - 1
                                break
                    elif event.key == pygame.K_SPACE:
                        self.pause()
            if time.time() - last_fall > speed:
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
            self.draw_stat(level)
            self.draw_info()
            self.draw_cup(cup)
            self.draw_fig(fig)
            self.draw_next_fig(next_fig)
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
