import pygame
from constants import *
import random


class Figure:
    def __init__(self, shape: str, rotation: int, color: int):
        self.shape = shape
        self.rotation = rotation
        self.fig = FIGURES[self.shape][rotation]
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
        return COLORS[self.color]

    def __getitem__(self, index):
        return self.fig[index[0]][index[1]] == 'x'

    @classmethod
    def generate_figure(cls):
        shape = random.choice(list(FIGURES.keys()))
        rotation = random.randint(0, len(FIGURES[shape]) - 1)
        color = random.randint(0, len(COLORS) - 1)
        return cls(shape, rotation, color)

    def next_rotation(self):
        self.rotation = (self.rotation + 1) % len(FIGURES[self.shape])
        self.fig = FIGURES[self.shape][self.rotation]

    def previous_rotation(self):
        self.rotation = (self.rotation - 1) % len(FIGURES[self.shape])
        self.fig = FIGURES[self.shape][self.rotation]

    def draw_fig(self, screen, cup_x, cup_y, block):
        for x, y in self.get_fig_coor:
            pygame.draw.rect(screen, self.get_color,
                             (cup_x + block * x ,
                              cup_y + block * y,
                              block, block))

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
