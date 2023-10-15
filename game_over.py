import pygame as pag
from pygame.surface import Surface

from Utilidades.text import *

class Game_over:
    def __init__(self, ventana: Surface) -> None:
        self.ventana = ventana
        self.ventana_rect = self.ventana.get_rect()

        self.game_over_text = Create_text('Game over', 50, 'Assets/Fuentes/Orbitron-ExtraBold.ttf', self.ventana_rect.center, ventana, with_rect=True, border_radius=20)

        self.restart = Create_boton('Restart', 30, './Assets/Fuentes/Orbitron-Medium.ttf', (self.ventana_rect.centerx, self.ventana_rect.height * 0.8), ventana, (40,10), 'center', 'white', color_rect='black', color_rect_active=(20,20,20), border_radius=5, border_top_right_radius=20, border_bottom_left_radius=20, border_width=8, border_color='purple')

    def draw_Gameover(self) -> None:
        self.game_over_text.draw()

        self.restart.draw()