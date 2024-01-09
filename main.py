import sys
import random
import time
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (146, 110, 174)
colors = [GREEN, BLUE, RED, YELLOW, PURPLE]

background = pygame.image.load(".jpg")      
icon = pygame.image.load(".png")
pygame.display.set_icon(icon)


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


class Figure:
    figures = {'S': [['     ',
                      '  xx ',
                      ' xx  ',
                      '     ',
                      '     '],
                     ['     ',
                      '  x  ',
                      '  xx ',
                      '   x ',
                      '     ']],
               'Z': [['     ',
                      ' xx  ',
                      '  xx ',
                      '     ',
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
                      ' xxx ',
                      '   x ',
                      '     ',
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
                      ' xxx ',
                      '   x ',
                      '     ',
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
                      'xxxx ',
                      '     ',
                      '     ',
                      '     ']],
               'O': [['     ',
                      ' xx  ',
                      ' xx  ',
                      '     ',
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
                      ' xxx ',
                      '  x  ',
                      '     ',
                      '     '],
                     ['     ',
                      '  x  ',
                      ' xx  ',
                      '  x  ',
                      '     ']]}

    def __init__(self, shape: str, rotation: int, color: int):
        self.shape = shape
        self.rotation = rotation
        self.fig = Figure.figures[self.shape][rotation]
        self.color = color
        self.x = 3
        self.y = -1

    @property
    def get_fig_coor(self):
        fig_coor = []
        for i in range(5):
            for j in range(5):
                if self[i, j]:
                    fig_coor.append([j, i])
        for i in range(len(fig_coor)):
            fig_coor[i][0] += self.x
            fig_coor[i][1] += self.y
        return fig_coor

    @property
    def get_color(self):
        return colors[self.color]

    def __getitem__(self, index):
        return self.fig[index[0]][index[1]] == 'x'

    @classmethod
    def generate_figure(cls):
        shape = random.choice(list(cls.figures.keys()))
        rotation = random.randint(0, len(cls.figures[shape]) - 1)
        color = random.randint(0, len(colors) - 1)
        return cls(shape, rotation, color)

    def next_rotation(self):
        self.rotation = (self.rotation + 1) % len(Figure.figures[self.shape])
        self.fig = Figure.figures[self.shape][self.rotation]

    def previous_rotation(self):
        self.rotation = (self.rotation - 1) % len(Figure.figures[self.shape])
        self.fig = Figure.figures[self.shape][self.rotation]

    def draw_fig(self, screen, cup_x, cup_y, block):
        for x, y in self.get_fig_coor:
            pygame.draw.rect(screen, self.get_color,
                             (cup_x + block * x + 1,
                              cup_y + block * y + 1,
                              block - 2, block - 2))

    def draw_next_fig(self, screen, block):
        font = pygame.font.SysFont('arial', 30)
        text = font.render('Next shape:', True, WHITE)
        rect = text.get_rect()
        rect.x = 425
        rect.y = 100
        screen.blit(text, rect)
        pygame.draw.rect(screen, WHITE,
                         (440, 150,
                          block * 5, block * 5), 1)
        for x in range(5):
            for y in range(5):
                if self[y, x]:
                    pygame.draw.rect(screen, self.get_color,
                                     (440 + block * x + 1,
                                      150 + block * y + 1,
                                      block - 2, block - 2))


class Cup:
    def __init__(self, cup_x, cup_y, block, cup_width, cup_height):
        self.cup_width = cup_width
        self.cup_height = cup_height

        self.cup_x = cup_x
        self.cup_y = cup_y

        self.block = block

        self.lines = 0
        self.score = 0

        self.cup = self.get_new_cup_list()

    def get_new_cup_list(self):
        cup = []
        for i in range(self.cup_width):
            cup.append([' ' for _ in range(self.cup_height)])
        return cup

    def __getitem__(self, index):
        if isinstance(index, tuple):
            x, y = index
            return self.cup[x][y]
        else:
            return self.cup[index]

    def __setitem__(self, key, value):
        x, y = key
        self.cup[x][y] = value

    def draw(self, screen, color):
        pygame.draw.rect(screen, color,
                         (self.cup_x, self.cup_y,
                          self.cup_width * self.block,
                          self.cup_height * self.block,
                          ), 1)

        for x in range(self.cup_width):
            for y in range(self.cup_height):
                if self[x, y] != ' ':
                    pygame.draw.rect(screen, colors[int(self[x, y])],
                                     (self.cup_x + self.block * x + 1,
                                      self.cup_y + self.block * y + 1,
                                      self.block - 2, self.block - 2))

    def add_fig(self, fig):
        for x, y in fig.get_fig_coor:
            self[x, y] = fig.color
        c = 0
        for y in range(0, 20):
            for x in range(10):
                if self[x, y] == ' ':
                    break
            else:
                for x in range(10):
                    self[x].pop(y)
                    self[x].insert(0, ' ')
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

    def check_pos(self, fig, deltax=0, deltay=0):
        fig_coor = fig.get_fig_coor
        for i in range(len(fig_coor)):
            fig_coor[i][0] += deltax
            fig_coor[i][1] += deltay
        for x, y in fig_coor:
            if x < 0 or x > self.cup_width - 1:
                return False
            if y < 0 or y > self.cup_height - 1:
                return False
            if self[x, y] != ' ':
                return False
        return True

    def clear(self):
        self.score = 0
        self.lines = 0
        self.cup = self.get_new_cup_list()


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

        self.cup = Cup(self.CUP_X, self.CUP_Y, self.BLOCK, self.CUP_WIDTH, self.CUP_HEIGHT)

        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

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

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()

    @staticmethod
    def wait_press(button_arr=None, k_arr=None):
        Tetris.check_exit()

        for event in pygame.event.get():
            if k_arr is not None:
                if event.type == pygame.KEYDOWN:
                    if event.key in k_arr:
                        return event.key
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in button_arr:
                    x, y = pygame.mouse.get_pos()
                    if button.is_clicked(x, y):
                        return button
        return None

    def start_window(self):
        self.screen.fill(BLACK)
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        text = font.render("Выберите уровень сложности:", True, WHITE)
        rect = text.get_rect()
        rect.centerx = int(self.WIDTH / 2)
        rect.y = 100
        self.screen.blit(text, rect)

        font_statistic = pygame.font.SysFont('arial', 20, italic=True)

        button_lvl_1 = Button(int(self.WIDTH / 2) - 140,
                              int(self.HEIGHT / 3),
                              280, 50, "Лёгкий",
                              WHITE, GREEN, font)
        button_lvl_2 = Button(int(self.WIDTH / 2) - 140,
                              int(self.HEIGHT / 3) + 60,
                              280, 50, "Нормальный",
                              WHITE, YELLOW, font)
        button_lvl_3 = Button(int(self.WIDTH / 2) - 140,
                              int(self.HEIGHT / 3) + 120,
                              280, 50, "Сложный",
                              WHITE, RED, font)
        button_lvl_4 = Button(int(self.WIDTH / 2) - 140,
                              int(self.HEIGHT / 3) + 200,
                              280, 50, "Экстремальный",
                              WHITE, PURPLE, font)
        button_statistic = Button(self.WIDTH - 130, 5, 120, 30,
                                  "Статистика", WHITE, WHITE,
                                  font_statistic)

        buttons_arr = [button_lvl_1, button_lvl_2, button_lvl_3, button_lvl_4, button_statistic]

        for button in buttons_arr:
            button.draw(screen=self.screen)

        btn = Tetris.wait_press(buttons_arr)

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)
        d = {'Лёгкий': 1, "Нормальный": 2, "Сложный": 3, "Экстремальный": 4, "Статистика": 5}
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
        self.screen.fill(BLACK)
        self.draw_title()
        self.update_statistic(self.count_figures)

        if self.cup.score > Tetris.get_record(level):
            text = "Вы побили свой рекорд!"
            Tetris.set_record(level, self.cup.score)
        else:
            text = "Вы проиграли."

        font = pygame.font.SysFont('timesnewroman', 40)
        text1 = font.render(text, True, WHITE)
        rect1 = text1.get_rect()
        rect1.centerx = int(self.WIDTH / 2)
        rect1.y = 50

        text2 = font.render(f'Счёт: {self.cup.score}', True, WHITE)
        rect2 = text2.get_rect()
        rect2.centerx = int(self.WIDTH / 2)
        rect2.y = 100

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)

        button_repeat = Button(int(self.WIDTH / 2) - 110, 150,
                               220, 50, 'Повторить',
                               WHITE, WHITE, font)
        button_menu = Button(int(self.WIDTH / 2) - 110, 210,
                             220, 50, 'Меню',
                             WHITE, WHITE, font)
        button_exit = Button(int(self.WIDTH / 2) - 110, 270,
                             220, 50, 'Выйти',
                             WHITE, WHITE, font)

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

    @property
    def get_count_games(self):
        with open("statistic.txt") as f:
            text = f.read().strip()
        count, _ = text.split(',')
        return int(count)

    @property
    def get_count_figures(self):
        with open("statistic.txt") as f:
            text = f.read().strip()
        _, count = text.split(',')
        return int(count)

    def statistic_window(self):
        self.screen.fill(BLACK)
        self.draw_title()

        small_font = pygame.font.SysFont('timesnewroman', 30)
        play_text = small_font.render(f"Игр сыгранно: {self.get_count_games}", True, WHITE)
        fig_text = small_font.render(f"Фигур упало: {self.get_count_figures}", True, WHITE)

        record_title_font = pygame.font.SysFont("timesnewroman", 30, bold=True)
        record_title_text = record_title_font.render("Рекорды:", True, WHITE)

        records_font = pygame.font.SysFont("timesnewroman", 35)

        easy_text = records_font.render(f"Лёгкий: {self.get_record(1)}", True, WHITE)
        easy_rect = easy_text.get_rect()
        easy_rect.centerx = self.WIDTH // 2
        easy_rect.y = 220

        normal_text = records_font.render(f"Нормальный: {self.get_record(2)}", True, WHITE)
        normal_rect = normal_text.get_rect()
        normal_rect.centerx = self.WIDTH // 2
        normal_rect.y = 260

        hard_text = records_font.render(f"Сложный: {self.get_record(3)}", True, WHITE)
        hard_rect = hard_text.get_rect()
        hard_rect.centerx = self.WIDTH // 2
        hard_rect.y = 300

        extreme_text = records_font.render(f"Экстремальный: {self.get_record(4)}", True, WHITE)
        extreme_rect = extreme_text.get_rect()
        extreme_rect.centerx = self.WIDTH // 2
        extreme_rect.y = 350

        font_exit = pygame.font.SysFont('arial', 30)

        play_rect = play_text.get_rect()
        play_rect.x = 50
        play_rect.y = 80

        fig_rect = fig_text.get_rect()
        fig_rect.x = 50
        fig_rect.y = 120

        record_title_rect = record_title_text.get_rect()
        record_title_rect.x = 50
        record_title_rect.y = 160

        self.screen.blit(play_text, play_rect)
        self.screen.blit(fig_text, fig_rect)
        self.screen.blit(record_title_text, record_title_rect)
        self.screen.blit(easy_text, easy_rect)
        self.screen.blit(normal_text, normal_rect)
        self.screen.blit(hard_text, hard_rect)
        self.screen.blit(extreme_text, extreme_rect)
        pygame.draw.rect(self.screen, WHITE, (50, 200, 500, 230), 1)

        button_exit = Button(5, 5, 40, 40, "<", WHITE, WHITE, font_exit)
        button_exit.draw(self.screen)

        btn = Tetris.wait_press([button_exit])

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press([button_exit])
        self.play()

    def play(self, level=None):
        if level is None:
            level = self.start_window()
        if level == 5:
            self.statistic_window()
            return
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
        text = font.render("Tetris", True, WHITE)
        rect = text.get_rect()
        rect.centerx = int(self.WIDTH / 2)
        rect.y = 0
        self.screen.blit(text, rect)

    @staticmethod
    def get_figure():
        return Figure.generate_figure()

    @staticmethod
    def get_speed(level):
        if level == 1:
            return 0.4
        if level == 2:
            return 0.25
        if level == 3:
            return 0.15
        return 0.08

    def draw_info(self):
        font = pygame.font.SysFont('arial', 20)

        text1 = font.render("esc - exit", True, WHITE)
        rect1 = text1.get_rect()
        rect1.x = 20
        rect1.y = 50

        text2 = font.render("space - pause", True, WHITE)
        rect2 = text2.get_rect()
        rect2.x = 20
        rect2.y = 100

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)

    def draw_stat(self, level):
        font_stat = pygame.font.SysFont('arial', 40, bold=True)
        stat = font_stat.render('Statistic:', True, WHITE)
        stat_rect = stat.get_rect()
        stat_rect.centerx = 100
        stat_rect.y = 200

        self.screen.blit(stat, stat_rect)
        pygame.draw.rect(self.screen, WHITE,
                         (10, 250, 170, 200), 1)

        font = pygame.font.SysFont('timesnewroman', 20, italic=True)
        lines_text = font.render(f"Lines: {self.cup.lines}", True, WHITE)
        lines_rect = lines_text.get_rect()
        lines_rect.x = 15
        lines_rect.y = 260

        score_text = font.render(f"Score: {self.cup.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.x = 15
        score_rect.y = 300

        record_text = font.render(f"Record: {self.get_record(level)}", True, WHITE)
        record_rect = record_text.get_rect()
        record_rect.x = 15
        record_rect.y = 340

        self.screen.blit(record_text, record_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(lines_text, lines_rect)

    def pause(self):
        pause = pygame.Surface((600, 500), pygame.SRCALPHA)
        pause.fill((0, 0, 0, 127))
        self.screen.blit(pause, (0, 0))
        # self.screen.fill(BLACK)
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        button_continue = Button(int(self.WIDTH / 2) - 110, 150,
                                 220, 50, 'Продолжить',
                                 WHITE, WHITE, font)

        button_menu = Button(int(self.WIDTH / 2) - 110, 210,
                             220, 50, 'Меню',
                             WHITE, WHITE, font)

        button_exit = Button(int(self.WIDTH / 2) - 110, 270,
                             220, 50, 'Выйти',
                             WHITE, WHITE, font)
        buttons_arr = [button_continue, button_menu, button_exit]
        for button in buttons_arr:
            button.draw(self.screen)

        btn = Tetris.wait_press(buttons_arr, k_arr=[pygame.K_SPACE])

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr, k_arr=[pygame.K_SPACE])
        d = {'Продолжить': 1, 'Меню': 2, "Выйти": 3, str(pygame.K_SPACE): 1}
        return d[str(btn)]

    @staticmethod
    def update_statistic(count_figures):
        with open("statistic.txt") as f:
            text = f.read().strip().split(',')
        c_games, c_figures = text
        c_games = int(c_games)
        c_figures = int(c_figures)
        c_games += 1
        c_figures += count_figures

        with open("statistic.txt", mode='w') as f:
            f.write(','.join([str(c_games), str(c_figures)]))

    def run(self, level):
        self.screen.fill(BLACK)

        self.draw_title()
        self.cup.draw(self.screen, WHITE)
        self.draw_stat(level)

        self.count_figures = 0

        self.cup.clear()

        fig = self.get_figure()
        next_fig = self.get_figure()

        last_fall = time.time()
        speed = self.get_speed(level)

        left = False
        right = False

        hold_down_time = 0.15
        last_click = -1

        add_time = 0
        while True:
            self.check_exit()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                        last_click = time.time()
                        if self.cup.check_pos(fig, deltax=-1):
                            fig.x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if self.cup.check_pos(fig, deltax=1):
                            fig.x += 1
                        right = True
                        last_click = time.time()
                    elif event.key == pygame.K_UP:
                        fig.next_rotation()
                        if not self.cup.check_pos(fig):
                            fig.previous_rotation()
                    elif event.key == pygame.K_RETURN:
                        for i in range(1, 20):
                            if not self.cup.check_pos(fig, deltay=i):
                                fig.y += i - 1
                                break
                    elif event.key == pygame.K_SPACE:
                        ans = self.pause()
                        if ans == 2:
                            self.play()
                        elif ans == 3:
                            self.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left = False
                    elif event.key == pygame.K_RIGHT:
                        right = False
            if time.time() - last_fall > speed and time.time() - add_time > 0.5:
                if self.cup.check_pos(fig, deltax=0, deltay=1):
                    fig.y += 1
                    last_fall = time.time()
                else:
                    self.count_figures += 1
                    self.cup.add_fig(fig)
                    add_time = time.time()
                    fig = next_fig
                    next_fig = self.get_figure()
                    if not self.cup.check_pos(fig):
                        return False
            if left and time.time() - last_click > hold_down_time:
                if self.cup.check_pos(fig, deltax=-1):
                    fig.x -= 1
                last_click = time.time()
            elif right and time.time() - last_click > hold_down_time:
                if self.cup.check_pos(fig, deltax=1):
                    fig.x += 1
                last_click = time.time()

            self.screen.fill(BLACK)
            self.draw_title()
            self.draw_stat(level)
            self.draw_info()
            self.cup.draw(self.screen, WHITE)
            fig.draw_fig(self.screen, self.CUP_X, self.CUP_Y, self.BLOCK)
            next_fig.draw_next_fig(self.screen, self.BLOCK)
            pygame.display.update()
            self.clock.tick()





def main():
    game = Tetris()
    game.play()


if __name__ == "__main__":
    main()
