import pygame as pag
from pygame.surface import Surface
class Ball:
    def __init__(self, pos: tuple, size: int, surface: Surface, vel: list) -> None:
        self.image = pag.transform.scale((pag.image.load('Assets/images/pelota.png')), (size,size))
        self.pos = pos
        self.rect = pag.rect.Rect(pos[0], pos[1], size, size)
        self.surface = surface
        self.vel = vel
        self.explocion = False
        self.lenta = False
        self.rapida = False

    def update(self,dt=1) -> None:
        self.pos=(self.pos[0]+(self.vel[0]*dt),self.pos[1]+(self.vel[1]*dt))
        self.rect.center = self.pos

    def retroceder(self,dt=1):
        self.pos=(self.pos[0]-(self.vel[0]*dt),self.pos[1]-(self.vel[1]*dt))
        self.rect.center = self.pos

    def draw(self) -> None:
        self.surface.blit(self.image, self.rect)