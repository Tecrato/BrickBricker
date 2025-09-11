from pygame import rect, draw
from pygame.surface import Surface


from Utilidades_pygame.Animaciones import Second_Order_Dinamics

class Player:
    def __init__(self, pos: tuple, size: int, vel: float, surface: Surface, limits: tuple) -> None:
        self.pos = pos
        self.rect = rect.Rect(pos[0], pos[1], size, size)
        self.rect2 = rect.Rect(pos[0], pos[1], size, size / 7)
        self.rect3 = rect.Rect(pos[0], pos[1], size, size / 7)
        self.vel = vel
        self.limits = limits
        self.right = False
        self.left = False
        self.surface = surface
        self.movimiento = Second_Order_Dinamics(60,1.5,1,1,self.rect2.center)

    def draw(self) -> None:
        draw.rect(self.surface, 'green', self.rect2)

    def draw2(self) -> None:
        self.rect3.center = self.movimiento.update(self.rect2.center)
        draw.rect(self.surface, (50,50,50), self.rect3)

    def move(self,dt=1) -> None:
        if self.right and self.rect.right < self.limits[1]:
            self.rect.left += self.vel*dt
        if self.left and self.rect.left > self.limits[0]:
            self.rect.left -= self.vel*dt
        self.rect2.left = self.rect.left