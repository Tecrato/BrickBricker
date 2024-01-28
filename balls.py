import numpy
from pygame import image, transform, rect
class Ball:
    def __init__(self, pos: tuple, size: int, surface, vel: list) -> None:
        self.image = transform.scale((image.load('Assets/images/pelota.png')), (size,size))
        self.pos = numpy.ndarray(pos)
        self.rect = rect.Rect(pos[0], pos[1], size, size)
        self.surface = surface
        self.vel = numpy.ndarray(vel)
        self.explocion = False
        self.lenta = False
        self.rapida = False

    def update(self,dt=1) -> None:
        self.pos = self.pos+(self.vel*dt)
        self.rect.center = self.pos

    def retroceder(self,dt=1) -> None:
        self.pos=(self.pos[0]-(self.vel[0]*dt),self.pos[1]-(self.vel[1]*dt))
        self.rect.center = self.pos

    def draw(self) -> None:
        self.surface.blit(self.image, self.rect)

    def set_vel(self,vel) -> None:
        self.vel = numpy.ndarray(vel)
    def set_pos(self,pos) -> None:
        self.pos = numpy.ndarray(pos)