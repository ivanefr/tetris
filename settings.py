import pygame
from button import Button
from tetris import Tetris


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

    @staticmethod
    def button_window(self: Tetris):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

    @staticmethod
    def font_window(self: Tetris):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_title()

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

        while btn is None:
            pygame.display.update()
            self.clock.tick()
            btn = Tetris.wait_press(buttons_arr)

        d = {"border-color": 1, "marking": 2, "<": 3}
        res = d[str(btn)]
        if res == 3:
            Settings.start_window(self)
        elif res == 2:
            ...
            # Settings.change_window()
        elif res == 1:
            ...
            # Settings.change_window()

    @staticmethod
    def change_window(self, *items: Button):
        ...
