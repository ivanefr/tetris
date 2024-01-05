import sys
import pygame


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
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

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
        font = pygame.font.SysFont('timesnewroman', 40)
        text = font.render("Tetris", True, self.WHITE)
        rect = text.get_rect()
        rect.centerx = int(self.WIDTH / 2)
        rect.y = 0
        self.screen.blit(text, rect)

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
        print(self.start_window())


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    game = Tetris()
    game.play()
