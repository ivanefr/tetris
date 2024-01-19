import sys
import time
import pygame
from cup import Cup
from constants import *
from button import Button, ButtonWithImage
from figure import Figure
import os
import random


class Tetris:
    def __init__(self):
        self.WIDTH = 600
        self.HEIGHT = 500
        self.size = self.WIDTH, self.HEIGHT

        self.BLOCK = 20

        self.CUP_WIDTH = 10
        self.CUP_HEIGHT = 20
        self.CUP_X = self.WIDTH // 2 - (self.CUP_WIDTH // 2) * self.BLOCK
        self.CUP_Y = 50

        self.count_figures = None

        self.cup = Cup(self.CUP_X, self.CUP_Y, self.BLOCK, self.CUP_WIDTH, self.CUP_HEIGHT)

        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

        colors = Tetris.get_colors()

        self.FONT_COLOR = colors[0]
        self.BUTTON_COLOR = colors[1]
        self.CUP_BORDER_COLOR = colors[2]
        self.MARKING_COLOR = colors[3]
        self.BACKGROUND_COLOR = colors[4]

    @staticmethod
    def get_colors():
        with open("data/colors.txt") as f:
            text = f.read().strip()
        colors = text.strip().split('\n')
        res = []
        for color in colors:
            if color == "None":
                res.append(None)
                continue
            color = color.split(',')
            c = []
            for i in color:
                c.append(int(i.strip()))
            res.append((*c,))
        return res

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

    def set_colors(self):
        with open('data/colors.txt', mode='w') as f:
            f.write(str(self.FONT_COLOR)[1:-1] + '\n')
            f.write(str(self.BUTTON_COLOR)[1:-1] + '\n')
            f.write(str(self.CUP_BORDER_COLOR)[1:-1] + '\n')
            if self.MARKING_COLOR is None:
                f.write("None\n")
            else:
                f.write(str(self.MARKING_COLOR)[1:-1] + '\n')
            f.write(str(self.BACKGROUND_COLOR)[1:-1] + '\n')

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
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        text = font.render("Выберите уровень сложности:", True, self.FONT_COLOR)
        rect = text.get_rect()
        rect.centerx = int(self.WIDTH / 2)
        rect.y = 100
        self.screen.blit(text, rect)

        font_statistic = pygame.font.SysFont('arial', 20, italic=True)

        button_lvl_1 = Button(int(self.WIDTH / 2) - 140,
                              int(self.HEIGHT / 3),
                              280, 50, "Лёгкий",
                              self.BUTTON_COLOR, GREEN, font)
        button_lvl_2 = Button(int(self.WIDTH / 2) - 140,
                              int(self.HEIGHT / 3) + 60,
                              280, 50, "Нормальный",
                              self.BUTTON_COLOR, YELLOW, font)
        button_lvl_3 = Button(int(self.WIDTH / 2) - 140,
                              int(self.HEIGHT / 3) + 120,
                              280, 50, "Сложный",
                              self.BUTTON_COLOR, RED, font)
        button_lvl_4 = Button(int(self.WIDTH / 2) - 140,
                              int(self.HEIGHT / 3) + 200,
                              280, 50, "Экстремальный",
                              self.BUTTON_COLOR, PURPLE, font)
        button_statistic = Button(self.WIDTH - 130, 5, 120, 30,
                                  "Статистика", self.BUTTON_COLOR, self.FONT_COLOR,
                                  font_statistic)

        setting_image = self.load_image("settings.png")
        image = pygame.transform.scale(setting_image, (40, 40))
        button_settings = ButtonWithImage(5, 5, 40, 40, image, self.BACKGROUND_COLOR)
        buttons_arr = [button_lvl_1, button_lvl_2, button_lvl_3, button_lvl_4, button_statistic, button_settings]

        for button in buttons_arr:
            button.draw(screen=self.screen)

        btn = Tetris.wait_press(buttons_arr)
        self.set_colors()

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)
        d = {'Лёгкий': 1, "Нормальный": 2, "Сложный": 3, "Экстремальный": 4, "Статистика": 5, "settings": 6}
        return d[str(btn)]

    @staticmethod
    def get_record(level):
        with open('data/records.txt') as f:
            text = f.read()
        return int(text.strip().split(',')[level - 1])

    @staticmethod
    def set_record(level, record):
        with open('data/records.txt') as f:
            text = f.read()
        text = text.strip().split(',')
        text[level - 1] = str(record)
        with open('data/records.txt', mode='w') as f:
            f.write(','.join(text))

    def draw_end_window(self, level, win=False):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        is_win = False

        if self.cup.score > Tetris.get_record(level) or win:
            text = "Вы побили свой рекорд!"
            Tetris.set_record(level, self.cup.score)
            is_win = True
        else:
            text = "Вы проиграли."

        font = pygame.font.SysFont('timesnewroman', 40)
        text1 = font.render(text, True, self.FONT_COLOR)
        rect1 = text1.get_rect()
        rect1.centerx = int(self.WIDTH / 2)
        rect1.y = 50

        text2 = font.render(f'Счёт: {self.cup.score}', True, self.FONT_COLOR)
        rect2 = text2.get_rect()
        rect2.centerx = int(self.WIDTH / 2)
        rect2.y = 100

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)

        button_repeat = Button(int(self.WIDTH / 2) - 110, 150,
                               220, 50, 'Повторить',
                               self.BUTTON_COLOR, self.FONT_COLOR, font)
        button_menu = Button(int(self.WIDTH / 2) - 110, 210,
                             220, 50, 'Меню',
                             self.BUTTON_COLOR, self.FONT_COLOR, font)
        button_exit = Button(int(self.WIDTH / 2) - 110, 270,
                             220, 50, 'Выйти',
                             self.BUTTON_COLOR, self.FONT_COLOR, font)

        buttons_arr = [button_repeat, button_menu, button_exit]

        for btn in buttons_arr:
            btn.draw(self.screen)

        return buttons_arr, is_win

    def end_window(self, level):
        self.update_statistic(self.count_figures)
        buttons_arr, is_win = self.draw_end_window(level)

        btn = Tetris.wait_press(buttons_arr)
        self.set_colors()

        all_sprites = None
        last_zv = None
        count_zv = None
        if is_win:
            all_sprites = pygame.sprite.Group()
            last_zv = 0
            count_zv = 0
        while btn is None:
            if is_win:
                if time.time() - last_zv > 0.5 and count_zv < 5:
                    from firework import create_particles
                    create_particles((random.randint(100, self.WIDTH - 100), random.randint(100, self.HEIGHT - 100)),
                                     all_sprites, self.WIDTH, self.HEIGHT)
                    last_zv = time.time()
                    count_zv += 1
                all_sprites.update()
                buttons_arr, _ = self.draw_end_window(level, is_win)
                all_sprites.draw(self.screen)
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)
        d = {'Повторить': 1, "Меню": 2, "Выйти": 3}
        return d[str(btn)]

    @property
    def get_count_games(self):
        with open("data/statistic.txt") as f:
            text = f.read().strip()
        count, _ = text.split(',')
        return int(count)

    @property
    def get_count_figures(self):
        with open("data/statistic.txt") as f:
            text = f.read().strip()
        _, count = text.split(',')
        return int(count)

    def statistic_window(self):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        small_font = pygame.font.SysFont('timesnewroman', 30)
        play_text = small_font.render(f"Игр сыгранно: {self.get_count_games}", True, self.FONT_COLOR)
        fig_text = small_font.render(f"Фигур упало: {self.get_count_figures}", True, self.FONT_COLOR)

        record_title_font = pygame.font.SysFont("timesnewroman", 30, bold=True)
        record_title_text = record_title_font.render("Рекорды:", True, self.FONT_COLOR)

        records_font = pygame.font.SysFont("timesnewroman", 35)

        easy_text, easy_rect = self.get_lvl_rect("Лёгкий", 220, records_font)
        normal_text, normal_rect = self.get_lvl_rect("Нормальный", 260, records_font)
        hard_text, hard_rect = self.get_lvl_rect("Сложный", 300, records_font)
        extreme_text, extreme_rect = self.get_lvl_rect("Экстремальный", 350, records_font)

        font_exit = pygame.font.SysFont('arial', 30)

        play_rect = self.get_rect(play_text, 50, 80)
        fig_rect = self.get_rect(fig_text, 50, 120)
        record_title_rect = self.get_rect(record_title_text, 50, 160)

        self.screen.blit(play_text, play_rect)
        self.screen.blit(fig_text, fig_rect)
        self.screen.blit(record_title_text, record_title_rect)
        self.screen.blit(easy_text, easy_rect)
        self.screen.blit(normal_text, normal_rect)
        self.screen.blit(hard_text, hard_rect)
        self.screen.blit(extreme_text, extreme_rect)
        pygame.draw.rect(self.screen, WHITE, (50, 200, 500, 230), 1)

        button_exit = Button(5, 5, 40, 40, "<", self.BUTTON_COLOR, self.FONT_COLOR, font_exit)
        button_exit.draw(self.screen)

        btn = Tetris.wait_press([button_exit])
        self.set_colors()

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press([button_exit])
        self.play()

    def get_lvl_rect(self, lvl_text, y, font):
        num = {"Лёгкий": 1, "Нормальный": 2, "Сложный": 3, "Экстремальный": 4}[lvl_text]
        easy_text = font.render(f"{lvl_text}: {self.get_record(num)}", True, self.FONT_COLOR)
        easy_rect = easy_text.get_rect()
        easy_rect.centerx = self.WIDTH // 2
        easy_rect.y = y
        return easy_text, easy_rect

    @staticmethod
    def get_rect(text, x, y):
        rect = text.get_rect()
        rect.x = x
        rect.y = y
        return rect

    def play(self, level=None):
        self.set_colors()

        if level is None:
            level = self.start_window()
        if level == 5:
            self.statistic_window()
            return
        if level == 6:
            from settings import Settings
            Settings.start_window(self)
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
        text = font.render("Tetris", True, self.FONT_COLOR)
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

        text1 = font.render("esc - exit", True, self.FONT_COLOR)
        rect1 = text1.get_rect()
        rect1.x = 20
        rect1.y = 50

        text2 = font.render("space - pause", True, self.FONT_COLOR)
        rect2 = text2.get_rect()
        rect2.x = 20
        rect2.y = 100

        self.screen.blit(text1, rect1)
        self.screen.blit(text2, rect2)

    def draw_stat(self, level):
        font_stat = pygame.font.SysFont('arial', 40, bold=True)
        stat = font_stat.render('Statistic:', True, self.FONT_COLOR)
        stat_rect = stat.get_rect()
        stat_rect.centerx = 100
        stat_rect.y = 200

        self.screen.blit(stat, stat_rect)
        pygame.draw.rect(self.screen, WHITE,
                         (10, 250, 170, 200), 1)

        font = pygame.font.SysFont('timesnewroman', 20, italic=True)
        lines_text = font.render(f"Lines: {self.cup.lines}", True, self.FONT_COLOR)
        lines_rect = lines_text.get_rect()
        lines_rect.x = 15
        lines_rect.y = 260

        score_text = font.render(f"Score: {self.cup.score}", True, self.FONT_COLOR)
        score_rect = score_text.get_rect()
        score_rect.x = 15
        score_rect.y = 300

        record_text = font.render(f"Record: {self.get_record(level)}", True, self.FONT_COLOR)
        record_rect = record_text.get_rect()
        record_rect.x = 15
        record_rect.y = 340

        levels = ["Easy", "Normal", "Hard", "Extreme"]

        lvl_text = font.render(f"Level: {levels[level - 1]}", True, self.FONT_COLOR)
        lvl_rect = lvl_text.get_rect()
        lvl_rect.x = 15
        lvl_rect.y = 380

        self.screen.blit(record_text, record_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(lines_text, lines_rect)
        self.screen.blit(lvl_text, lvl_rect)

    def pause_window(self):
        pause = pygame.Surface((600, 500), pygame.SRCALPHA)
        pause.fill((*self.BACKGROUND_COLOR, 127))
        self.screen.blit(pause, (0, 0))
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        button_continue = Button(int(self.WIDTH / 2) - 110, 150,
                                 220, 50, 'Продолжить',
                                 self.BUTTON_COLOR, self.FONT_COLOR, font)
        button_restart = Button(int(self.WIDTH / 2) - 110, 210,
                                220, 50, 'Заново',
                                self.BUTTON_COLOR, self.FONT_COLOR, font)
        button_menu = Button(int(self.WIDTH / 2) - 110, 270,
                             220, 50, 'Меню',
                             self.BUTTON_COLOR, self.FONT_COLOR, font)

        button_exit = Button(int(self.WIDTH / 2) - 110, 330,
                             220, 50, 'Выйти',
                             self.BUTTON_COLOR, self.FONT_COLOR, font)
        buttons_arr = [button_continue, button_menu, button_exit, button_restart]
        for button in buttons_arr:
            button.draw(self.screen)

        btn = Tetris.wait_press(buttons_arr, k_arr=[pygame.K_SPACE])
        self.set_colors()

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr, k_arr=[pygame.K_SPACE])
        d = {"Продолжить": 1, "Меню": 2, "Выйти": 3, str(pygame.K_SPACE): 1, "Заново": 4}
        return d[str(btn)]

    @staticmethod
    def load_image(name):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            sys.exit()
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        return image

    @staticmethod
    def update_statistic(count_figures):
        with open("data/statistic.txt") as f:
            text = f.read().strip().split(',')
        c_games, c_figures = text
        c_games = int(c_games)
        c_figures = int(c_figures)
        c_games += 1
        c_figures += count_figures

        with open("data/statistic.txt", mode='w') as f:
            f.write(','.join([str(c_games), str(c_figures)]))

    def run(self, level):
        self.screen.fill(self.BACKGROUND_COLOR)

        self.draw_title()
        self.cup.draw(self.screen, WHITE, self.MARKING_COLOR)
        self.draw_stat(level)

        self.count_figures = 0
        rotation_count = 0

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

        quick = False
        height = None
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
                        rotation_count += 1
                        if not self.cup.check_pos(fig):
                            fig.previous_rotation()
                            rotation_count -= 1
                    elif event.key == pygame.K_RETURN:
                        for i in range(1, 20):
                            if not self.cup.check_pos(fig, deltay=i):
                                fig.y += i - 1
                                height = i - 1
                                quick = True
                                break
                    elif event.key == pygame.K_SPACE:
                        ans = self.pause_window()
                        if ans == 2:
                            self.play()
                        elif ans == 3:
                            self.exit()
                        elif ans == 4:
                            self.play(level)
                    elif event.key == pygame.K_DOWN:
                        speed /= 3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left = False
                    elif event.key == pygame.K_RIGHT:
                        right = False
                    elif event.key == pygame.K_DOWN:
                        speed *= 3
            if time.time() - last_fall > speed and time.time() - add_time > 0.5:
                if self.cup.check_pos(fig, deltax=0, deltay=1):
                    fig.y += 1
                    last_fall = time.time()
                else:
                    self.count_figures += 1
                    self.cup.add_fig(fig)
                    if quick:
                        self.cup.update_score_by_falling(count_rotations=rotation_count,
                                                         is_quick=True, height=height)
                        quick = False

                    else:
                        self.cup.update_score_by_falling(count_rotations=rotation_count)
                    rotation_count = 0
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

            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_title()
            self.draw_stat(level)
            self.draw_info()
            fig.draw_fig(self.screen, self.CUP_X, self.CUP_Y, self.BLOCK)
            self.cup.draw(self.screen, self.CUP_BORDER_COLOR, self.MARKING_COLOR)
            next_fig.draw_next_fig(self.screen, self.BLOCK)
            pygame.display.update()
            self.clock.tick()
