import pygame as pag, requests

from lvl_manager import Lvl_manager
from Utilidades import GUI

class Botons_functions:
    def check_web_lvls_list(self, lista):
        lvl_manager = Lvl_manager(self.DB_path_name)
        for li in lista:
            if lvl_manager.search_web_lvl_saved(li[0]):
                li.append('')
            else:
                li.append('')
        lvl_manager.close()
        return lista


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
        self.salir_text_title.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * 1.65)
        self.options_menu()

    def func_extras(self) -> None:
        self.bool_title_extras = True
        self.salir_text_title.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * 1.65)
        self.title_extras()

    def func_fan_lvls_title(self) -> None:
        self.title_fan_lvls_bool = True
        self.lista_fans_lvls.change_list(self.lvl_manager.search_custom_lvls_list())
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
            self.text_low_detail_mode.text = 'Low Detail Mode: O'
        else:
            self.text_low_detail_mode.text = 'Low Detail Mode: X'

    def func_del_progress(self, result) -> None:
        if result == 'cancelar': return 0
        self.bool_title_confirm = True
        if self.title_confirm():
            self.json["lvlLimit"] = 1
            self.lvl_max = 1
            self.boton_reanudar.pos = (-500,-500)
            self.savejson()

    def func_fullscreen(self) -> None:
        pag.display.toggle_fullscreen()
        
    def func_drop_music_file(self) -> None:
        self.Drop_event_bool = True
        self.button_load_music.change_color_ad('green')
        self.button_load_music.text = 'Arrastra tu carpeta/cancion aca!'


# -------------------------------------------------- Music Botons --------------------------------------------#
    def func_music_next(self) -> None:
        if len(self.music_var.canciones) > 0:
            self.funcs_pool.start('cambiar cancion')
    def func_music_retry(self) -> None:
        if len(self.music_var.canciones) > 0:
            pag.mixer_music.play()
    def func_music_pause(self) -> None:
        if p := self.music_var.pause():
            self.boton_pause_musica.text = ''
        else:
            self.boton_pause_musica.text = ''
        self.json["music_pause"] = p
    def func_music_random(self) -> None:
        if r := self.music_var.set_random():
            self.boton_random_musica.text = '列'
        else:
            self.boton_random_musica.text = ''
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
    
    def select_lvl(self) -> None:
        self.title_screen = False
        self.title_fan_lvls_bool = False
        self.start_fan_lvl()
    def select_lvl_web(self) -> None:
        if self.lvl_fan == '-':
            return 0
        self.title_screen = False
        self.title_fan_lvls_bool = False
        self.start_fan_lvl()
    def borrar_lvl(self) -> None:
        self.GUI_admin.add(
            GUI.Desicion(self.ventana_rect.center, 'Confirmacion', 'Desea eliminar permanentemente el nivel?'), 
            lambda result: (self.lvl_manager.delete_custom_lvl(self.lvl_fan),self.lista_fans_lvls.change_list(self.lvl_manager.search_custom_lvls_list())) if result == 'aceptar' else None
            )
    def borrar_lvl_web(self) -> None:
        self.GUI_admin.add(
            GUI.Desicion(self.ventana_rect.center, 'Confirmacion', 'Desea eliminar los datos del nivel?'), 
            lambda result: (self.lvl_manager.delete_web_lvl(self.lvl_fan),self.funcs_pool.start('cargar niveles')) if result == 'aceptar' else None 
            )

    def func_load_custom_lvls(self) -> None:
        if self.bool_web_lvls:
            self.bool_web_lvls: bool = False
            for x in [self.lista_web_lvls,self.lista_fans_lvls,self.boton_borrar,self.boton_seleccionar,self.boton_seleccionar_web,
                self.boton_borrar_web,self.boton_web_lvls]:
                x.pos += (self.ventana_rect.width, 0)
            self.boton_web_lvls.pos += (50,0)
            self.boton_custom_lvls.pos += (-200,0)
            self.boton_reload_web_lvls.pos += (-100,0)

        self.lista_fans_lvls.change_list(self.lvl_manager.search_custom_lvls_list())

    def func_see_web_lvls(self) -> None:
        if not self.bool_web_lvls:
            self.bool_web_lvls: bool = True
            for x in [self.lista_web_lvls,self.lista_fans_lvls,self.boton_borrar,self.boton_seleccionar,self.boton_seleccionar_web,
                self.boton_borrar_web,self.boton_web_lvls]:
                x.pos -= (self.ventana_rect.width, 0)

            self.boton_web_lvls.pos -= (50,0)
            self.boton_custom_lvls.pos -= (-200,0)
            self.boton_reload_web_lvls.pos += (100,0)

    def func_load_web_lvls(self) -> None:
        self.ocupado = True
        " Esta función carga los niveles desde el servidor en internet. "
        

        self.text_buscando_niveles.text = 'Buscando niveles'
        
        # self.text_buscando_niveles.normal_move()
        self.text_buscando_niveles.pos = self.ventana_rect.center


        try:
            var = requests.get('https://Tecrato.pythonanywhere.com/api/get_all_lvls',timeout=5)
            if var.status_code == 200:
                lista = var.json()['niveles']
                lista = self.check_web_lvls_list(lista)
                self.lista_web_lvls.change_list(lista)
                self.text_buscando_niveles.text = 'Exito'
            elif var.status_code == 404:
                self.text_buscando_niveles.text = 'No se ah encontrado la pagina web'
            else:
                print(var.status_code)
        except Exception as err:
            print(err)
            self.text_buscando_niveles.text = 'Verifique su conexion a internet'
        finally:
            self.text_buscando_niveles.smothmove(120, .5, .3, -1.5)
            self.text_buscando_niveles.pos = pag.Vector2(self.ventana_rect.center) - (0,self.ventana_rect.height)
            self.ocupado = False
        
    def load_web_lvl(self,id:str) -> None:
        self.ocupado = True
        self.text_buscando_niveles.text = 'Descargando nivel'
        self.text_buscando_niveles.normal_move()
        self.text_buscando_niveles.pos = self.ventana_rect.center

        try:
            var = requests.get(f'https://Tecrato.pythonanywhere.com/api/get_lvl?id={id}',timeout=7)
            if var.status_code == 200:
                self.text_buscando_niveles.text = 'Exito'
                lvl_manager = Lvl_manager(self.DB_path_name)
                lvl_manager.guardar_nivel_online(var.json())
                self.func_load_web_lvls()
            elif var.status_code == 404:
                self.text_buscando_niveles.text = 'Error al conectar con la API'
        except Exception as err:
            print(err)
            self.text_buscando_niveles.text = 'Verifique su conexion a internet'
        finally:
            self.text_buscando_niveles.smothmove(120, .5, .3, -1.5)
            self.text_buscando_niveles.pos = pag.Vector2(self.ventana_rect.center) - (0,self.ventana_rect.height)
            self.ocupado = False
