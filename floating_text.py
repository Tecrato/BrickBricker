import pygame as pag
from math import sin,radians
from pygame.surface import Surface


class Float_text:
    def __init__(self, text: str, size: int, font: str, pos: tuple, surface: Surface, color = 'white') -> None:
        self.top_inicial = pos[1]
        self.font = pag.font.Font(font, size)
        self.text = self.font.render(text, 1, color)
        self.rect = self.text.get_rect()
        self.rect.center = pos
        self.surface = surface
        self.vel = 1.0
        self.dis = 0

    def update(self) -> bool:
        if self.top_inicial - self.rect.top > 55:
            return True
        self.rect.centery = self.top_inicial - sin(radians(90)) * self.dis
        self.dis += self.vel
        self.vel -= 0.0113
        return False
        # self.rect.top -= self.vel
        # self.vel -= 0.02

    def draw(self) -> None:
        self.surface.blit(self.text, self.rect)      