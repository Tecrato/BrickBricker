import pygame as pag, time, random
from pygame.surface import Surface

from Utilidades.text import *
from effects import Effect

class Win:
    def __init__(self, ventana: Surface) -> None:
        self.ventana = ventana
        self.ventana_rect = self.ventana.get_rect()

        self.contador = time.time()

        self.win_text = Create_text('You Win', 50, 'Assets/Fuentes/Orbitron-ExtraBold.ttf', self.ventana_rect.center, ventana)

        self.boton_lvl_pass = Create_boton('Next lvl', 30, './Assets/Fuentes/Orbitron-Medium.ttf', (self.ventana_rect.centerx, self.ventana_rect.height * 0.8), ventana, (40,10), 'center', 'white', color_rect='black', color_rect_active=(20,20,20), border_radius=5, border_top_right_radius=20, border_bottom_left_radius=20, border_width=8, border_color='purple')

        self.efecto = Effect(3,(random.randint(50,self.ventana_rect.w-50),random.randint(50,self.ventana_rect.h-50)),self.ventana, 20)

    def draw_WIN(self) -> None:
        # if time.time()-self.contador < random.randint(.5,2):

        if self.efecto.update(dt=4):
            self.efecto = Effect(3,(random.randint(50,self.ventana_rect.w-50),random.randint(50,self.ventana_rect.h-50)),self.ventana, 20)

        self.efecto.draw()

        self.win_text.draw()
        self.boton_lvl_pass.draw()