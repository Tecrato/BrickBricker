from typing import Tuple
import pygame as pag
from pygame.surface import Surface

class Vertical_bars:
    def __init__(self, pos: Tuple[int,int], surface: Surface, height: int) -> None:
        self.height = height
        self.pos = pos
        self.rect = pag.rect.Rect(0, 0, 10, height/2)
        self.rect2 = pag.rect.Rect(0, 0, 10, height)
        self.rect.bottomleft = pos
        self.rect2.bottomleft = pos
        self.surface = surface
        self.volumen = float(self.rect.height / self.height)

    def pulsando_volumen(self) -> None:
        g,k = pag.mouse.get_pos()
        if self.rect2.bottom - k > self.height:
            self.rect.height = self.height
        elif self.rect2.bottom - k < 0:
            self.rect.height = 0
        else:
            self.rect.height = self.rect2.bottom - k
        self.rect.bottom = self.pos[1]
        self.volumen = float(self.rect.height / self.height)
    
    def set_volumen(self, volumen) -> None:
        self.volumen = volumen
        self.rect.height = self.height*volumen
        self.rect.bottom = self.pos[1]
        pag.mixer_music.set_volume(volumen)

    def draw(self) -> None:
        pag.draw.rect(self.surface, 'lightblue', self.rect2, width=2)
        pag.draw.rect(self.surface, 'green', self.rect)