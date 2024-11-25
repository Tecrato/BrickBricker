from pygame import draw, rect 
import random

from Utilidades import Hipotenuza
from Utilidades_pygame.Animaciones import *
# from Utilidades_pygame.particles import Particles
from Utilidades_pygame.particles import Particles
class Snake:
    def __init__(self, surface) -> None:
        self.surface = surface
        self.surface_rect = self.surface.get_rect()

        # self.particles = Particles(self.surface, radius=10)
        self.particles = Particles(
            spawn_pos=(0,0), radio=20, color=(255,255,255), velocity=.1, direccion=(1,0), radio_down=.05,
            vel_dispersion=.5, angle_dispersion=30, radio_dispersion=10, max_particles=100, time_between_spawns=.01,
            max_distance=1000, spawn_count=1
            )
        self.reset()


    def update(self) -> None:
        cab_center = self.movimiento1.update()
        if cab_center == True:
            self.reset()
            return True
        self.Cabeza.center = cab_center
        self.cuerpo1.center = self.movimiento2.update(self.Cabeza.center)
        self.cuerpo2.center = self.movimiento3.update(self.cuerpo1.center)
        self.cuerpo3.center = self.movimiento4.update(self.cuerpo2.center)
        self.cuerpo4.center = self.movimiento5.update(self.cuerpo3.center)
        self.cuerpo5.center = self.movimiento6.update(self.cuerpo4.center)

        self.particles.spawn_pos = self.cuerpo1.center
        self.particles.velocity = Hipotenuza((0,0),Vector2(self.cuerpo1.center) - Vector2(self.Cabeza.center))/10
        self.particles.direccion = Vector2(Vector2(self.cuerpo1.center) - Vector2(self.Cabeza.center)).normalize()
        self.particles.update(dt=1)

    def reset(self) -> None:

        self.Cabeza = rect.Rect(-200, -200, 50, 50)
        self.cuerpo1 = rect.Rect(-200, -200, 50, 50)
        self.cuerpo2 = rect.Rect(-200, -200, 45, 45)
        self.cuerpo3 = rect.Rect(-200, -200, 40, 40)
        self.cuerpo4 = rect.Rect(-200, -200, 35, 35)
        self.cuerpo5 = rect.Rect(-200, -200, 30, 30)

        self.movimiento1 = Curva_de_Bezier(60 * 7,
            [
                (-200, random.randint(-100,int(self.surface_rect.h *1.1))),
                (random.randint(-100,int(self.surface_rect.w *1.1)), random.randint(-100,int(self.surface_rect.h *1.1))),
                (random.randint(-100,int(self.surface_rect.w *1.1)), random.randint(-100,int(self.surface_rect.h *1.1))),
                (random.randint(-100,int(self.surface_rect.w *1.1)), random.randint(-100,int(self.surface_rect.h *1.1))),
                (self.surface_rect.w + 500, random.randint(-100,int(self.surface_rect.h *1.1)))
                ]
            , 1.3)

        self.movimiento2 = Second_Order_Dinamics(60, .8, .7, 0.5, self.cuerpo1.center)
        self.movimiento3 = Second_Order_Dinamics(60, .50, .7, 1.15, self.cuerpo2.center)
        self.movimiento4 = Second_Order_Dinamics(60, .50, .7, 1.15, self.cuerpo3.center)
        self.movimiento5 = Second_Order_Dinamics(60, .50, .7, 1.15, self.cuerpo4.center)
        self.movimiento6 = Second_Order_Dinamics(60, .50, .7, 1.15, self.cuerpo4.center)
        # self.particles = Particles(self.surface)

    def draw(self) -> None:
        self.particles.draw(self.surface)
        draw.rect(self.surface, (182,220,29), self.cuerpo5, border_radius=25)
        draw.rect(self.surface, (10,146,16), self.cuerpo5, 5, border_radius=25)

        draw.rect(self.surface, (182,220,29), self.cuerpo4, border_radius=25)
        draw.rect(self.surface, (10,146,16), self.cuerpo4, 5, border_radius=25)

        draw.rect(self.surface, (182,220,29), self.cuerpo3, border_radius=25)
        draw.rect(self.surface, (10,146,16), self.cuerpo3, 5, border_radius=25)

        draw.rect(self.surface, (182,220,29), self.cuerpo2, border_radius=25)
        draw.rect(self.surface, (10,146,16), self.cuerpo2, 5, border_radius=25)

        draw.rect(self.surface, (182,220,29), self.cuerpo1, border_radius=25)
        draw.rect(self.surface, (10,146,16), self.cuerpo1, 5, border_radius=25)

        draw.rect(self.surface, (0,128,0), self.Cabeza, border_top_right_radius=25, 
                      border_bottom_right_radius=25, border_bottom_left_radius=10, 
                      border_top_left_radius=10)