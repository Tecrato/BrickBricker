import pygame as pag, random, sys, numpy, sqlite3, json, os, shutil
from concurrent.futures import ThreadPoolExecutor
from pygame._sdl2 import messagebox
from pygame.locals import *
from io import open
from platformdirs import *
from Utilidades import *

appdata = user_data_dir('save', 'BrickBreacker', roaming=True)
try:
    os.mkdir('/'.join(appdata.split('\\')[:-1]))
except:
    pass
try:
    os.mkdir(appdata)
except:
    pass



from balls import Ball
from background import Background
from Barras_verticales import Vertical_bars
from effects import Effect
from floating_text import Float_text
from funcs import Botons_functions
from game_over import Game_over
from music import Set_music
from player import Player
from powers import PowerUp
from snake import Snake
from sound import Set_sounds
from win import Win


class BrickBricker(Botons_functions):
    """
    1329

    hacer sombras con las mascaras

    Ideas para niveles
        - Incluir ladrillos irrompibles
    """
    def __init__(self) -> None:
        pag.init()


        #Ventana
        self.ventana = pag.display.set_mode((800,700), SCALED|RESIZABLE|DOUBLEBUF|HWSURFACE)
        self.ventana_rect = self.ventana.get_rect()
        pag.display.set_caption('BrickBreacker')
        pag.display.set_icon(pag.image.load('Screenshot_10.ico'))

        
        #Variedad en las variables
        self.hilos = ThreadPoolExecutor(2)

        self.life = 3
        self.lvl = 1
        self.lvl_fan = ''
        self.lvl_max = 1
        self.score = 0
        self.mulpliquer = 0
        self.bugueado = 0
        self.all_inputs = []
        self.bloques = []
        self.bloques_rects = []
        self.cubic_bezier_transitions = []
        self.effects_after = []
        self.effects_before = []
        self.float_texts_list = []
        self.powers = []
        self.sparks = []
        self.acercandose = False
        self.alive = True
        self.bool_final_lvl = False
        self.bool_title_confirm = False
        self.Drop_event_bool = False
        self.fan_lvl_bool = False
        self.low_detail_mode = False
        self.options_while = False
        self.pausado = False
        self.playing = False
        self.title_fan_lvls_bool = False
        self.title_screen = True
        self.win = False
        self.relog = pag.time.Clock()
        self.framerate_general = 60
        self.framerate_dificultad = 90

        self.txt = Create_text('Cargando 0%',50,None,(400,350),self.ventana,color='white',padding=100,with_rect=True)
        self.txt.draw()
        pag.display.flip()


        self.inilializar_juego()
        
        self.txt.change_text('Cargando 90%')
        self.txt.draw()
        pag.display.flip()

        pag.mixer_music.set_volume(0)
        self.load_json()
        pag.mixer_music.set_volume(self.json["music_volumen"])

        del self.txt

        self.Pantalla_de_titulo()
        self.Main_Process()

    def inilializar_juego(self) -> None:

        #Leer base de datos
        self.base_de_datos = sqlite3.connect(appdata+'/'+'lvls.sqlite3')
        self.cursor = self.base_de_datos.cursor()
        try:
            self.cursor.execute("SELECT * FROM FAN_LVLS")
        except:
            self.base_de_datos.close()
            os.remove(appdata+'/'+'lvls.sqlite3')
            shutil.copy('./lvls.sqlite3',appdata+'/'+'lvls.sqlite3')
            self.base_de_datos = sqlite3.connect(appdata+'/'+'lvls.sqlite3')
            self.cursor = self.base_de_datos.cursor()

        #Fuentes
        self.fuente_orbi_medium = 'Assets/Fuentes/Orbitron-Medium.ttf'
        self.fuente_orbi_extrabold = 'Assets/Fuentes/Orbitron-ExtraBold.ttf'
        self.fuente_consolas = 'Assets/Fuentes/consola.ttf'
        self.fuente_simbolos = 'Assets/Fuentes/Symbols.ttf'

        #Variable Musica/Sonidos
        self.music_var = Set_music()
        self.sounds = Set_sounds()
        self.sounds.set_volumen(.5)


        #Textos
                                                #Del proceso principal
        self.life_text = Create_text('lives', 30, self.fuente_orbi_medium, (70,40), self.ventana, 'center')
        self.score_text = Create_text('Score 0', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx - 60,40), self.ventana)
        self.lvl_text = Create_text('lvl 1 ', 30, self.fuente_orbi_medium, (self.ventana_rect.w ,40), self.ventana, 'right')

        self.a_reiniciar = Create_text('Se ha Bugueado :V', 50, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery), self.ventana)
        self.a_reiniciar2 = Create_text('Debes reiniciar con "R"', 40, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery + self.a_reiniciar.rect.h), self.ventana)

        self.text_press_space = Create_text('Presiona espacio para comenzar', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.3), self.ventana)
        
        self.txt.change_text('Cargando 14%')
        self.txt.draw()
        pag.display.flip()
                                                #De la pantalla de titulo
        self.title_text = Create_text('BrickBricker', 50, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery * .5), self.ventana)
        self.boton_reanudar = Create_boton('Reanudar', 35, self.fuente_orbi_medium, (-500,-500), self.ventana, 0, color='white', with_rect=False, func=self.func_reanudar)
        self.boton_jugar = Create_boton('Jugar', 35, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.0), self.ventana, 0, color='white', with_rect=False,func=self.func_jugar)
        self.boton_fan_lvls = Create_boton('', 30, self.fuente_simbolos, (self.boton_jugar.rect.right + 20,self.boton_jugar.rect.centery), self.ventana, 0, color='white', with_rect=False,func=self.func_fan_lvls_title)
        self.options_text_title = Create_boton('Opciones', 35, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.15), self.ventana, 0, color='white', with_rect=False,func=self.func_opciones)
        self.salir_text_title = Create_boton('Cerrar', 35, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.3), self.ventana, 0,color='white',color_active='darkgrey', with_rect=False)
        self.salir_text_title.smothmove(1/60, 1, 0.73, 2)
        self.boton_extras = Create_boton('', 40, self.fuente_simbolos, (0,self.ventana_rect.h-20), self.ventana, dire='left', color='white', with_rect=False,func=self.func_extras)
        

                                                #Del menu de opciones
        self.title_dificult = Create_text('Dificultad', 40, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery * .9), self.ventana)
        self.title_easy = Create_boton('Fácil', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1), self.ventana, 0, color='white',color_active='red', with_rect=False,func=lambda:self.func_change_difficult(1))
        self.title_medium = Create_boton('Medio', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.13), self.ventana, 0, color='white',color_active='red', with_rect=False ,func=lambda:self.func_change_difficult(2))
        self.title_hard = Create_boton('Difícil', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.26), self.ventana, 0, color='white',color_active='red', with_rect=False,func=lambda:self.func_change_difficult(3))
        self.button_load_music = Create_boton('Cargar musica', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.38), self.ventana, 0,func=lambda:self.func_drop_music_file())


        self.text_low_detail_mode = Create_boton('Low Detail Mode: X', 20, self.fuente_orbi_medium, (0,self.ventana_rect.h), self.ventana, 40, 'bottomleft', 'white', with_rect=False, func= self.func_low_detail_mode)
        self.button_toggle_fullscreen = Create_boton('', 30, self.fuente_simbolos, (30,self.text_low_detail_mode.rect.top), self.ventana, 0, dire='bottomleft',func=self.func_fullscreen)
        self.button_del_progress = Create_boton('Borrar Progreso actual', 30, self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery * 1.50), self.ventana, 0,func=lambda:self.func_del_progress(appdata))

        self.lista_cosa=List_Box((220,500),self.ventana,(580,20), None,smothscroll= True,background_color='black',padding_left= 0,padding_top=0,header=True, text_header='Canciones', header_top_left_radius=0, header_top_right_radius=0)


                                                #De la pausa
        self.pausa_text = Create_text('Pausado', 50, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery * .8), self.ventana, 'center', border_radius=10, with_rect=True)
        self.pausa_text_X = Create_boton('Salir', 40, self.fuente_orbi_extrabold, (self.ventana_rect.w - 20,20), self.ventana,20, 'topright', 'white', with_rect=True,color_rect='black', border_radius=40,func=self.func_pause_X)


                                                #Del menu de confirmacion
        self.text_title_confirm = Create_text(['Coloque \"si\"','si esta segur@'], 25, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery-70), self.ventana, 'center', 'black')
        self.input_confirm = Input_text(self.ventana, (self.ventana_rect.centerx-95,self.ventana_rect.centery+10), (25,200), None, 'confirmacion')
        self.all_inputs.append(self.input_confirm)

        self.rect_title_confirm = pag.rect.Rect(0,0,300,250)
        self.rect_title_confirm.center = self.ventana_rect.center
        
        self.txt.change_text('Cargando 28%')
        self.txt.draw()
        pag.display.flip()

                                                #La pantalla de niveles creados
        self.text_created_lvls = Create_text('Created lvls', 40, self.fuente_orbi_medium, (self.ventana_rect.centerx, 10), self.ventana, 'top')
        self.boton_seleccionar = Create_boton('Seleccionar',22,self.fuente_orbi_medium,(350,105),self.ventana,15,'topleft','black',border_radius=15, toggle_rect=True)
        self.boton_borrar = Create_boton('Eliminar',22,self.fuente_orbi_medium,(600,105),self.ventana,15,'topleft','black',border_radius=15, toggle_rect=True)
        self.lista_fans_lvls= Multi_list((self.ventana_rect.width*.8, self.ventana_rect.height*.8), self.ventana,
            (self.ventana_rect.width*.1, self.ventana_rect.height*.15), 2, None, 30, padding_left=13, header_text=['Id','Nombre'], colums_witdh=[0,.10])


                                                #Del menu de extras
        self.extras_nombre = Create_text(['Created','by','Edouard Sandoval'], 45, self.fuente_orbi_extrabold, (self.ventana_rect.centerx,self.ventana_rect.centery * .5), self.ventana)
        self.extras_version = Create_text('Version 1.4.5',30,self.fuente_orbi_medium, (self.ventana_rect.centerx,self.ventana_rect.centery), self.ventana)

        #Limites
        self.limite_inferior = pag.rect.Rect(0, self.ventana_rect.height-15, self.ventana_rect.width, 50)
        self.limite_superior = pag.rect.Rect(-50, -47, self.ventana_rect.width+150, 50)
        self.limite_derecho = pag.rect.Rect(self.ventana_rect.width-2, -50, 50, self.ventana_rect.height+100)
        self.limite_izquierdo = pag.rect.Rect(-48, -50, 50, self.ventana_rect.height+100)

        #Jugador
        self.player = Player((350,650), 100, 3.4, self.ventana, (0, self.ventana_rect.w))

        #Bola
        self.ball = Ball((self.ventana_rect.centerx,self.ventana_rect.centery * 1.7), 10, self.ventana, [0,0])

        #Serpiente
        self.Serpiente = Snake(self.ventana)

        #Musica
        self.boton_musica_musica = Create_text('♫', 40, self.fuente_consolas, (25,40), self.ventana, padding=(20,0), with_rect=True)
        self.text_song = Create_text('\"Song\"', 20, self.fuente_consolas, (40,40), self.ventana, 'left', 'white', True, (0,0,0,255))
        self.boton_next_musica = Create_boton('', 20, self.fuente_simbolos, (self.ventana_rect.w-20,self.ventana_rect.h - 120 - 30), self.ventana, 10, func=self.func_music_next)
        self.boton_pause_musica = Create_boton('', 20, self.fuente_simbolos, (self.ventana_rect.w-50,self.ventana_rect.h - 120 - 30), self.ventana, 10,func=self.func_music_pause)
        self.boton_retry_musica = Create_boton('', 20, self.fuente_simbolos, (self.ventana_rect.w-80,self.ventana_rect.h - 120 - 30), self.ventana, 10,func=self.func_music_retry)
        self.boton_random_musica = Create_boton('列', 20, self.fuente_simbolos, (self.ventana_rect.w-110,self.ventana_rect.h - 120 - 30), self.ventana, 10,func=self.func_music_random)

        self.BV_Volumen_Musica = Vertical_bars((self.ventana_rect.w - 30, self.ventana_rect.h - 30), self.ventana, 100)
        self.BV_Volumen_Musica_press = False
        self.text_musica_vertical = Create_text(['M','u','s','i','c'], 20, self.fuente_consolas, (self.ventana_rect.w-50,self.ventana_rect.h - 120), self.ventana)

        self.BV_Volumen_Sonidos = Vertical_bars((self.ventana_rect.w - 80, self.ventana_rect.h - 30), self.ventana, 100)
        self.BV_Volumen_Sonidos_press = False
        self.text_sonido_vertical = Create_text(['S','o','u','n','d'], 20, self.fuente_consolas, (self.ventana_rect.w-100,self.ventana_rect.h - 120), self.ventana)

        self.txt.change_text('Cargando 42%')
        self.txt.draw()
        pag.display.flip()

        #Cosas ... nose
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

        self.texts_options_list = [self.title_text,self.title_dificult,self.salir_text_title]
        self.texts_options_list.extend(self.texts_song_list)
        self.botones_options_list = [self.button_load_music,self.title_easy,self.title_medium,self.title_hard,self.text_low_detail_mode
                                     ,self.button_del_progress,self.button_toggle_fullscreen,self.boton_next_musica,self.boton_retry_musica,self.boton_pause_musica, self.boton_random_musica]
        # self.botones_options_list.extend()

        [x.change_color_ad('white','darkgrey') for x in self.botones_options_list]
        
        for y,z in zip(self.botones_options_list,self.botones_title_list):
            y.change_color_ad('white','darkgrey')
            z.change_color_ad('white','darkgrey')

            y.sound_to_click = self.sounds.boton1
            z.sound_to_click = self.sounds.boton1
        
        self.txt.change_text('Cargando 56%')
        self.txt.draw()
        pag.display.flip()
        
        for x in self.botones_song_list:
            x.with_rect = False
        for x in self.botones_options_list:
            x.with_rect = False

        self.txt.change_text('Cargando 70%')
        self.txt.draw()
        pag.display.flip()

        self.game_over = Game_over(self.ventana)
        self.lvl_clear = Win(self.ventana)
        self.particles_ball = Particles(self.ventana, 2)
        self.background = Background(self.ventana,(800,700),2)
        self.background2 = Background(self.ventana,(800,700),3)
        self.deltatime = Deltatime(90)
        self.deltatime_ball = Deltatime(90)

        self.text_ganaste=Create_text(['Haz Ganado el juego','Gracias por jugar'],40,self.fuente_orbi_medium,(self.ventana_rect.centerx,self.ventana_rect.centery-50),self.ventana,'center','white')

        self.txt.change_text('Cargando 84%')
        self.txt.draw()
        pag.display.flip()
        self.reload_list_for_fans_lvls()

    def load_json(self) -> None:
        #A hora con la posibilidad de guardar datos en un archivo json, el mundo es mas bonito
        try:
            self.json = json.load(open(appdata+'/' + 'progress.json', 'r'))
        except:
            self.json = {}

        # Para el nivel maximo
        try:
            self.lvl_max = self.json["lvlLimit"]
            if self.lvl_max > 1: self.boton_reanudar.move((self.ventana_rect.centerx,self.ventana_rect.centery * .85))
        except Exception as e:
            self.json["lvlLimit"] = 1

        try:
            self.json["lvl_scores"]
        except Exception as e:
            self.json["lvl_scores"] = {}
        try:
            self.json["fan_lvl_scores"]
        except Exception as e:
            self.json["fan_lvl_scores"] = {}

        # Para el "Aleatorio" en la musica
        try:
            if self.json["music_random"]:
                self.boton_random_musica.change_text('列')
            else:
                self.boton_random_musica.change_text('')
            self.music_var.random(self.json["music_random"])
        except:
            self.json["music_random"] = True

        # El directorio de la musica
        try:
            if self.json["music_dir"] != None and self.json["music_dir"] != '':
                p = self.music_var.load_music(self.json["music_dir"])
                self.text_song.change_text(p['text'])
                if len(self.music_var.canciones) > 0:
                    self.lista_cosa.change_list(self.music_var.canciones)
                    self.lista_cosa.select(p['index'])
        except:
            self.json["music_dir"] = None

        # Si la musica esta pausada
        try:
            if self.json["music_pause"] == True:
                self.music_var.pause(True)
                self.boton_pause_musica.change_text('')
            else:
                self.boton_pause_musica.change_text('')
        except:
            self.json["music_pause"] = False
        

        # Para rendimientos bajos
        try:
            self.low_detail_mode = self.json['low_detail']
        except:
            self.json['low_detail'] = self.low_detail_mode
            if self.low_detail_mode:
                self.text_low_detail_mode.change_text('Low Detail Mode: O')
            else:
                self.text_low_detail_mode.change_text('Low Detail Mode: X')

        #El volumen de la musica
        try:
            self.BV_Volumen_Musica.set_volumen(self.json["music_volumen"])
        except:
            self.json["music_volumen"] = .5
        #El volumen de los sonidos
        try:
            self.BV_Volumen_Sonidos.set_volumen(self.json["sound_volumen"])
            self.sounds.set_volumen(self.json["sound_volumen"])
        except:
            self.json["sound_volumen"] = .5
        # El nivel de dificultad
        try:
            self.func_change_difficult(self.json['difficult'])
        except:
            self.json["difficult"] = 2
            self.func_change_difficult(2)
        self.savejson()

    def savejson(self) -> None:
        json.dump(self.json, open(appdata+'/'+'progress.json', 'w'))



    def colicion(self) -> None:
        choque = self.ball.rect.collidelist(self.bloques_rects)
        if choque > 0:
            self.ball.retroceder(self.deltatime_ball.dt)
            self.ball.update(.5)
            choque = self.ball.rect.collidelist(self.bloques_rects)
        try:
            if choque2 := self.ball.rect.collidelistall(self.bloques_rects):
                b1 = Hipotenuza(self.ball.rect.center,self.bloques[choque]['rect'].center)
                b2 = Hipotenuza(self.ball.rect.center,self.bloques[choque2[1]]['rect'].center)
                if b1 > b2: choque = choque2[1]
                else: choque = choque
        except Exception as e:
            pass

        if choque == 0:
            self.ball.pos = (self.ball.pos[0]-self.ball.vel[0],self.player.rect2.top - 5)
            angle = Angulo(self.player.rect.center, self.ball.rect.center)
            self.ball.vel = [numpy.cos(numpy.radians(angle))*Hipotenuza((0,0), self.ball.vel),numpy.sin(numpy.radians(angle))*Hipotenuza((0,0), self.ball.vel)]
            self.mulpliquer = 0
            self.bugueado = 0
            if not self.low_detail_mode:
                for x in range(15):
                    self.sparks.append(Spark(self.ventana, (self.ball.rect.centerx,650), numpy.radians(random.randint(230, 340)),random.randint(1, 4),(255, 255, 255),.6))
        elif choque > 0:
            if choque == 4:
                self.life -= 1
                self.life_text.change_text(f'Lives {self.life}')
                if self.life > 0:
                    self.sounds.ball_colicion.play()
                    self.effects_after.append(Effect(4,(0,0),self.ventana,self.ventana_rect.size))
                self.mulpliquer = 0
            elif choque > 4:
                self.bugueado = 0
                self.mulpliquer += 1
                self.score += 100 * self.mulpliquer
                self.score_text.change_text(f'Score {self.score}')
                if  self.bloques[choque]['power']:
                    self.powers.append(PowerUp(self.ventana, self.bloques[choque]['rect'].center, self.bloques[choque]['power'], 25))
                if not self.low_detail_mode:
                    self.float_texts_list.append(Float_text(f'+{100*self.mulpliquer} X {self.mulpliquer}',20,'Assets/Fuentes/mononoki Bold Nerd Font Complete Mono.ttf',self.bloques[choque]['rect'].center,self.ventana))
                
            if self.bloques[choque]['border_radius'] == 10000:
                angle = Angulo(self.bloques[choque]['rect'].center, self.ball.rect.center)
                self.ball.vel=Vector2(numpy.cos(numpy.radians(angle))*Hipotenuza((0,0),self.ball.vel),numpy.sin(numpy.radians(angle))*Hipotenuza((0,0),self.ball.vel))
            else:
                if (self.ball.rect.centery < self.bloques[choque]['rect'].top and self.ball.vel[1] > 0) or (
                    self.ball.rect.centery > self.bloques[choque]['rect'].bottom and self.ball.vel[1] < 0):
                    self.ball.vel[1] *= -1
                if (self.ball.rect.centerx < self.bloques[choque]['rect'].left and self.ball.vel[0] > 0) or (
                    self.ball.rect.centerx > self.bloques[choque]['rect'].right and self.ball.vel[0] < 0):
                    self.ball.vel[0] *= -1

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
                        self.score_text.change_text(f'Score {self.score}')
                        if x['power']:
                            self.powers.append(PowerUp(self.ventana, x['rect'].center, x['power'], 25))
                        if not self.low_detail_mode:
                            self.float_texts_list.append(Float_text(f'+{100*self.mulpliquer} X {self.mulpliquer}',20,'Assets/Fuentes/mononoki Bold Nerd Font Complete Mono.ttf',x['rect'].center,self.ventana))
                        self.bloques.pop(i)
            else: self.bloques.remove(self.bloques[choque])
            self.sounds.ball_pop.play()
            self.update_bloques_rects()

    def draw_effects_before(self) -> None:
        if len(self.effects_before) < 1:
            return
        for i,x in sorted(enumerate(self.effects_before), reverse=True):
            if x.update():
                self.effects_before.pop(i)
        for x in self.effects_before:
            x.draw()
    def draw_effects_after(self) -> None:
        if len(self.effects_after) < 1:
            return
        for i,x in sorted(enumerate(self.effects_after), reverse=True):
            if x.update():
                self.effects_after.pop(i)
        for x in self.effects_after:
            x.draw()

    def update_bloques_rects(self) -> None:
        for b in self.bloques:
            try:
                b['power']
                if b['power'] == None: raise Exception('No tiene')
            except Exception as e:
                if random.randrange(0,10000) < 700:
                    b['power'] = random.randint(1,6)
                else:
                    b['power'] = 0
        self.bloques_rects.clear()
        for d in self.bloques:
            self.bloques_rects.append(d['rect'])

    def load_lvl_to_DB(self,name) -> None:
        self.cursor.execute("SELECT * FROM {n}".format(n=name))
        datos = self.cursor.fetchall()

        for rect, effect, color, border_radius in datos:
            r = rect.replace('(', '').replace(')', '').split(',')
            c = color.replace('(','').replace(')','').split(',')
            self.bloques.append({'rect': pag.rect.Rect(int(r[0]),int(r[1]),int(r[2]),int(r[3])), 'effect': effect, 'color': (round(float(c[0])),round(float(c[1])),round(float(c[2]))), 'border_radius': border_radius})

    def start(self, lvl: int) -> None:

        self.life = 3
        self.score = 0
        self.bugueado = 0
        self.mulpliquer = 0
        self.life_text.change_text(f'Lives {self.life}')
        self.lvl_text.change_text(f'Nivel: {self.lvl}')
        self.score_text.change_text('Score 0')
        self.ball.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * 1.7)
        self.ball.vel = [0,-4]
        self.ball.update()
        self.particles_ball.clear()
        self.particles_ball.con = 0
        self.player.rect.topleft = (350,650)
        self.limite_inferior.top = self.ventana_rect.height-15

        self.lvl_max = max(self.lvl, self.lvl_max)
        self.json["lvlLimit"] = max(self.json["lvlLimit"], self.lvl_max)
        if self.lvl_max > 1: self.boton_reanudar.move((self.ventana_rect.centerx,self.ventana_rect.centery * .85))
        self.savejson()

        self.fan_lvl_bool = False
        self.playing = False
        self.alive = True
        self.win = False

        self.cubic_bezier_transitions.clear()
        self.reset()


        self.bloques.clear()
        self.bloques.append({'rect': self.player.rect2, 'effect': 1, 'color': 'green', 'border_radius': 0, 'power':None})
        self.bloques.append({'rect': self.limite_derecho, 'effect': 0, 'color': 'grey', 'border_radius': 0, 'power':None})
        self.bloques.append({'rect': self.limite_izquierdo, 'effect': 0, 'color': 'grey', 'border_radius': 0, 'power':None})
        self.bloques.append({'rect': self.limite_superior, 'effect': 0, 'color': 'grey', 'border_radius': 0, 'power':None})
        self.bloques.append({'rect': self.limite_inferior, 'effect': 1, 'color': 'red', 'border_radius': 0, 'power':None})
        if lvl == 1:
            for x in range(3,10):
                self.bloques.append({'rect': pag.rect.Rect(52*x + 80,22*6 + 100, 50, 20), 'effect': 2, 'color': (random.random()*255,random.random()*255,random.random()*255), 'border_radius': 0})
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
                        self.bloques.append({'rect': pag.rect.Rect(52 * x + 80,22 * y + 100, 50, 20), 'effect': 2, 'color': color, 'border_radius': 0})
        elif lvl == 3:
            for y in range(5):
                color = (random.random()*255,random.random()*255,random.random()*255)
                for x in range(10):
                    self.bloques.append({'rect': pag.rect.Rect(62 * x + 80,50 * y + 100, 60, 20), 'effect': 2, 'color': color, 'border_radius': 0})
        elif lvl == 4:
            self.load_lvl_to_DB('espadaminecraft')
        elif lvl == 5:
            self.load_lvl_to_DB('prueba2')
        elif lvl == 6:
            self.load_lvl_to_DB('circulos')
        elif lvl == 7:
            self.load_lvl_to_DB('paisaje1')
        elif lvl == 8:
            self.load_lvl_to_DB('rosa')
        elif lvl == 9:
            self.load_lvl_to_DB('interpolacion')
        else:
            y = 6
            color = (random.random()*255,random.random()*255,random.random()*255)
            for x in range(3,10):
                self.bloques.append({'rect': pag.rect.Rect(52 * x + 80,22 * y + 100, 50, 20), 'effect': 2, 'color': color, 'border_radius': 0})

        self.update_bloques_rects()

    def start_fan_lvl(self, lvl: str) -> None:

        self.lvl = 1
        self.life = 3
        self.score = 0
        self.bugueado = 0
        self.mulpliquer = 0
        self.life_text.change_text(f'Lives 3')
        self.lvl_text.change_text(f'Nivel: {self.lvl_fan}')
        self.score_text.change_text(f'Score 0')
        self.ball.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * 1.7)
        self.ball.vel = [0,-4]
        self.ball.update()
        self.particles_ball.clear()
        self.particles_ball.con = 0
        self.player.rect.topleft = (350,650)
        self.limite_inferior.top = self.ventana_rect.height-15

        self.fan_lvl_bool = True
        self.alive = True
        self.playing = False
        self.win = False

        self.powers.clear()
        self.cubic_bezier_transitions.clear()
        self.deltatime.FPS = self.framerate_dificultad
        self.deltatime_ball.FPS = self.framerate_dificultad
        pag.time.set_timer(USEREVENT+1,500000000,1)
        pag.time.set_timer(USEREVENT+2,500000000,1)
        self.ball.rapida = False
        self.ball.lenta = False

        self.bloques.clear()
        self.bloques.append({'rect': self.player.rect2, 'effect': 1, 'color': 'green', 'border_radius': 0})
        self.bloques.append({'rect': self.limite_derecho, 'effect': 0, 'color': 'grey', 'border_radius': 0})
        self.bloques.append({'rect': self.limite_izquierdo, 'effect': 0, 'color': 'grey', 'border_radius': 0})
        self.bloques.append({'rect': self.limite_superior, 'effect': 0, 'color': 'grey', 'border_radius': 0})
        self.bloques.append({'rect': self.limite_inferior, 'effect': 1, 'color': 'red', 'border_radius': 0})

        self.cursor.execute("SELECT * FROM {}".format(lvl))

        for rect, effect, color, border_radius, power in self.cursor.fetchall():
            r = rect.replace('(', '').replace(')', '').split(',')
            c = color.replace('(','').replace(')','').split(',')
            self.bloques.append({'rect': pag.rect.Rect(int(r[0]),int(r[1]),int(r[2]),int(r[3])), 'effect': effect, 'color': (round(float(c[0])),round(float(c[1])),round(float(c[2]))), 'border_radius': border_radius, 'power': power})
        self.update_bloques_rects()

    def eventos_en_comun(self, e) -> None:
        if not self.low_detail_mode: self.background.draw()
        else: self.ventana.fill('black')

        for event in e:
            if event.type == QUIT:
                pag.quit()
                self.hilos.shutdown()
                sys.exit()
            elif event.type == 50000:
                self.hilos.submit(self.cambiar_musica, 'change')
            elif event.type == KEYDOWN:
                if event.key == K_F2 and len(self.music_var.canciones) > 0:
                    self.hilos.submit(self.cambiar_musica, 'change')
                elif event.key == K_F11:
                    pag.display.toggle_fullscreen()

    def cambiar_musica(self, acc: str) -> None:
        if acc == 'change':
            p = self.music_var.change()
            self.text_song.change_text(p['text'])
            self.lista_cosa.select(p['index'])

    def reload_list_for_fans_lvls(self) -> None:
        self.cursor.execute("SELECT * FROM FAN_LVLS")
        perfiles = self.cursor.fetchall()
        perfiles.sort()

        self.lista_fans_lvls.change_list([[x[0] for x in perfiles],[x[1] for x in perfiles]])

    def delete_table_in_list_for_fans_lvls(self) -> None:
        if self.lvl_fan == '' or self.lvl_fan == None or self.lvl_fan == False:
            return False

        try:
            self.cursor.execute("DELETE FROM FAN_LVLS WHERE NOMBRE=?",[self.lvl_fan])
        except Exception as e:
            messagebox(
                "Error",
                "A ocurrido un error al eliminar el nivel",
                info=False,
                error=1,
                buttons=("Ok",),
                return_button=1,
                escape_button=1,
            )
        try:
            self.cursor.execute("DROP TABLE {}".format(self.lvl_fan))
        except Exception as e:
            messagebox(
                "Error",
                "A ocurrido un error al eliminar la tabla del nivel",
                info=False,
                error=1,
                buttons=("Ok",),
                return_button=1,
                escape_button=1,
            )
        self.lvl_fan = ''
        self.base_de_datos.commit()
        self.reload_list_for_fans_lvls()

    def appli_powerup(self, type) -> None:
        if type == 1:
            self.life += 1
            self.life_text.change_text(f'Lives {self.life}')
            self.effects_after.append(Effect(4,(0,0),self.ventana,self.ventana_rect.size, color=(0,100,0)))
            self.sounds.extra_life.play()
        if type == 2:
            self.mulpliquer += 1
            self.score += 100 * self.mulpliquer+10
            self.score_text.change_text(f'Score {self.score}')
            if not self.low_detail_mode:
                self.float_texts_list.append(Float_text(f'+{100*self.mulpliquer} X {self.mulpliquer}',20,'Assets/Fuentes/mononoki Bold Nerd Font Complete Mono.ttf',self.player.rect2.center,self.ventana))
            self.sounds.money.play()
        elif type == 3:
            self.ball.explocion = True
        elif type == 4 and not self.ball.rapida:
            self.ball.lenta = True
            self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(30, [(0,self.framerate_dificultad), (0,self.framerate_dificultad/2)]), 'afectado': 'ball'})
            pag.time.set_timer(USEREVENT+1,5000,1)
            self.sounds.slow.play()
        elif type == 5 and not self.ball.lenta:
            self.ball.rapida = True
            self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(30, [(0,self.framerate_dificultad), (0,self.framerate_dificultad*2)]), 'afectado': 'ball'})
            pag.time.set_timer(USEREVENT+2,5000,1)
            self.sounds.fast.play()
        elif type == 6:
            self.life -= 1
            self.life_text.change_text(f'Lives {self.life}')
            if self.life > 0:
                self.sounds.ball_colicion.play()
                self.effects_after.append(Effect(4,(0,0),self.ventana,self.ventana_rect.size))

    def reset(self) -> None:
        self.powers.clear()
        self.float_texts_list.clear()
        self.deltatime.FPS = self.framerate_dificultad
        self.deltatime_ball.FPS = self.framerate_dificultad
        for i,tra in sorted(enumerate(self.cubic_bezier_transitions),reverse= True):
            if tra['afectado'] == 'ball':
                self.cubic_bezier_transitions.pop(i)
        pag.time.set_timer(USEREVENT+1,500000000,1)
        pag.time.set_timer(USEREVENT+2,500000000,1)
        self.ball.rapida = False
        self.ball.lenta = False

    def loss(self) -> bool:
        if self.life <= 0 and self.alive == True:
            self.alive = False
            self.sounds.loss.play()
            self.reset()
            return True
        return False



    def title_confirm(self) -> None:
        self.input_confirm.typing = True
        while self.bool_title_confirm:

            self.eventos_en_comun(eventos := pag.event.get())

            #Para el input
            for en in self.all_inputs:
                if resultado := en.eventos_teclado(eventos) == "enter" and entradas[0].get_text() != "":
                    ecuaciones.append((formatear_texto(entradas[0].get_text()),entradas[1].get_text() if entradas[1].get_text() != '' else True))
                    print(ecuaciones)
            #Fin del input
            for eventos in eventos:
                if eventos.type == pag.KEYDOWN:
                    if eventos.key == K_ESCAPE:
                        self.bool_title_confirm = False
                    elif eventos.key == K_RETURN:
                        self.bool_title_confirm = False
                        if self.input_confirm.get_text().lower() == 'si':return True
                        else: return False
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    if self.pausa_text_X.rect.collidepoint(eventos.pos):
                        self.bool_title_confirm = False

            pag.draw.rect(self.ventana, 'lightgrey', self.rect_title_confirm, border_radius=20)
            self.text_title_confirm.draw()
            self.input_confirm.draw()
            self.pausa_text_X.draw()

            pag.display.flip()
            self.relog.tick(30)

    def title_extras(self) -> None:
        while self.bool_title_extras:
            self.eventos_en_comun(eventos := pag.event.get())

            for eventos in eventos:
                if eventos.type == KEYDOWN:
                    if eventos.key == K_ESCAPE:
                        self.bool_title_extras = False
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    if self.salir_text_title.rect.collidepoint(eventos.pos):
                        self.sounds.boton1.play()
                        self.salir_text_title.move((self.ventana_rect.centerx,self.ventana_rect.centery * 1.3))
                        self.bool_title_extras = False

            self.extras_nombre.draw()
            if not self.low_detail_mode:
                self.Serpiente.update()
                self.Serpiente.draw()
            self.salir_text_title.draw()
            self.extras_version.draw()

            pag.display.flip()
            self.relog.tick(60)

    def Pantalla_niveles_fans(self) -> None:
        while self.title_fan_lvls_bool:
            self.eventos_en_comun(eventos := pag.event.get())

            for eventos in eventos:
                if eventos.type == KEYDOWN:
                    if eventos.key == K_ESCAPE:
                        self.title_fan_lvls_bool = False
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    if self.lista_fans_lvls.rect.collidepoint(eventos.pos):
                        p = self.lista_fans_lvls.select()
                        if p:
                            self.lvl_fan = p[1]
                    if self.pausa_text_X.rect.collidepoint(eventos.pos):
                        self.title_fan_lvls_bool = False
                    if self.boton_seleccionar.rect.collidepoint(eventos.pos):
                        if self.lvl_fan:
                            self.title_screen = False
                            self.title_fan_lvls_bool = False
                            self.start_fan_lvl(self.lvl_fan)
                    if self.boton_borrar.rect.collidepoint(eventos.pos):
                        self.bool_title_confirm = True
                        if self.title_confirm():
                            self.delete_table_in_list_for_fans_lvls()
                elif eventos.type == MOUSEWHEEL and self.lista_fans_lvls.rect.collidepoint(pag.mouse.get_pos()):
                    self.lista_fans_lvls.rodar(eventos.y * 15)

                if eventos.type == MOUSEBUTTONUP:
                    self.lista_fans_lvls.scroll = False

            if not self.low_detail_mode:
                self.Serpiente.update()

            self.pausa_text_X.draw()
            self.text_created_lvls.draw()
            self.lista_fans_lvls.draw()
            self.boton_borrar.draw()
            self.boton_seleccionar.draw()
            

            pag.display.flip()
            self.relog.tick(60)

    def Pantalla_de_titulo(self) -> None:
        while self.title_screen:
            self.eventos_en_comun(eventos := pag.event.get())

            for eventos in eventos:
                if eventos.type == KEYDOWN:
                    if eventos.key == K_ESCAPE:
                        pag.quit()
                        sys.exit()
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    for b in self.botones_title_list:
                        if b.rect.collidepoint(eventos.pos):
                            b.click()
                    if self.salir_text_title.rect.collidepoint(eventos.pos):
                        self.sounds.boton1.play()
                        pag.time.set_timer(QUIT, 200)

            if not self.low_detail_mode:
                self.Serpiente.update()
                self.Serpiente.draw()

            [x.draw() for x in self.texts_title_list]
            [x.draw() for x in self.botones_title_list]
            

            pag.display.flip()
            self.relog.tick(60)

    def options_menu(self) -> None:
        self.options_while = True
        while self.options_while:
            self.eventos_en_comun(evento:=pag.event.get())

            for eventos in evento:
                if eventos.type == DROPFILE and self.Drop_event_bool:
                    self.button_load_music.change_color_ad('white','grey')
                    self.button_load_music.change_text('Cargar musica')
                    self.Drop_event_bool = False
                    p = self.music_var.load_music(eventos.file)
                    if not p:
                        continue
                    self.text_song.change_text(p['text'])
                    self.json["music_dir"] = self.music_var.music_dir
                    self.savejson()
                    if len(self.music_var.canciones) > 0:
                        self.lista_cosa.change_list(self.music_var.canciones)
                        self.lista_cosa.select(p['index'])
                if eventos.type == KEYDOWN:
                    if eventos.key == K_ESCAPE:
                        self.options_while = False
                        self.savejson()
                        self.salir_text_title.move((self.ventana_rect.centerx,self.ventana_rect.centery * 1.3))
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    if self.Drop_event_bool == True:
                        self.button_load_music.change_color_ad('white','grey')
                        self.button_load_music.change_text('Cargar musica')
                        self.Drop_event_bool = False


                    for b in self.botones_options_list:
                        if b.rect.collidepoint(eventos.pos):
                            b.click()

                    if self.salir_text_title.rect.collidepoint(eventos.pos):
                        self.sounds.boton1.play()
                        self.salir_text_title.move((self.ventana_rect.centerx,self.ventana_rect.centery * 1.3))
                        self.options_while = False
                        self.savejson()

                    elif self.BV_Volumen_Musica.rect2.collidepoint(eventos.pos):
                        self.BV_Volumen_Musica_press = True
                    elif self.BV_Volumen_Sonidos.rect2.collidepoint(eventos.pos):
                        self.BV_Volumen_Sonidos_press = True
                    elif self.lista_cosa.rect.collidepoint(eventos.pos):
                        p = self.lista_cosa.select()
                        if p and p != 'scrolling':
                            self.text_song.change_text(self.music_var.change(p['text'])['text'])
                elif eventos.type == MOUSEWHEEL and self.lista_cosa.rect.collidepoint(pag.mouse.get_pos()):
                    self.lista_cosa.rodar(eventos.y * 15)

                if eventos.type == MOUSEBUTTONUP:
                    self.BV_Volumen_Musica_press = False
                    self.BV_Volumen_Sonidos_press = False
                    self.lista_cosa.scroll = False

            #Barras de sonido
            if self.BV_Volumen_Sonidos_press:
                self.BV_Volumen_Sonidos.pulsando_volumen()
                self.sounds.set_volumen(self.BV_Volumen_Sonidos.volumen)
                self.json["sound_volumen"] = self.BV_Volumen_Sonidos.volumen
            if self.BV_Volumen_Musica_press:
                self.BV_Volumen_Musica.pulsando_volumen()
                pag.mixer_music.set_volume(self.BV_Volumen_Musica.volumen)
                self.json["music_volumen"] = self.BV_Volumen_Musica.volumen


            self.lista_cosa.draw()

            if not self.low_detail_mode:
                self.Serpiente.update()
                self.Serpiente.draw()

            [x.draw() for x in self.texts_options_list]
            [x.draw() for x in self.botones_options_list]

            pag.draw.circle(self.ventana, 'white', self.button_toggle_fullscreen.rect.center, 27, 4)
                

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
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(60, [(0,self.framerate_dificultad*2), (0,self.framerate_dificultad)]), 'afectado': 'ball'})
                if eventos.type == KEYDOWN:
                    if eventos.key == K_ESCAPE or eventos.key == K_SPACE:
                        self.sounds.boton1.play()
                        self.pausado = False
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    for b in self.botones_pause_list:
                        if b.rect.collidepoint(eventos.pos):
                            b.click()
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
                self.BV_Volumen_Sonidos.pulsando_volumen()
                self.sounds.set_volumen(self.BV_Volumen_Sonidos.volumen)
                self.json["sound_volumen"] = self.BV_Volumen_Sonidos.volumen
            if self.BV_Volumen_Musica_press:
                self.BV_Volumen_Musica.pulsando_volumen()
                pag.mixer_music.set_volume(self.BV_Volumen_Musica.volumen)
                self.json["music_volumen"] = self.BV_Volumen_Musica.volumen
                if self.BV_Volumen_Musica.volumen == 0:
                    pag.mixer_music.pause()
                else:
                    pag.mixer_music.unpause()

            self.draw_effects_before()

            for alala in self.bloques:
                pag.draw.rect(self.ventana, alala['color'], alala['rect'], border_radius= alala['border_radius'])


            if self.alive:
                if self.playing:
                    self.ball.draw()
                    self.particles_ball.draw()

            self.draw_effects_after()

            for i,text in sorted(enumerate(self.float_texts_list),reverse= True):
                if text.update():
                    self.float_texts_list.pop(i)
                text.draw()

            [x.draw() for x in self.texts_pause_list]
            [x.draw() for x in self.botones_pause_list]

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
                if eventos.type == USEREVENT+1:
                    self.ball.lenta = False
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(60, [(0,self.framerate_dificultad/2), (0,self.framerate_dificultad)]), 'afectado': 'ball'})
                if eventos.type == USEREVENT+2:
                    self.ball.rapida = False
                    self.cubic_bezier_transitions.append({'transition': Curva_de_Bezier(60, [(0,self.framerate_dificultad*2), (0,self.framerate_dificultad)]), 'afectado': 'ball'})
                elif eventos.type == KEYDOWN:
                    if eventos.key == K_u and self.alive and not self.fan_lvl_bool:
                        self.lvl += 1
                        self.start(self.lvl)
                    if eventos.key == K_ESCAPE and not self.win and self.alive:
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
                    if eventos.key == K_LEFT or eventos.key == K_a:
                        self.player.left = True
                    if eventos.key == pag.K_RIGHT or eventos.key == K_d:
                        self.player.right = True
                elif eventos.type == pag.KEYUP:
                    if eventos.key == K_LEFT or eventos.key == K_a:
                        self.player.left = False
                    if eventos.key == pag.K_RIGHT or eventos.key == K_d:
                        self.player.right = False
                elif eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    if self.game_over.restart.rect.collidepoint(eventos.pos) and not self.alive:
                        if not self.fan_lvl_bool:self.start(self.lvl)
                        else: self.start_fan_lvl(self.lvl_fan)
                    if self.lvl_clear.boton_lvl_pass.rect.collidepoint(eventos.pos) and self.win:
                        if not self.fan_lvl_bool:
                            try:
                                self.json["lvl_scores"][f"lvl_{self.lvl}_score"]
                            except:
                                self.json["lvl_scores"][f"lvl_{self.lvl}_score"] = 0
                            self.json["lvl_scores"][f"lvl_{self.lvl}_score"] = max(self.score,self.json["lvl_scores"][f"lvl_{self.lvl}_score"])
                            self.lvl += 1
                            self.start(self.lvl)
                        else:
                            try:
                                self.json["fan_lvl_scores"][f"lvl_{self.lvl_fan}_score"]
                            except:
                                self.json["fan_lvl_scores"][f"lvl_{self.lvl_fan}_score"] = 0
                            self.json["fan_lvl_scores"][f"lvl_{self.lvl_fan}_score"] = max(self.score,self.json["fan_lvl_scores"][f"lvl_{self.lvl_fan}_score"])
                            self.title_screen = True
                            self.Pantalla_de_titulo()

                            
                            # Logica del juego
            self.loss()

            if len(self.bloques) == 6 and Hipotenuza(self.bloques[-1]['rect'].center, self.ball.rect.center) < 130:
                angulo1 = Angulo(self.ball.rect.center,self.bloques[-1]['rect'].center)
                angulo2 = Angulo((0,0),self.ball.vel)
                dist = Hipotenuza(self.bloques[-1]['rect'].center, self.ball.rect.center)
                # if (Hipotenuza(self.bloques[-1]['rect'].center, self.ball.rect.center) < 150 and angulo1 > angulo2-15 and angulo1 < angulo2+15) or(
                #     Hipotenuza(self.bloques[-1]['rect'].center, self.ball.rect.center) < 110 and angulo1 > angulo2-20 and angulo1 < angulo2+20) or (
                #     Hipotenuza(self.bloques[-1]['rect'].center, self.ball.rect.center) < 50 and angulo1 > angulo2-170 and angulo1 < angulo2+170):
                if angulo1 > (angulo2- (angulo2* abs((1.5-(dist/150))*.8)))*.7 and angulo1 < (angulo2+ (angulo2* abs(1.5-(dist/150))*.8))*.7 or dist < 50:
                    if not self.acercandose:
                        self.acercandose = True
                        self.sounds.casi.play()
                    self.deltatime_ball.FPS = max(15,(Hipotenuza(self.ball.rect.center,self.bloques[-1]['rect'].center)/90)*self.framerate_dificultad)
                else:
                    if self.acercandose:
                        self.acercandose = False
                        if len(self.bloques) > 5:
                            self.sounds.casi.stop()
                            self.sounds.decepcion.play()
                    self.acercandose = False
                    self.deltatime_ball.FPS = self.framerate_dificultad
            elif not self.ball.lenta and not self.ball.rapida:
                self.deltatime_ball.FPS = self.framerate_dificultad
                
            for i,tra in sorted(enumerate(self.cubic_bezier_transitions),reverse= True):
                vec = tra['transition'].update()
                if vec == True:
                    self.cubic_bezier_transitions.pop(i)
                else:
                    if tra['afectado'] == 'player':
                        tra['transition'].move([(self.player.rect2.centerx, 650), (self.player.rect2.centerx, 650 + 15), (self.player.rect2.centerx, 650)])
                        self.player.rect2.center = vec
                    elif tra['afectado'] == 'ball':
                        self.deltatime_ball.FPS = vec[1]
                    else:
                        self.bloques[tra['afectado']]['rect'].center = vec


            if not self.win and self.alive and self.playing:
                self.bugueado += 1
            if self.bugueado == 10 * self.deltatime_ball.FPS:
                self.ball.pos = (self.ventana_rect.centerx,self.ventana_rect.centery * 1.7)
                self.ball.vel = [0,-4]
                self.playing = False


                        # Dibujar
            self.draw_effects_before()

            if not self.low_detail_mode:
                self.particles_ball.update(self.ball.pos)
                self.particles_ball.draw()

            for alala in self.bloques[1:]:
                pag.draw.rect(self.ventana, alala['color'], alala['rect'], border_radius= alala['border_radius'])

            if not self.low_detail_mode:
                self.player.draw2()
            self.player.draw()

            if self.ball.rect.left > self.ventana_rect.w or self.ball.rect.top > self.ventana_rect.h or self.ball.rect.right < 0 or self.ball.rect.bottom < 0:
                self.bugueado = 0
                self.a_reiniciar.draw()
                self.a_reiniciar2.draw()

            if len(self.bloques) == 5:
                if not self.win:
                    self.win = True
                    self.sounds.lvl_clear.play()
                self.lvl_clear.draw_WIN()
            elif self.alive:
                if self.playing:
                    self.ball.update(self.deltatime_ball.dt)
                    self.ball.draw()
                    self.colicion()
                else:
                    self.text_press_space.draw()
                self.player.move(self.deltatime.dt)
            else:
                self.game_over.draw_Gameover()
        
            [x.draw() for x in self.texts_main_list]

            for i, spark in sorted(enumerate(self.sparks), reverse=True):
                spark.move(self.deltatime.dt)
                spark.draw(self.ventana)
                if not spark.alive:
                    self.sparks.pop(i)

            self.draw_effects_after()


            for i,p in sorted(enumerate(self.powers),reverse= True):
                p.move(self.deltatime.dt)
                p_c = p.colicion(self.bloques_rects[:5])
                if p_c == 'Destroy':
                    self.powers.pop(i)
                elif p_c == True:
                    self.appli_powerup(p.type)
                    self.powers.pop(i)
                p.draw()


            for i,text in sorted(enumerate(self.float_texts_list),reverse= True):
                if text.update():
                    self.float_texts_list.pop(i)
                text.draw()


            if self.lvl > 9:self.text_ganaste.draw()

            pag.display.flip()
            self.relog.tick(self.framerate_general)


if __name__=='__main__':
    BrickBricker()