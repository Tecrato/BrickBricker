from pygame import image, transform, rect, Vector2
from Utilidades import Hipotenuza
class Ball:
    def __init__(self, pos: tuple, size: int, surface, vel: list) -> None:
        self.image = transform.scale((image.load('Assets/images/pelota.png')), (size,size))
        self.pos = Vector2(pos)
        self.rect = rect.Rect(pos[0], pos[1], size, size)
        self.surface = surface
        self.vel = Vector2(vel)
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
        self.vel = Vector2(vel)
    def set_pos(self,pos) -> None:
        self.pos = Vector2(pos)

    def check_colision(self,bloques, dt=1):
        choque = self.rect.collidelistall(bloques)
        if len(choque) == 0:
            return -1
        elif len(choque) == 1:
            while self.rect.collidelist(bloques) != -1:
                self.retroceder(.1)
            while self.rect.collidelist(bloques) == -1:
                self.update(.1)
            return self.rect.collidelist(bloques)
        elif len(choque) > 1:
            self.retroceder(dt)
            return sorted(choque,key=lambda num:Hipotenuza(self.rect.center,bloques[num].center))[0]