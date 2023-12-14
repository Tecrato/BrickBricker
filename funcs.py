import pygame as pag
from pygame.locals import QUIT
class Botons_functions:
        # -------------------------------------------------- Title Screen --------------------------------------------#
    def func_reanudar(self) -> None:
        self.title_screen = False
        self.lvl = self.lvl_max
        self.start(self.lvl_max)
    def func_jugar(self) -> None:
        self.title_screen = False
        self.lvl = 1
        self.start(self.lvl)
    def func_opciones(self) -> None:
        self.salir_text_title.move((self.ventana_rect.centerx,self.ventana_rect.centery * 1.65))
        self.options_menu()
    def func_extras(self) -> None:
        self.bool_title_extras = True
        self.salir_text_title.move((self.ventana_rect.centerx,self.ventana_rect.centery * 1.65))
        self.title_extras()
    def func_fan_lvls_title(self) -> None:
        self.title_fan_lvls_bool = True
        self.Pantalla_niveles_fans()


        # -------------------------------------------------- Options Title --------------------------------------------#
    def func_change_difficult(self,difficult) -> None:
        self.title_easy.change_color_ad('white','darkgrey')
        self.title_medium.change_color_ad('white','darkgrey')
        self.title_hard.change_color_ad('white','darkgrey')
        if difficult == 1:
            self.title_easy.change_color_ad('green','lightgreen')
            self.deltatime.FPS = 60
            self.deltatime_ball.FPS = 60
            self.framerate_dificultad = 60
            self.player.vel = 4
        elif difficult == 2:
            self.title_medium.change_color_ad('green','lightgreen')
            self.deltatime.FPS = 90
            self.deltatime_ball.FPS = 90
            self.framerate_dificultad = 90
            self.player.vel = 3.6
        elif difficult == 3:
            self.title_hard.change_color_ad('green','lightgreen')
            self.deltatime.FPS = 130
            self.deltatime_ball.FPS = 130
            self.framerate_dificultad = 130
            self.player.vel = 3.2
        self.json['difficult'] = difficult
    def func_low_detail_mode(self) -> None:
        self.low_detail_mode = not self.low_detail_mode
        self.json['low_detail'] = self.low_detail_mode
        if self.low_detail_mode:
            self.text_low_detail_mode.change_text('Low Detail Mode: O')
        else:
            self.text_low_detail_mode.change_text('Low Detail Mode: X')
    def func_del_progress(self) -> None:
        self.bool_title_confirm = True
        if self.title_confirm():
            self.json["lvlLimit"] = 1
            self.lvl_max = 1
            self.boton_reanudar.move((-500,-500))
            self.savejson()
    def func_fullscreen(self) -> None:
        pag.display.toggle_fullscreen()
    def func_drop_music_file(self) -> None:
        self.Drop_event_bool = True
        self.button_load_music.change_color_ad('green','green')
        self.button_load_music.change_text('Arrastra tu carpeta/cancion aca!')


        # -------------------------------------------------- Music Botons --------------------------------------------#
    def func_music_next(self) -> None:
        if len(self.music_var.canciones) > 0:
            self.hilos.submit(self.cambiar_musica, 'change')
    def func_music_retry(self) -> None:
        if len(self.music_var.canciones) > 0:
            pag.mixer_music.play()
    def func_music_pause(self) -> None:
        if p := self.music_var.pause():
            self.boton_pause_musica.change_text('')
        else:
            self.boton_pause_musica.change_text('')
        self.json["music_pause"] = p
    def func_music_random(self) -> None:
        if r := self.music_var.set_random():
            self.boton_random_musica.change_text('列')
        else:
            self.boton_random_musica.change_text('')
        self.json["music_random"] = r


        # -------------------------------------------------- Pause Botons --------------------------------------------#
    def func_pause_X(self) -> None:
        self.title_screen = True
        self.pausado = False
        self.effects_after.clear()
        self.effects_before.clear()
        self.cubic_bezier_transitions.clear()
        self.reset()
        self.Pantalla_de_titulo()