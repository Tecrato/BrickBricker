import pygame as pag, requests

from Utilidades.hipotenuza import Vector2

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
        self.bool_web_lvls = False
        self.reload_list_for_fans_lvls()
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
        # -------------------------------------------------- Extra-lvls Botons --------------------------------------------#

    def func_load_web_lvls(self) -> None:
        """
        Esta función carga los niveles desde el servidor en internet.
        """
        self.text_buscando_niveles.change_text('Buscando niveles')
        self.text_buscando_niveles.smothmove(60, 2, .7, 1)
        self.text_buscando_niveles.move(self.ventana_rect.center)


        # self.hilos.submit(self.load_custom_lvls,(your_DB,))
        try:
            var = requests.get('http://Tecrato.pythonanywhere.com/api/get_all_lvls',timeout=5)
            if var.status_code == 200:
                lista = var.json()['niveles']
                self.lista_fans_lvls.change_list(lista)
                self.text_buscando_niveles.change_text('Exito')
                self.bool_web_lvls = True
            elif var.status_code == 404:
                self.text_buscando_niveles.change_text('No se ah encontrado la pagina web')
            else:
                print(var.status_code)
        except Exception as err:
            print(err)
            self.text_buscando_niveles.change_text('Verifique su conexion a internet')
        finally:
            self.text_buscando_niveles.smothmove(120, .5, .3, -1.5)
            self.text_buscando_niveles.move(list(Vector2(*self.ventana_rect.center) - (0,self.ventana_rect.height)))
        

    def load_web_lvl(self,name:str) -> None:
        self.text_buscando_niveles.change_text('Descargando nivel')
        self.text_buscando_niveles.smothmove(60, 2, .7, 1)
        self.text_buscando_niveles.move(self.ventana_rect.center)
        try:
            var = requests.get(f'http://Tecrato.pythonanywhere.com/api/get_lvl?nombre={name}',timeout=7)
            if var.status_code == 200:
                self.text_buscando_niveles.change_text('Exito')
                return var.json()['bloques']
            elif var.status_code == 404:
                self.text_buscando_niveles.change_text('Error al nocentar con la API')
        except Exception as err:
            print(err)
            self.text_buscando_niveles.change_text('Verifique su conexion a internet')
        finally:
            self.text_buscando_niveles.smothmove(120, .5, .3, -1.5)
            self.text_buscando_niveles.move(list(Vector2(*self.ventana_rect.center) - (0,self.ventana_rect.height)))

    # def load_custom_lvls(self,your_DB):
    #     try:
    #         var = requests.get('http://Tecrato.pythonanywhere.com/api/get_all_lvls',timeout=7)
    #         if var.status_code == 200:
    #             # self.cursor.execute("Select * FROM Niveles_2")
    #             # your_DB = self.cursor.fetchall()

    #             # [list(x)+[True] for x in var.json()['niveles']]
    #             lista = [list(x)+[x[1] in your_DB] for x in var.json()['niveles']]
    #             print(your_DB)
    #             self.lista_fans_lvls.change_list(lista)
    #             self.text_buscando_niveles.change_text('Exito')
    #         elif var.status_code == 404:
    #             self.text_buscando_niveles.change_text('No se ah encontrado la pagina web')
    #         else:
    #             print(var.status_code)
    #     except Exception as err:
    #         print(err)
    #         self.text_buscando_niveles.change_text('Verifique su conexion a internet')
    #     finally:
    #         self.text_buscando_niveles.smothmove(120, .5, .3, -1.5)
    #         self.text_buscando_niveles.move(list(Vector2(*self.ventana_rect.center) - (0,self.ventana_rect.height)))
