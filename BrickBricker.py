import pygame as pag, math, json, random
from os import mkdir, path, startfile
from pygame.locals import *
from sys import exit as ex
from io import open
from platformdirs import user_data_dir
from Utilidades import *
from pygame import Vector2


from balls import Ball
from background import Background
from effects import Effect
from floating_text import Float_text
from funcs import Botons_functions
from music import Set_music
from player import Player
from powers import PowerUp
from snake import Snake
from sound import Set_sounds

from lvl_manager import Lvl_manager
from Utilidades import GUI
from Utilidades import Funcs_pool

appdata = user_data_dir('save', 'BrickBreacker', roaming=True)


if not path.isdir('/'.join(appdata.split('\\')[:-1])):
    mkdir('/'.join(appdata.split('\\')[:-1]))
if not path.isdir(appdata):
    mkdir(appdata)


class BrickBricker(Botons_functions):
    def __init__(self) -> None:
        pag.init()


        #Ventana
        self.ventana = pag.display.set_mode((800,700), SCALED|RESIZABLE|DOUBLEBUF|HWSURFACE)
        self.ventana_rect = self.ventana.get_rect()
        pag.display.set_caption('BrickBreacker')
        pag.display.set_icon(pag.image.load('Screenshot_10.ico'))

        
        #Variedad en las variables
        # Cuenta contador, y saca cuenta
        self.life = 3
        self.lvl = 1
        self.lvl_fan = ''
        self.lvl_max = 1
        self.score = 0
        self.mulpliquer = 0
        self.bugueado = 0

        # Listas, y las que faltan
        self.bloques = []
        self.bloques_rects = []
        self.cubic_bezier_transitions = []
        self.effects_after = []
        self.effects_before = []
        self.float_texts_list = []
        self.powers = []
        self.sparks = []

        # Muchas verdades y falsedades
        self.acercandose: bool = False
        self.alive: bool = True
        self.bool_web_lvls: bool = False
        self.Drop_event_bool: bool = False
        self.fan_lvl_bool: bool = False
        self.low_detail_mode: bool = False
        self.ocupado: bool = False
        self.pausado: bool = False
        self.playing: bool = False
        self.title_fan_lvls_bool: bool = False
        self.title_screen: bool = True
        self.title_screen_options_bool: bool = False
        self.win: bool = False

        # Para los FPS y deltatime
        self.relog = pag.time.Clock()
        self.framerate_general = 60
        self.framerate_dificultad = 90
        
        # Fuentes
        self.fuente_nerd_mono = 'Assets/Fuentes/mononoki Bold Nerd Font Complete Mono.ttf'
        self.fuente_orbi_medium = 'Assets/Fuentes/Orbitron-Medium.ttf'
        self.fuente_orbi_extrabold = 'Assets/Fuentes/Orbitron-ExtraBold.ttf'
        self.fuente_consolas = 'Assets/Fuentes/consola.ttf'
        self.fuente_simbolos = 'Assets/Fuentes/Symbols.ttf'

        self.txt = Text('Cargando 0%\nCargando',50,None,(400,350),color='white',padding=100,with_rect=True,color_rect='black')
        self.loading_text('0')
        pag.display.flip()

        self.inilializar_juego()
        
        self.loading_text('90','Load Config\'s')

        pag.mixer_music.set_volume(0)
        self.load_json()
        pag.mixer_music.set_volume(self.json["music_volumen"])

        self.__delattr__('txt')

        self.Pantalla_de_titulo()
        self.Main_Process()

    def loading_text(self,n, txt = 'Load resources') -> None:
        self.ventana.fill('black')
        self.txt.text = f'Cargando {n}%\n{txt}'
        self.txt.draw(self.ventana)
        pag.display.flip()


    def inilializar_juego(self) -> None:

        GUI.configs['fuente_simbolos'] = self.fuente_simbolos

        # Base de datos
        self.DB_path_name = appdata+'/'+'lvls.sqlite3'
        self.lvl_manager = Lvl_manager(self.DB_path_name)

        # Manejador de hilos mejorado
        self.funcs_pool = Funcs_pool()
        self.funcs_pool.add('cargar niveles',self.func_load_web_lvls)
        self.funcs_pool.add('descargar nivel',lambda: self.load_web_lvl(self.lvl_fan))
        self.funcs_pool.add('cambiar cancion',self.cambiar_musica)

        # Jugador
        self.player = Player((350,650), 100, 3.4, self.ventana, (0, self.ventana_rect.w))

        # Bola
        self.ball = Ball((self.ventana_rect.centerx,self.ventana_rect.centery * 1.7), 10, self.ventana, [0,0])

        # Ventanas emergentes
        self.GUI_admin = GUI.GUI_admin()

        # Limites 
        self.limite_inferior = pag.rect.Rect(0, self.ventana_rect.height-15, self.ventana_rect.width, 50)
        self.limite_superior = pag.rect.Rect(-50, -47, self.ventana_rect.width+150, 50)
        self.limite_derecho = pag.rect.Rect(self.ventana_rect.width-2, -50, 50, self.ventana_rect.height+100)
        self.limite_izquierdo = pag.rect.Rect(-48, -50, 50, self.ventana_rect.height+100)

        # Variable Musica/Sonidos
        self.music_var = Set_music()
        self.sounds = Set_sounds()
        self.sounds.set_volumen(.5)

        # Aun mas cosas
        self.Serpiente = Snake(self.ventana)
        self.particles_ball = Particles(self.ventana, 2, radius=10,degrad_vel=.5)
        self.background = Background(self.ventana,(800,700),2)
        self.background2 = Background(self.ventana,(800,700),3)
        self.deltatime = Deltatime(90)
        self.deltatime_ball = Deltatime(90)

        Effect(5,(350,350), self.ventana, 100).draw()
        Effect(5,(350,350), self.ventana, 100).reset()


        # Textos y Botones

                                                # Del proceso principal
        self.life_text = Text('lives', 30, self.fuente_orbi_medium, (70,40),  'center')
        self.score_text = Text('Score 0', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx - 60,40), self.ventana)
        self.lvl_text = Text('lvl 1 ', 30, self.fuente_orbi_medium, (self.ventana_rect.w ,40),  'right')

        self.a_reiniciar = Text('Se ha Bugueado :V\nDebes reiniciar con "R"', 50, self.fuente_orbi_extrabold, self.ventana_rect.center)

        self.text_press_space = Text('Presiona espacio para comenzar', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.3), self.ventana)
        self.text_game_over = Text('Game over', 50, self.fuente_orbi_extrabold, self.ventana_rect.center,  with_rect=True, border_radius=20)
        self.boton_game_over = Button('Restart', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx, self.ventana_rect.height * 0.8),  (40,10), 'center', 'white', color_rect='black', color_rect_active=(20,20,20), border_radius=5, border_top_right_radius=20, border_bottom_left_radius=20, border_width=8, border_color='purple')
        self.text_win = Text('You Win', 50, self.fuente_orbi_extrabold, self.ventana_rect.center,  with_rect=True, border_radius=20)
        self.boton_win = Button('Next lvl', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx, self.ventana_rect.height * 0.8),  (40,10), 'center', 'white', color_rect='black', color_rect_active=(20,20,20), border_radius=5, border_top_right_radius=20, border_bottom_left_radius=20, border_width=8, border_color='purple')
        self.efecto_win = Effect(3,(random.randint(50,self.ventana_rect.w-50),random.randint(50,self.ventana_rect.h-50)), self.ventana, 20)

        self.text_ganaste=Text('Haz Ganado el juego\nGracias por jugar',40,self.fuente_orbi_medium,(self.ventana_rect.centerx,self.ventana_rect.centery-50),'center','white')

        self.loading_text(14)
                                                # De la pantalla de titulo
        self.title_text = Text('BrickBricker', 50, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery * .5), self.ventana)
        self.boton_reanudar = Button('Reanudar', 35, self.fuente_orbi_medium, (-500,-500),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1, func=self.func_reanudar)
        self.boton_jugar = Button('Jugar', 35, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.0),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=self.func_jugar)
        self.boton_fan_lvls = Button('', 30, self.fuente_simbolos, (self.boton_jugar.rect.right + 20,self.boton_jugar.rect.centery),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=self.func_fan_lvls_title)
        self.options_text_title = Button('Opciones', 35, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.15),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=self.func_opciones)
        self.salir_text_title = Button('Cerrar', 35, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.3),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1)
        self.salir_text_title.smothmove(60, 1, 0.73, 2)
        self.boton_extras = Button('', 40, self.fuente_simbolos, (0,self.ventana_rect.h-20),  dire='left', color='white', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=self.func_extras)
        

                                                # Del menu de opciones
        self.title_dificult = Text('Dificultad', 40, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery * .9), border_width=-1)
        self.title_easy = Button('Fácil', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1, func=lambda:self.func_change_difficult(1))
        self.title_medium = Button('Medio', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.13),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1, func=lambda:self.func_change_difficult(2))
        self.title_hard = Button('Difícil', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.26),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=lambda:self.func_change_difficult(3))
        self.button_load_music = Button('Cargar musica', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.38),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1, func=lambda:self.func_drop_music_file())


        self.text_low_detail_mode = Button('Low Detail Mode: X', 20, self.fuente_orbi_medium, (0,self.ventana_rect.h),  35, 'bottomleft', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1, func= self.func_low_detail_mode)
        self.button_toggle_fullscreen = Button('', 30, self.fuente_simbolos, (30,self.text_low_detail_mode.rect.top-10),  0, 'bottomleft', 'white', border_radius=10_000, border_color='white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=self.func_fullscreen)
        self.button_del_progress = Button('Borrar Progreso actual', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.50),  0, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1, func=lambda: self.GUI_admin.add(GUI.Desicion(self.ventana_rect.center, 'Confirmacion', 'Desea eliminar permanentemente el progreso?'), self.func_del_progress))

        self.lista_canciones=List((220,500),(580,20), None,smothscroll= True,background_color='black',padding_left= 0,padding_top=0,header=True, text_header='Canciones', header_top_left_radius=0, header_top_right_radius=0)


                                                # De la pausa
        self.pausa_text = Text('Pausado', 50, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery * .8),  'center', border_radius=10, with_rect=True)
        self.pausa_text_X = Button('Salir', 40, self.fuente_orbi_extrabold, (self.ventana_rect.w - 20,20), 20, 'topright', 'white', with_rect=True,color_rect='black', border_radius=40,func=self.func_pause_X)

        self.loading_text(28)


                                                # La pantalla de niveles creados
        self.text_created_lvls = Text('Created lvls', 40, self.fuente_orbi_medium, (self.ventana_rect.centerx, 10),  'top')
        self.boton_seleccionar = Button('Seleccionar',24,None,(430,107),10,'topleft','black',border_radius=0, border_width=-1, func=self.select_lvl)
        self.boton_borrar = Button('Eliminar',24,None,(640,107),10,'topleft','black',border_top_right_radius=10,border_radius=0, border_width=-1, func=self.borrar_lvl)
        self.lista_fans_lvls: Multi_list= Multi_list((self.ventana_rect.width*.8, self.ventana_rect.height*.8), 
            (self.ventana_rect.width*.1, self.ventana_rect.height*.15), 2, None, 30, 5, padding_left=13, header_text=['Id','Nombre'], 
            colums_witdh=[0,.10], border_color=(20,20,20), background_color=(1,1,1)) # (self.ventana_rect.width*.1, self.ventana_rect.height*.15)
        
        # Para niveles web
        self.boton_seleccionar_web = Button('Seleccionar',24,None,(self.ventana_rect.w+430,107),10,'topleft','black',border_radius=0, border_width=-1, func=self.select_lvl_web)
        self.boton_borrar_web = Button('Eliminar',24,None,(self.ventana_rect.w+640,107),10,'topleft','black',border_top_right_radius=10,border_radius=0, border_width=-1, func=self.borrar_lvl_web)
        self.lista_web_lvls: Multi_list= Multi_list((self.ventana_rect.width*.8, self.ventana_rect.height*.8), 
            (self.ventana_rect.width*1.1, self.ventana_rect.height*.15), 3, None, 30, padding_left=13, header_text=['Web_id','Nombre', ''], 
            colums_witdh=[0,.15, .5], border_color=(20,20,20), fonts=[None, None, self.fuente_simbolos], default=['-','-',''])
        
        self.boton_custom_lvls = Button('custom_lvls', 20,self.fuente_orbi_medium, (-200,0), dire='topleft', func= self.func_load_custom_lvls)
        self.boton_web_lvls = Button('web_lvls', 20,self.fuente_orbi_medium, (0,0), dire='topleft', func= self.func_see_web_lvls)
        self.boton_reload_web_lvls = Button('', 20,self.fuente_simbolos, (-100,50), dire='topleft', func= lambda:self.funcs_pool.start('cargar niveles'))
        l = [self.lista_web_lvls,self.lista_fans_lvls,self.boton_borrar,self.boton_seleccionar,self.boton_seleccionar_web,self.boton_borrar_web,self.boton_web_lvls,self.boton_custom_lvls, self.boton_reload_web_lvls]
        for x in l:
            x.smothmove(60, 1, .9, 1) 

        self.text_buscando_niveles: Text = Text('Buscando niveles',30,self.fuente_orbi_medium, Vector2(*self.ventana_rect.center) - (0,self.ventana_rect.height))
        self.text_buscando_niveles.smothmove(60, 2, .7, 1)


                                                # Del menu de extras
        self.extras_nombre = Text('Created\nby\nEdouard Sandoval', 45, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery * .5))
        self.extras_version = Text('Version 1.9.1',30,self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery))
        self.social_media_github_button = Button('',30,self.fuente_simbolos, (10,self.ventana_rect.h -10), 20, 'bottomleft', func=lambda: startfile('http://github.com/Tecrato'))
        self.social_media_youtube_button = Button('輸',30,self.fuente_simbolos, (70,self.ventana_rect.h -10), 20, 'bottomleft', func=lambda: startfile('http://youtube.com/channel/UCeMfUcvDXDw2TPh-b7UO1Rw'))

        # Musica
        self.boton_musica_musica = Text('♫', 40, self.fuente_consolas, (25,40),  padding=(20,0), with_rect=True)
        self.text_song = Text('\"Song\"', 20, self.fuente_consolas, (40,40),  'left', 'white', True, (0,0,0,255))
        self.boton_next_musica = Button('', 20, self.fuente_simbolos, (self.ventana_rect.w-20,self.ventana_rect.h - 120 - 30),  10, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1, func=self.func_music_next)
        self.boton_pause_musica = Button('', 20, self.fuente_simbolos, (self.ventana_rect.w-50,self.ventana_rect.h - 120 - 30),  10, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=self.func_music_pause)
        self.boton_retry_musica = Button('', 20, self.fuente_simbolos, (self.ventana_rect.w-80,self.ventana_rect.h - 120 - 30),  10, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=self.func_music_retry)
        self.boton_random_musica = Button('列', 20, self.fuente_simbolos, (self.ventana_rect.w-110,self.ventana_rect.h - 120 - 30),  10, 'center', 'white', color_active='darkgrey', with_rect=False, border_width=-1, sound_to_click=self.sounds.boton1,func=self.func_music_random)

        self.BV_Volumen_Musica = Barra_de_progreso((self.ventana_rect.w - 30, self.ventana_rect.h - 30), [15,100])
        self.BV_Volumen_Musica_press = False
        self.text_musica_vertical = Text('M\nu\ns\ni\nc', 20, self.fuente_consolas, (self.ventana_rect.w-50,self.ventana_rect.h - 120))

        self.BV_Volumen_Sonidos = Barra_de_progreso((self.ventana_rect.w - 80, self.ventana_rect.h - 30), [15,100])
        self.BV_Volumen_Sonidos_press = False
        self.text_sonido_vertical = Text('S\no\nu\nn\nd', 20, self.fuente_consolas, (self.ventana_rect.w-100,self.ventana_rect.h - 120))

        self.loading_text(42)

        # listas para no repetir codigo
        self.texts_title_list = [self.title_text,self.salir_text_title]
        self.botones_title_list = [self.boton_reanudar,self.boton_jugar,self.boton_fan_lvls,self.options_text_title,self.boton_extras]

        self.texts_main_list = [self.life_text, self.score_text, self.lvl_text]

        self.texts_song_list = [self.BV_Volumen_Musica,self.text_musica_vertical,self.BV_Volumen_Sonidos,
                                self.text_sonido_vertical,self.text_song,self.boton_musica_musica]
        self.botones_song_list = [self.boton_next_musica,self.boton_retry_musica,self.boton_pause_musica, self.boton_random_musica]
        
        self.texts_pause_list = self.texts_main_list.copy()
        self.texts_pause_list.extend(self.texts_song_list)
        self.texts_pause_list.append(self.pausa_text)
        self.botones_pause_list = self.botones_song_list.copy()
        self.botones_pause_list.append(self.pausa_text_X)

        self.texts_options_list = [self.lista_canciones, self.title_text,self.title_dificult,self.salir_text_title]
        self.texts_options_list.extend(self.texts_song_list)
        self.botones_options_list = [
            self.button_load_music,self.title_easy,self.title_medium,self.title_hard,self.text_low_detail_mode
            ,self.button_del_progress,self.button_toggle_fullscreen
            ]
        self.botones_options_list.extend(self.botones_song_list)

        self.texts_lvls_fans_list = [
            self.lista_fans_lvls,
            self.lista_web_lvls,
            self.text_created_lvls,
            self.pausa_text_X,
            self.text_buscando_niveles,
        ]
        self.botones_custom_lvls_list = [
            self.boton_seleccionar,
            self.boton_seleccionar_web,
            self.boton_borrar,
            self.boton_borrar_web,
            self.boton_web_lvls,
            self.boton_custom_lvls,
            self.boton_reload_web_lvls,
        ]
        
        self.loading_text(84)

    def load_json(self) -> None:
        #A hora con la posibilidad de guardar datos en un archivo json, el mundo es mas bonito
        try:
            self.json = json.load(open(appdata+'/' + 'progress.json', 'r'))
        except:
            self.json = {}

        # Para el nivel maximo
            
        self.json.setdefault("lvlLimit",1)
        self.lvl_max = self.json['lvlLimit']
        if self.lvl_max > 1:
            self.boton_reanudar.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * .85)

        # Para el "Aleatorio" en la musica
        self.json.setdefault("music_random",True)
        if self.json["music_random"]:
            self.boton_random_musica.text = '列'
        else:
            self.boton_random_musica.text = ''
        self.music_var.set_random(self.json["music_random"])

        # El directorio de la musica
        self.json.setdefault("music_random",True)
        self.json.setdefault("music_dir",None)

        if self.json["music_dir"] != None and self.json["music_dir"] != '':
            p = self.music_var.load_music(self.json["music_dir"])
            self.text_song.text = p['text']
            if len(self.music_var.canciones) > 0:
                self.lista_canciones.change_list(self.music_var.canciones)
                self.lista_canciones.select(index=p['index'])


        # Si la musica esta pausada
        self.json.setdefault("music_pause",False)
        if self.json["music_pause"]:
            self.music_var.pause(True)
            self.boton_pause_musica.text = ''
        else:
            self.boton_pause_musica.text = ''
        

        # Para rendimientos bajos
        self.json.setdefault("low_detail",False)
        self.low_detail_mode = self.json['low_detail']
        if self.low_detail_mode:
            self.text_low_detail_mode.text = 'Low Detail Mode: O'
        else:
            self.text_low_detail_mode.text = 'Low Detail Mode: X'

        #El volumen de la musica
        self.json.setdefault("music_volumen",.5)

        #El volumen de los sonidos
        self.json.setdefault("sound_volumen",.5)
        self.BV_Volumen_Sonidos.volumen = self.json["sound_volumen"]
        self.sounds.set_volumen(self.json["sound_volumen"])

        # El nivel de dificultad
        self.json.setdefault("difficult",2)
        self.func_change_difficult(self.json['difficult'])

        self.loading_text('99','Load Config\'s')

        self.savejson()

    def savejson(self) -> None:
        json.dump(self.json, open(appdata+'/'+'progress.json', 'w'))



    def colicion(self) -> None:
        choque = self.ball.check_colision(self.bloques_rects, self.deltatime_ball.dt)

        if choque == 0:
            self.ball.set_pos(Vector2(self.ball.pos[0]-self.ball.vel[0],self.player.rect2.top - 5))
            angle = Angulo(self.player.rect.center, self.ball.rect.center)
            self.ball.set_vel([math.cos(math.radians(angle))*Hipotenuza((0,0), self.ball.vel),math.sin(math.radians(angle))*Hipotenuza((0,0), self.ball.vel)])
            self.mulpliquer = 0
            self.bugueado = 0
            if not self.low_detail_mode:
                for x in range(15):
                    self.sparks.append(Spark(self.ventana, (self.ball.rect.centerx,650), math.radians(random.randint(230, 340)),random.randint(1, 4),(255, 255, 255),.6))
        elif choque > 0:
            if choque == 4:
                self.life -= 1
                self.life_text.text = f'Lives {self.life}'
                if self.life > 0:
                    self.sounds.ball_colicion.play()
                    self.effects_after.append(Effect(4,(0,0),self.ventana,self.ventana_rect.size))
                self.mulpliquer = 0
            elif choque > 4:
                self.bugueado = 0
                self.mulpliquer += 1
                self.score += 100 * self.mulpliquer
                self.score_text.text = f'Score {self.score}'
                if  self.bloques[choque]['power'] and self.bloques[choque]['power'] < 7:
                    self.powers.append(PowerUp(self.ventana, self.bloques[choque]['rect'].center, self.bloques[choque]['power'], 25))
                if not self.low_detail_mode:
                    self.float_texts_list.append(Float_text(f'+{100*self.mulpliquer} X {self.mulpliquer}',20,self.fuente_nerd_mono,self.bloques[choque]['rect'].center,self.ventana))
                
            if self.bloques[choque]['border_radius'] == 10000:
                angle = Angulo(self.bloques[choque]['rect'].center, self.ball.rect.center)
                self.ball.set_vel(Vector2(math.cos(math.radians(angle))*Hipotenuza((0,0),self.ball.vel),math.sin(math.radians(angle))*Hipotenuza((0,0),self.ball.vel)))
            else:
                if (self.ball.rect.centerx < self.bloques[choque]['rect'].left and self.ball.vel[0] > 0) or \
                    (self.ball.rect.centerx > self.bloques[choque]['rect'].right and self.ball.vel[0] < 0):
                    self.ball.vel[0] *= -1
                if (self.ball.rect.centery < self.bloques[choque]['rect'].top and self.ball.vel[1] > 0) or \
                    (self.ball.rect.centery > self.bloques[choque]['rect'].bottom and self.ball.vel[1] < 0):
                    self.ball.vel[1] *= -1


        if choque > -1 and self.bloques[choque]['effect'] == 1:
            if self.bloques[choque]['rect'] == self.player.rect2:
                self.sounds.ball_pop2.play()
                if not self.low_detail_mode:
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(15, [self.player.rect2.center, (self.player.rect2.centerx, self.player.rect2.centery + 15), self.player.rect2.center]), 'afectado': 'player'})
                    self.effects_before.append(Effect(1, (self.bloques[choque]['rect'].left,self.bloques[choque]['rect'].top), self.ventana, self.bloques[choque]['rect'].size))
            elif choque == 4:
                if not self.low_detail_mode:
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(60, [self.bloques[choque]['rect'].center, (self.bloques[choque]['rect'].centerx, self.bloques[choque]['rect'].centery - 30), self.bloques[choque]['rect'].center]), 'afectado': choque})
                    self.effects_before.append(Effect(1, (self.bloques[choque]['rect'].left,self.bloques[choque]['rect'].top), self.ventana, self.bloques[choque]['rect'].size))
        if choque > -1 and self.bloques[choque]['effect'] == 2:
            if not self.low_detail_mode:
                self.effects_after.append(Effect(2, self.bloques[choque]['rect'].center, self.ventana, 30))
            if self.ball.explocion:
                self.ball.explocion = False
                self.effects_before.append(Effect(5, self.ball.rect.center, self.ventana, 70, 90))
                for i,x in sorted(enumerate(self.bloques),reverse=True):
                    if i > 4 and Hipotenuza(self.ball.rect.center,x['rect'].center) < 90:

                        self.mulpliquer += 1
                        self.score += 100 * self.mulpliquer
                        self.score_text.text = f'Score {self.score}'
                        if x['power'] and x['power'] < 7:
                            self.powers.append(PowerUp(self.ventana, x['rect'].center, x['power'], 25))
                        if not self.low_detail_mode:
                            self.float_texts_list.append(Float_text(f'+{100*self.mulpliquer} X {self.mulpliquer}',20,self.fuente_nerd_mono,x['rect'].center,self.ventana))
                        self.bloques.pop(i)
                        self.bloques_rects.pop(i)
            else:
                self.bloques_rects.pop(choque)
                self.bloques.pop(choque)
            self.sounds.ball_pop.play()

    def draw_effects(self, effects_list) -> None:
        for i,x in sorted(enumerate(effects_list), reverse=True):
            if x.update(dt=self.deltatime.dt):
                effects_list.pop(i)
        [x.draw() for x in effects_list]
            
    def update_bloques_rects(self) -> None:
        self.bloques_rects.clear()
        for b in self.bloques:
            self.bloques_rects.append(b['rect'])

    def start(self, lvl: int) -> None:

        self.life = 3
        self.life_text.text = f'Lives {self.life}'
        self.lvl_text.text = f'Nivel: {self.lvl}'
        self.score_text.text = 'Score 0'
        self.ball.set_pos((self.ventana_rect.centerx,self.ventana_rect.centery * 1.7))
        self.ball.set_vel([0,-4])
        self.ball.update()
        self.player.rect.topleft = (350,650)

        self.lvl_max = max(self.lvl, self.lvl_max)
        self.json["lvlLimit"] = max(self.json["lvlLimit"], self.lvl_max)
        if self.lvl_max > 1:
            self.boton_reanudar.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * .85)
        self.savejson()

        self.fan_lvl_bool = False
        self.playing = False
        self.alive = True

        self.cubic_bezier_transitions.clear()
        self.reset()


        self.bloques.clear()
        self.bloques.append({'rect': self.player.rect2, 'effect': 1, 'color': 'green', 'border_radius': 0, 'power':0})
        self.bloques.append({'rect': self.limite_derecho, 'effect': 0, 'color': 'grey', 'border_radius': 0, 'power':0})
        self.bloques.append({'rect': self.limite_izquierdo, 'effect': 0, 'color': 'grey', 'border_radius': 0, 'power':0})
        self.bloques.append({'rect': self.limite_superior, 'effect': 0, 'color': 'grey', 'border_radius': 0, 'power':0})
        self.bloques.append({'rect': self.limite_inferior, 'effect': 1, 'color': 'red', 'border_radius': 0, 'power':0})
        if lvl == 1:
            for x in range(3,10):
                self.bloques.append({'rect': pag.rect.Rect(52*x + 80,22*6 + 100, 50, 20), 'effect': 2, 'color': (random.random()*255,random.random()*255,random.random()*255), 'border_radius': 0, 'power':0})
        elif lvl == 2:
            lvl_map = [
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 9 , 1 , 1 , 9 , 1 , 1 , 9 , 1 , 1 , 9 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 9 , 1 , 1 , 9 , 1 , 1 , 9 , 1 , 1 , 9 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 9 , 1 , 1 , 9 , 1 , 1 , 9 , 1 , 1 , 9 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
            ]

            for y in range(len(lvl_map)):
                color = (random.random()*255,random.random()*255,random.random()*255)
                for x in range(len(lvl_map[y])):
                    if lvl_map[y][x] == 9:
                        self.bloques.append({'rect': pag.rect.Rect(52 * x + 80,22 * y + 100, 50, 20), 'effect': 2, 'color': color, 'border_radius': 0, 'power':0})
        elif lvl == 3:
            for y in range(5):
                color = (random.random()*255,random.random()*255,random.random()*255)
                for x in range(10):
                    self.bloques.append({'rect': pag.rect.Rect(62 * x + 80,50 * y + 100, 60, 20), 'effect': 2, 'color': color, 'border_radius': 0, 'power':0})
        elif lvl == 4:
            bloques = self.lvl_manager.search_lvl_blocks(2)
        elif lvl == 5:
            bloques = self.lvl_manager.search_lvl_blocks(3)
        elif lvl == 6:
            bloques = self.lvl_manager.search_lvl_blocks(4)
        elif lvl == 7:
            bloques = self.lvl_manager.search_lvl_blocks(7)
        elif lvl == 8:
            bloques = self.lvl_manager.search_lvl_blocks(5)
        elif lvl == 9:
            bloques = self.lvl_manager.search_lvl_blocks(6)
        else:
            color = (random.random()*255,random.random()*255,random.random()*255)
            for x in range(3,10):
                self.bloques.append({'rect': pag.rect.Rect(52 * x + 80,22 * 6 + 100, 50, 20), 'effect': 2, 'color': color, 'border_radius': 0, 'power':0})
        
        if 10 > lvl > 3:
            self.bloques += [{'rect': pag.Rect(b[2],b[3],b[4],b[5]), 'effect': b[6], 'border_radius': b[7], 'power': b[8], 'color': (b[10],b[11],b[12])} for b in bloques]
        
        self.update_bloques_rects()

    def start_fan_lvl(self) -> None:
        self.lvl = 1
        self.life = 3
        self.life_text.text = f'Lives 3'
        self.lvl_text.text = f'Nivel: {self.lvl_fan_name}'
        self.score_text.text = f'Score 0'
        self.ball.set_pos((self.ventana_rect.centerx,self.ventana_rect.centery * 1.7))
        self.ball.set_vel([0,-4])
        self.ball.update()
        self.player.rect.topleft = (350,650)

        self.fan_lvl_bool = True
        self.alive = True
        self.playing = False

        self.powers.clear()
        self.cubic_bezier_transitions.clear()
        self.deltatime.FPS = self.framerate_dificultad
        self.deltatime_ball.FPS = self.framerate_dificultad
        pag.time.set_timer(USEREVENT+1,500000000,1)
        pag.time.set_timer(USEREVENT+2,500000000,1)
        self.reset()

        if self.bool_web_lvls:
            if  not self.lvl_manager.check_online_lvl(self.lvl_fan):
                self.funcs_pool.start('descargar nivel')


            # Cargar los bloques 
        self.bloques.clear()
        self.bloques.append({'rect': self.player.rect2, 'effect': 1, 'color': 'green', 'border_radius': 0, 'power':0})
        self.bloques.append({'rect': self.limite_derecho, 'effect': 0, 'color': 'grey', 'border_radius': 0,'power':0})
        self.bloques.append({'rect': self.limite_izquierdo, 'effect': 0, 'color': 'grey', 'border_radius': 0, 'power':0})
        self.bloques.append({'rect': self.limite_superior, 'effect': 0, 'color': 'grey', 'border_radius': 0, 'power':0})
        self.bloques.append({'rect': self.limite_inferior, 'effect': 1, 'color': 'red', 'border_radius': 0, 'power':0})
        
        if self.bool_web_lvls:
            bloques = self.lvl_manager.search_web_lvl_blocks(self.lvl_fan)
        else:
            bloques = self.lvl_manager.search_custom_lvl_blocks(self.lvl_fan)
        
        self.bloques += [{'rect': pag.Rect(b[2],b[3],b[4],b[5]), 'effect': b[6], 'border_radius': b[7], 'power': (random.randint(1,6) if random.randint(0,10000) < 1000 else 7) if b[8] != 0 else b[8], 'color': (b[10],b[11],b[12])} for b in bloques]
        
        self.update_bloques_rects()

    def cambiar_musica(self) -> None:
        p = self.music_var.change()
        self.text_song.text = p['text']
        self.lista_canciones.select(index=p['index'])

    def appli_powerup(self, type) -> None:
        if type == 1:
            self.life += 1
            self.life_text.text = f'Lives {self.life}'
            self.effects_after.append(Effect(4,(0,0),self.ventana,self.ventana_rect.size, color=(0,100,0)))
            self.sounds.extra_life.play()
        if type == 2:
            self.mulpliquer += 1
            self.score += 100 * (self.mulpliquer+10)
            self.score_text.text = f'Score {self.score}'
            if not self.low_detail_mode:
                self.float_texts_list.append(Float_text(f'+{100*self.mulpliquer+10} X {self.mulpliquer+10}',20,'Assets/Fuentes/mononoki Bold Nerd Font Complete Mono.ttf',self.player.rect2.center,self.ventana))
            self.sounds.money.play()
        elif type == 3:
            self.ball.explocion = True
        elif type == 4 and not self.ball.rapida:
            if not self.ball.lenta:
                self.ball.lenta = True
                self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(30, [(0,self.framerate_dificultad), (0,self.framerate_dificultad/2)]), 'afectado': 'ball'})
            pag.time.set_timer(USEREVENT+1,5000,1)
            self.sounds.slow.play()
        elif type == 5 and not self.ball.lenta:
            if not self.ball.rapida:
                self.ball.rapida = True
                self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(30, [(0,self.framerate_dificultad), (0,self.framerate_dificultad*1.5)]), 'afectado': 'ball'})
            pag.time.set_timer(USEREVENT+2,5000,1)
            self.sounds.fast.play()
        elif type == 6:
            self.life -= 1
            self.life_text.text = f'Lives {self.life}'
            if self.life > 0:
                self.sounds.decepcion.play()
                self.effects_after.append(Effect(4,(0,0),self.ventana,self.ventana_rect.size))

    def reset(self) -> None:
        self.score = 0
        self.mulpliquer = 0
        self.bugueado = 0
        self.powers.clear()
        self.particles_ball.clear()
        self.particles_ball.con = 0
        self.float_texts_list.clear()
        self.deltatime.FPS = self.framerate_dificultad
        self.deltatime_ball.FPS = self.framerate_dificultad
        self.limite_inferior.top = self.ventana_rect.height-15

        for i,tra in sorted(enumerate(self.cubic_bezier_transitions),reverse= True):
            if tra['afectado'] == 'ball':
                self.cubic_bezier_transitions.pop(i)
        pag.time.set_timer(USEREVENT+1,500000000,-1)
        pag.time.set_timer(USEREVENT+2,500000000,-1)
        self.ball.rapida = False
        self.ball.lenta = False
        self.ball.explocion = False

        self.win = False

    def check_loss(self) -> bool:
        if self.life <= 0 and self.alive == True:
            self.alive = False
            self.sounds.loss.play()
            self.reset()
            return True
        return False

    def eventos_en_comun(self, e) -> None:
        if not self.low_detail_mode: self.background.draw()
        else: self.ventana.fill('black')
        
        self.GUI_admin.input_update(e)
        for event in e:
            if event.type == QUIT:
                pag.quit()
                ex()
            elif event.type == 50000:
                self.funcs_pool.start('cambiar cancion')
            elif event.type == KEYDOWN:
                if event.key == K_F2 and len(self.music_var.canciones) > 0:
                    self.funcs_pool.start('cambiar cancion')
                elif event.key == K_F11:
                    pag.display.toggle_fullscreen()



    def title_extras(self) -> None:
        while self.bool_title_extras:
            self.eventos_en_comun(eventos := pag.event.get())

            for eventos in eventos:
                if eventos.type == KEYDOWN and eventos.key == K_ESCAPE:
                    self.bool_title_extras = False
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    if self.salir_text_title.click(eventos.pos):
                        self.sounds.boton1.play()
                        self.salir_text_title.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * 1.3)
                        self.bool_title_extras = False
                    self.social_media_github_button.click(eventos.pos)
                    self.social_media_youtube_button.click(eventos.pos)

            self.extras_nombre.draw(self.ventana)
            if not self.low_detail_mode:
                self.Serpiente.update()
                self.Serpiente.draw()
            self.salir_text_title.draw(self.ventana)
            self.extras_version.draw(self.ventana)
            self.social_media_github_button.draw(self.ventana)
            self.social_media_youtube_button.draw(self.ventana)

            pag.display.flip()
            self.relog.tick(60)

    def Pantalla_niveles_fans(self) -> None:
        while self.title_fan_lvls_bool:
            mx,my = pag.mouse.get_pos()
            self.eventos_en_comun(eventos := pag.event.get())

            for evento in eventos:
                if self.GUI_admin.active >= 0:
                    if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                        self.GUI_admin.pop()
                    elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                        self.GUI_admin.click((mx,my))
                elif self.ocupado:
                    break
                elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                    self.title_fan_lvls_bool = False
                elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                    if self.lista_fans_lvls.rect.collidepoint(evento.pos) and (p := self.lista_fans_lvls.click(evento.pos)):
                        self.lvl_fan = p['result'][0]
                        self.lvl_fan_name = p['result'][1]
                    elif self.lista_web_lvls.rect.collidepoint(evento.pos) and (p := self.lista_web_lvls.click(evento.pos)):
                        self.lvl_fan = p['result'][0]
                        self.lvl_fan_name = p['result'][1]
                    elif self.pausa_text_X.rect.collidepoint(evento.pos):
                        self.title_fan_lvls_bool = False
                    for b in self.botones_custom_lvls_list:
                        b.click(evento.pos)
                elif evento.type == MOUSEWHEEL and self.lista_fans_lvls.rect.collidepoint((mx,my)):
                    self.lista_fans_lvls.rodar(evento.y * 15)
                elif evento.type == MOUSEMOTION and self.lista_fans_lvls.scroll:
                    self.lista_fans_lvls.rodar_mouse(evento.rel[1])

            if not self.low_detail_mode:
                self.Serpiente.update()

            for b in self.texts_lvls_fans_list:
                b.draw(self.ventana)
            for b in self.botones_custom_lvls_list:
                b.draw(self.ventana,(mx,my))

            # print(self.lista_fans_lvls.pos)
            
            self.GUI_admin.draw(self.ventana, (mx,my))
            
            pag.display.flip()
            self.relog.tick(60)

    def Pantalla_de_titulo(self) -> None:
        while self.title_screen:
            self.eventos_en_comun(eventos := pag.event.get())

            for evento in eventos:
                if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                    pag.time.set_timer(QUIT, 200)
                if evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                    for b in self.botones_title_list:
                        b.click(evento.pos)
                    if self.salir_text_title.rect.collidepoint(evento.pos):
                        self.sounds.boton1.play()
                        pag.time.set_timer(QUIT, 200)

            if not self.low_detail_mode:
                self.Serpiente.update()
                self.Serpiente.draw()

            for x in [*self.texts_title_list,*self.botones_title_list]:
                x.update()
                x.draw(self.ventana)
            # for x in self.texts_title_list:
            #     x.draw(self.ventana)
            # for x in self.botones_title_list:
            #     x.draw(self.ventana)
            

            pag.display.flip()
            self.relog.tick(60)

    def options_menu(self) -> None:
        self.title_screen_options_bool = True
        while self.title_screen_options_bool:
            mx,my = pag.mouse.get_pos()
            self.eventos_en_comun(eventos:=pag.event.get())

            for evento in eventos:
                if evento.type == DROPFILE and self.Drop_event_bool:
                    self.button_load_music.change_color_ad('white','grey')
                    self.button_load_music.text = 'Cargar musica'
                    self.Drop_event_bool = False
                    if p := self.music_var.load_music(evento.file):
                        self.text_song.text = p['text']
                        self.json["music_dir"] = self.music_var.music_dir
                        self.savejson()
                        if len(self.music_var.canciones) > 0:
                            self.lista_canciones.change_list(self.music_var.canciones)
                            self.lista_canciones.select(p['index'])
                elif self.GUI_admin.active >= 0:
                    if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                        self.GUI_admin.pop()
                    elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                        self.GUI_admin.click((mx,my))
                elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                    self.sounds.boton1.play()
                    self.title_screen_options_bool = False
                    self.savejson()
                    self.salir_text_title.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * 1.3)
                elif evento.type == MOUSEBUTTONDOWN and evento.button == 1:
                    if self.Drop_event_bool == True:
                        self.button_load_music.change_color_ad('white','grey')
                        self.button_load_music.text = 'Cargar musica'
                        self.Drop_event_bool = False

                    for b in self.botones_options_list:
                        b.click(evento.pos)

                    if self.salir_text_title.rect.collidepoint(evento.pos):
                        self.sounds.boton1.play()
                        self.salir_text_title.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * 1.3)
                        self.title_screen_options_bool = False
                        self.savejson()

                    elif self.BV_Volumen_Musica.rect2.collidepoint(evento.pos):
                        self.BV_Volumen_Musica_press = True
                    elif self.BV_Volumen_Sonidos.rect2.collidepoint(evento.pos):
                        self.BV_Volumen_Sonidos_press = True
                    elif self.lista_canciones.rect.collidepoint(evento.pos):
                        p = self.lista_canciones.click(evento.pos)
                        if p and p != 'scrolling':
                            self.text_song.text = self.music_var.change(p['text'])['text']
                elif evento.type == MOUSEWHEEL and self.lista_canciones.rect.collidepoint((mx,my)):
                    self.lista_canciones.rodar(evento.y * 15)
                elif evento.type == MOUSEBUTTONUP:
                    self.BV_Volumen_Musica_press = False
                    self.BV_Volumen_Sonidos_press = False
                    self.lista_canciones.scroll = False
                elif evento.type == MOUSEMOTION and self.lista_canciones.scroll:
                    self.lista_canciones.rodar_mouse(evento.rel[1])

            #Barras de sonido
            if self.BV_Volumen_Sonidos_press:
                self.BV_Volumen_Sonidos.pulsando()
                self.sounds.set_volumen(self.BV_Volumen_Sonidos.volumen)
                self.json["sound_volumen"] = self.BV_Volumen_Sonidos.volumen
            if self.BV_Volumen_Musica_press:
                self.BV_Volumen_Musica.pulsando()
                pag.mixer_music.set_volume(self.BV_Volumen_Musica.volumen)
                self.json["music_volumen"] = self.BV_Volumen_Musica.volumen

            if not self.low_detail_mode:
                self.Serpiente.update()
                self.Serpiente.draw()

            for x in [*self.texts_options_list,*self.botones_options_list]:
                x.update()
                x.draw(self.ventana)
            # for x in self.texts_options_list:
            #     x.draw(self.ventana)
            # for x in self.botones_options_list:
            #     x.draw(self.ventana)

            pag.draw.circle(self.ventana, 'white', self.button_toggle_fullscreen.rect.center, 27, 4)
                
            self.GUI_admin.draw(self.ventana, (mx,my))

            pag.display.flip()
            self.relog.tick(60)


    def pause(self) -> None:
        while self.pausado:
            self.eventos_en_comun(eventos := pag.event.get())
            if not self.low_detail_mode:self.background2.draw()

            for eventos in eventos:
                if eventos.type == USEREVENT+1:
                    self.ball.lenta = False
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(60, [(0,self.framerate_dificultad/2), (0,self.framerate_dificultad)]), 'afectado': 'ball'})
                if eventos.type == USEREVENT+2:
                    self.ball.rapida = False
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(60, [(0,self.framerate_dificultad*1.5), (0,self.framerate_dificultad)]), 'afectado': 'ball'})
                if eventos.type == KEYDOWN and (eventos.key == K_ESCAPE or eventos.key == K_SPACE):
                    self.sounds.boton1.play()
                    self.pausado = False
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    for b in self.botones_pause_list:
                        b.click(eventos.pos)
                    if self.pausa_text.rect_text.collidepoint(eventos.pos):
                        self.sounds.boton1.play()
                        self.pausado = False
                    elif self.BV_Volumen_Musica.rect2.collidepoint(eventos.pos):  self.BV_Volumen_Musica_press = True
                    elif self.BV_Volumen_Sonidos.rect2.collidepoint(eventos.pos): self.BV_Volumen_Sonidos_press = True
                if eventos.type == MOUSEBUTTONUP:
                    self.BV_Volumen_Musica_press = False
                    self.BV_Volumen_Sonidos_press = False

            #Barras de sonido
            if self.BV_Volumen_Sonidos_press:
                self.BV_Volumen_Sonidos.pulsando()
                self.sounds.set_volumen(self.BV_Volumen_Sonidos.volumen)
                self.json["sound_volumen"] = self.BV_Volumen_Sonidos.volumen
            if self.BV_Volumen_Musica_press:
                self.BV_Volumen_Musica.pulsando()
                pag.mixer_music.set_volume(self.BV_Volumen_Musica.volumen)
                self.json["music_volumen"] = self.BV_Volumen_Musica.volumen
                if self.BV_Volumen_Musica.volumen == 0:
                    pag.mixer_music.pause()
                else:
                    pag.mixer_music.unpause()

            self.draw_effects(self.effects_before)

            [pag.draw.rect(self.ventana, alala['color'], alala['rect'], border_radius= alala['border_radius']) for alala in self.bloques]


            if self.alive and self.playing:
                self.ball.draw()
                self.particles_ball.draw()

            for i,p in sorted(enumerate(self.powers),reverse= True):
                p.draw()

            self.draw_effects(self.effects_after)

            for i,text in sorted(enumerate(self.float_texts_list),reverse= True):
                if text.update():
                    self.float_texts_list.pop(i)
                text.draw()

            for x in [*self.texts_pause_list,*self.botones_pause_list]:
                x.update()
                x.draw(self.ventana)
            # [x.draw(self.ventana) for x in self.texts_pause_list]
            # [x.draw(self.ventana) for x in ]

            if self.pausado == True:
                pag.display.flip()
            else: self.ventana.fill('black')
            self.relog.tick(30)

    def Main_Process(self) -> None:
        while True:
            self.deltatime.update()
            self.deltatime_ball.update()

            self.eventos_en_comun(eventos:=pag.event.get())
            if not self.low_detail_mode:self.background2.draw()
                
            for eventos in eventos:
                if eventos.type == WINDOWHIDDEN:
                    self.pausado = True
                    self.player.left = False
                    self.player.right = False
                    self.sounds.boton
                    self.pause()
                elif eventos.type == USEREVENT+1:
                    self.ball.lenta = False
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(60, [(0,self.framerate_dificultad/2), (0,self.framerate_dificultad)]), 'afectado': 'ball'})
                elif eventos.type == USEREVENT+2:
                    self.ball.rapida = False
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(60, [(0,self.framerate_dificultad*1.5), (0,self.framerate_dificultad)]), 'afectado': 'ball'})
                elif eventos.type == KEYDOWN:
                    if eventos.key == K_u and self.alive and not self.fan_lvl_bool:
                        self.lvl += 1
                        self.start(self.lvl)
                    elif eventos.key == K_ESCAPE and not self.win and self.alive:
                        self.pausado = True
                        self.player.left = False
                        self.player.right = False
                        self.sounds.boton1.play()
                        self.pause()
                    elif eventos.key == K_SPACE:
                        self.bugueado = 0
                        self.playing = True
                    elif eventos.key == K_r:
                        if not self.fan_lvl_bool:self.start(self.lvl)
                        else: self.start_fan_lvl(self.lvl_fan)
                    elif eventos.key == K_LEFT or eventos.key == K_a:
                        self.player.left = True
                    elif eventos.key == pag.K_RIGHT or eventos.key == K_d:
                        self.player.right = True
                elif eventos.type == pag.KEYUP:
                    if eventos.key == K_LEFT or eventos.key == K_a:
                        self.player.left = False
                    elif eventos.key == pag.K_RIGHT or eventos.key == K_d:
                        self.player.right = False
                elif eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    if self.boton_game_over.rect.collidepoint(eventos.pos) and not self.alive:
                        if not self.fan_lvl_bool:self.start(self.lvl)
                        else: self.start_fan_lvl()
                    if self.boton_win.rect.collidepoint(eventos.pos) and self.win:
                        if not self.fan_lvl_bool:
                            self.lvl += 1
                            self.start(self.lvl)
                        else:
                            self.title_screen = True
                            self.Pantalla_de_titulo()

                            

            # -------------------------------------------------------  Logica   ------------------------------------------
            self.check_loss()

            if len(self.bloques) > 6 and not self.ball.lenta and not self.ball.rapida:
                self.deltatime_ball.FPS = self.framerate_dificultad
            elif (distancia := Hipotenuza(self.bloques[-1]['rect'].center, self.ball.rect.center)) < 170:
                self.deltatime_ball.FPS = max(10,(distancia/170)*self.framerate_dificultad)
                if distancia < 80 and not self.acercandose:
                    self.sounds.casi.play()
                    self.acercandose = True
            elif self.acercandose:
                self.acercandose = False

                
            for i,tra in sorted(enumerate(self.cubic_bezier_transitions),reverse= True):
                vec = tra['transition'].update()
                if vec != True:
                    if tra['afectado'] == 'player':
                        tra['transition'].move([(self.player.rect2.centerx, 650), (self.player.rect2.centerx, 650 + 15), (self.player.rect2.centerx, 650)])
                        self.player.rect2.center = vec
                    elif tra['afectado'] == 'ball':
                        self.deltatime_ball.FPS = vec[1]
                    else:
                        self.bloques[tra['afectado']]['rect'].center = vec
                else:
                    self.cubic_bezier_transitions.pop(i)


            if not self.win and self.alive and self.playing:
                self.bugueado += 1
            if self.bugueado > 10*self.framerate_general:
                self.ball.set_pos((self.ventana_rect.centerx,self.ventana_rect.centery * 1.7))
                self.ball.set_vel([0,-4])
                self.playing = False


                        # -----------------------------------Dibujar --------------------------------------

            self.draw_effects(self.effects_before)

            if not self.low_detail_mode:
                self.particles_ball.update(self.ball.pos)
                self.particles_ball.draw()

            for alala in self.bloques[1:]:
                pag.draw.rect(self.ventana, alala['color'], alala['rect'], border_radius= alala['border_radius'])

            if not self.low_detail_mode:
                self.player.draw2()
            self.player.draw()

            if self.ball.rect.left>self.ventana_rect.w or self.ball.rect.top>self.ventana_rect.h or self.ball.rect.right<0 or self.ball.rect.bottom<0:
                self.bugueado = 0
                self.a_reiniciar.draw(self.ventana)

            if len(self.bloques) == 5:
                if not self.win:
                    self.win = True
                    self.sounds.lvl_clear.play()
                self.text_win.draw(self.ventana)
                self.boton_win.draw(self.ventana)
                if self.efecto_win.update():
                    self.efecto_win = Effect(3,(random.randint(50,self.ventana_rect.w-50),random.randint(50,self.ventana_rect.h-50)),self.ventana, 50)
                
                self.efecto_win.draw()
            elif self.alive:
                if self.playing:
                    self.ball.update(self.deltatime_ball.dt)
                    self.ball.draw()
                    self.colicion()
                else:
                    self.text_press_space.draw(self.ventana)
                self.player.move(self.deltatime.dt)
            else:
                self.text_game_over.draw(self.ventana)
                self.boton_game_over.draw(self.ventana)
        
            for x in self.texts_main_list:
                x.update()
                x.draw(self.ventana)

            for i, spark in sorted(enumerate(self.sparks), reverse=True):
                spark.move(self.deltatime.dt)
                spark.draw(self.ventana)
                if not spark.alive:
                    self.sparks.pop(i)

            for i,p in sorted(enumerate(self.powers),reverse= True):
                p.move(self.deltatime.dt)
                p_c = p.colicion(self.bloques_rects[:5])
                if p_c == 'Destroy':
                    self.powers.pop(i)
                elif p_c == True:
                    self.appli_powerup(p.type)
                    self.powers.pop(i)
                p.draw()
                
            self.draw_effects(self.effects_after)


            for i,text in sorted(enumerate(self.float_texts_list),reverse= True):
                if text.update():
                    self.float_texts_list.pop(i)
                text.draw()


            if self.lvl > 9:
                self.text_ganaste.draw(self.ventana)

            pag.display.flip()
            self.relog.tick(self.framerate_general)


if __name__=='__main__':
    BrickBricker()