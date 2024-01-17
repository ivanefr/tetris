import pygame
from button import Button
from tetris import Tetris
from constants import *


class Settings:
    @staticmethod
    def start_window(self: Tetris):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        font_exit = pygame.font.SysFont('arial', 30)

        button_background = Button(self.WIDTH / 2 - 100, 150, 200, 50,
                                   "background", self.BUTTON_COLOR,
                                   self.FONT_COLOR, font)

        button_font = Button(self.WIDTH / 2 - 100, 210, 200, 50,
                             "font", self.BUTTON_COLOR,
                             self.FONT_COLOR, font)
        button_btn = Button(self.WIDTH / 2 - 100, 270, 200, 50,
                            "button", self.BUTTON_COLOR,
                            self.FONT_COLOR, font)
        button_cup = Button(self.WIDTH / 2 - 100, 330, 200, 50,
                            "cup", self.BUTTON_COLOR,
                            self.FONT_COLOR, font)
        button_exit = Button(5, 5, 40, 40, "<", self.BUTTON_COLOR, self.FONT_COLOR, font_exit)

        buttons_arr = [button_cup, button_btn, button_font, button_background, button_exit]

        for button in buttons_arr:
            button.draw(self.screen)

        btn = Tetris.wait_press(buttons_arr)
        self.set_colors()

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)

        d = {"background": 1, "font": 2, "button": 3, "cup": 4, "<": 5}
        res = d[str(btn)]
        if res == 5:
            self.play()
        elif res == 4:
            Settings.cup_window(self)
        elif res == 3:
            Settings.button_window(self)
        elif res == 2:
            Settings.font_window(self)
        elif res == 1:
            Settings.background_window(self)

    @staticmethod
    def background_window(self: Tetris):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        font_exit = pygame.font.SysFont('arial', 30)

        button_white = Button(self.WIDTH / 2 - 110, 150, 220, 50,
                              "White", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_green = Button(self.WIDTH / 2 - 110, 210, 220, 50,
                              "Green", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_red = Button(self.WIDTH / 2 - 110, 270, 220, 50,
                            "Red", self.BUTTON_COLOR,
                            self.FONT_COLOR, font)
        button_black = Button(self.WIDTH / 2 - 110, 330, 220, 50,
                              "Black", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_exit = Button(5, 5, 40, 40, "<", self.BUTTON_COLOR, self.FONT_COLOR, font_exit)
        res = Settings.change_window(self, button_white, button_black, button_green, button_red, button_exit)
        if res == str(button_white):
            self.BACKGROUND_COLOR = BG_WHITE
        elif res == str(button_red):
            self.BACKGROUND_COLOR = BG_RED
        elif res == str(button_green):
            self.BACKGROUND_COLOR = BLACK_GREEN
        elif res == str(button_black):
            self.BACKGROUND_COLOR = BLACK
        elif res == str(button_exit):
            Settings.start_window(self)
        Settings.background_window(self)

    @staticmethod
    def button_window(self: Tetris):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        font_exit = pygame.font.SysFont('arial', 30)

        button_white = Button(self.WIDTH / 2 - 110, 150, 220, 50,
                              "White", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_green = Button(self.WIDTH / 2 - 110, 210, 220, 50,
                              "Green", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_red = Button(self.WIDTH / 2 - 110, 270, 220, 50,
                            "Red", self.BUTTON_COLOR,
                            self.FONT_COLOR, font)
        button_black = Button(self.WIDTH / 2 - 110, 330, 220, 50,
                              "Black", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_exit = Button(5, 5, 40, 40, "<", self.BUTTON_COLOR, self.FONT_COLOR, font_exit)
        res = Settings.change_window(self, button_white, button_black, button_green, button_red, button_exit)
        if res == str(button_white):
            self.BUTTON_COLOR = WHITE
        elif res == str(button_red):
            self.BUTTON_COLOR = RED
        elif res == str(button_green):
            self.BUTTON_COLOR = GREEN
        elif res == str(button_black):
            self.BUTTON_COLOR = BLACK
        elif res == str(button_exit):
            Settings.start_window(self)
        Settings.button_window(self)

    @staticmethod
    def font_window(self: Tetris):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        font_exit = pygame.font.SysFont('arial', 30)

        button_white = Button(self.WIDTH / 2 - 110, 150, 220, 50,
                              "White", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_green = Button(self.WIDTH / 2 - 110, 210, 220, 50,
                              "Green", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_red = Button(self.WIDTH / 2 - 110, 270, 220, 50,
                            "Red", self.BUTTON_COLOR,
                            self.FONT_COLOR, font)
        button_black = Button(self.WIDTH / 2 - 110, 330, 220, 50,
                              "Black", self.BUTTON_COLOR,
                              self.FONT_COLOR, font)
        button_exit = Button(5, 5, 40, 40, "<", self.BUTTON_COLOR, self.FONT_COLOR, font_exit)
        res = Settings.change_window(self, button_white, button_black, button_green, button_red, button_exit)
        if res == str(button_white):
            self.FONT_COLOR = WHITE
        elif res == str(button_red):
            self.FONT_COLOR = RED
        elif res == str(button_green):
            self.FONT_COLOR = GREEN
        elif res == str(button_black):
            self.FONT_COLOR = BLACK
        elif res == str(button_exit):
            Settings.start_window(self)
        Settings.font_window(self)

    @staticmethod
    def cup_window(self: Tetris):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        font = pygame.font.SysFont('timesnewroman', 40)
        font_exit = pygame.font.SysFont('arial', 30)

        button_border_color = Button(self.WIDTH / 2 - 110, 150, 220, 50,
                                     "border-color", self.BUTTON_COLOR,
                                     self.FONT_COLOR, font)

        button_marking = Button(self.WIDTH / 2 - 110, 310, 220, 50,
                                "marking", self.BUTTON_COLOR,
                                self.FONT_COLOR, font)
        button_exit = Button(5, 5, 40, 40, "<", self.BUTTON_COLOR, self.FONT_COLOR, font_exit)

        buttons_arr = [button_border_color, button_marking, button_exit]

        for button in buttons_arr:
            button.draw(self.screen)

        btn = Tetris.wait_press(buttons_arr)
        self.set_colors()

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)

        d = {"border-color": 1, "marking": 2, "<": 3}
        res = d[str(btn)]
        if res == 3:
            Settings.start_window(self)
        elif res == 2:
            button_none = Button(self.WIDTH / 2 - 110, 150, 220, 50,
                                 "None", self.BUTTON_COLOR,
                                 self.FONT_COLOR, font)
            button_white = Button(self.WIDTH / 2 - 110, 210, 220, 50,
                                  "White", self.BUTTON_COLOR,
                                  self.FONT_COLOR, font)
            button_black = Button(self.WIDTH / 2 - 110, 270, 220, 50,
                                  "Black", self.BUTTON_COLOR,
                                  self.FONT_COLOR, font)
            button_red = Button(self.WIDTH / 2 - 110, 330, 220, 50,
                                "Red", self.BUTTON_COLOR,
                                self.FONT_COLOR, font)
            button_exit = Button(5, 5, 40, 40, "<", self.BUTTON_COLOR, self.FONT_COLOR, font_exit)
            res = Settings.change_window(self, button_none, button_white, button_exit, button_black, button_red)
            if res == str(button_none):
                self.MARKING_COLOR = None
            elif res == str(button_white):
                self.MARKING_COLOR = WHITE
            elif res == str(button_black):
                self.MARKING_COLOR = BLACK
            elif res == str(button_red):
                self.MARKING_COLOR = RED
            elif res == str(button_exit):
                Settings.cup_window(self)
            Settings.cup_window(self)
        elif res == 1:
            button_white = Button(self.WIDTH / 2 - 110, 150, 220, 50,
                                  "White", self.BUTTON_COLOR,
                                  self.FONT_COLOR, font)
            button_red = Button(self.WIDTH / 2 - 110, 210, 220, 50,
                                "Red", self.BUTTON_COLOR,
                                self.FONT_COLOR, font)
            button_black = Button(self.WIDTH / 2 - 110, 270, 220, 50,
                                  "Black", self.BUTTON_COLOR,
                                  self.FONT_COLOR, font)
            button_green = Button(self.WIDTH / 2 - 110, 330, 220, 50,
                                  "Green", self.BUTTON_COLOR,
                                  self.FONT_COLOR, font)
            button_exit = Button(5, 5, 40, 40, "<", self.BUTTON_COLOR, self.FONT_COLOR, font_exit)
            res = Settings.change_window(self, button_white, button_red, button_exit, button_black, button_green)
            if res == str(button_white):
                self.CUP_BORDER_COLOR = WHITE
            elif res == str(button_red):
                self.CUP_BORDER_COLOR = RED
            elif res == str(button_exit):
                Settings.cup_window(self)
            Settings.cup_window(self)

    @staticmethod
    def change_window(self: Tetris, *items: Button):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

        buttons_arr = [*items]

        for button in buttons_arr:
            button.draw(self.screen)

        btn = Tetris.wait_press(buttons_arr)
        self.set_colors()

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)

        return str(btn)
