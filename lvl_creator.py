import pygame as pag, sys, sqlite3,os
from pygame._sdl2 import messagebox
from pygame.locals import *
from platformdirs import *

appdata = user_data_dir('save', 'BrickBreacker', roaming=True)
try:
    os.mkdir('/'.join(appdata.split('\\')[:-1]))
except:
    pass
try:
    os.mkdir(appdata)
except:
    pass

from Utilidades import *
from Barras_verticales import Vertical_bars

# que borre el ultimo cambio (es fliparse ya)
 
pag.init()

class lvl_creator_for_BrickBricker:
    def __init__(self) -> None:
        
        #Ventana
        self.ventana = pag.display.set_mode((800,700), SCALED|RESIZABLE|DOUBLEBUF|HWSURFACE)
        self.ventana_rect = self.ventana.get_rect()
        pag.display.set_caption('BrickBreacker')
        pag.display.set_icon(pag.image.load('lvl_c.ico'))

        self.distancia_borrando = 30
        self.upgrade_selected = 0
        self.all_inputs = []
        self.bloques = []
        self.bloques_colores = []
        self.bloques_rects = []
        self.bool_title_guardar = False
        self.brocha = False
        self.cambiando = False
        self.capturando_color = False
        self.click = True
        self.colocando_power = False
        self.mucho_border_radius = False
        self.color = (0,0,0)
        self.relog = pag.time.Clock()

        # Fuentes
        self.fuente_simbolos= 'Assets/Fuentes/Symbols.ttf'
        self.fuente_orbi_medium= 'Assets/Fuentes/Orbitron-Medium.ttf'
        self.fuente_mononoki = 'Assets/Fuentes/mononoki Bold Nerd Font Complete Mono.ttf'


        #Limites
        self.limite_inferior = pag.rect.Rect(0, self.ventana_rect.height-20, self.ventana_rect.width, 20)
        self.limite_superior = pag.rect.Rect(0, 0, self.ventana_rect.width, 20)
        self.limite_derecho = pag.rect.Rect(self.ventana_rect.width-20, 0, 20, self.ventana_rect.height)
        self.limite_izquierdo = pag.rect.Rect(0, 0, 20, self.ventana_rect.height)

        #Botones 
        self.text_boton1 = Create_text('1', 30, self.fuente_orbi_medium, (50,45), self.ventana,'center', 'black', True, color_rect='white', border_radius=10000)
        self.text_boton2 = Create_text('2', 30, self.fuente_orbi_medium, (100,45), self.ventana, 'center', 'black', True, color_rect='white', border_radius=10000)
        self.text_boton3 = Create_text('3', 30, self.fuente_orbi_medium, (150,45), self.ventana, 'center', 'black', True, color_rect='white', border_radius=10000)
        self.text_boton4 = Create_text('4', 30, self.fuente_orbi_medium, (200,45), self.ventana, 'center', 'black', True, color_rect='white', border_radius=10000)
        self.text_boton5 = Create_text('5', 30, self.fuente_orbi_medium, (250,45), self.ventana, 'center', 'black', True, color_rect='white', border_radius=10000)
        self.text_boton_b = Create_text('B', 30, self.fuente_orbi_medium, (50,100), self.ventana, 'center', 'black', True, color_rect='white', border_radius=10000)
        self.text_boton_borrar = Create_text('', 30, self.fuente_simbolos, (50,160), self.ventana, 'center', 'black', True, 'white', border_radius=40)
        self.text_boton_borrar_dis = Create_text(self.distancia_borrando, 20, self.fuente_orbi_medium, (50,200), self.ventana, 'center', 'white')
        self.text_boton_color_capture = Create_text('Capturar color', 30, self.fuente_orbi_medium, (300,45), self.ventana, 'left', 'black', True, 'white', border_radius=40)
        self.text_boton_guardar = Create_text('', 30, self.fuente_simbolos, (730,45), self.ventana, 'left', 'black', True, 'white', border_radius=40)

        self.boton_back_U = Create_text('', 20, self.fuente_simbolos, (30,260), self.ventana, 'center', 'white', padding=5)
        self.boton_next_U = Create_text('', 20, self.fuente_simbolos, (60,260), self.ventana, 'center', 'white', padding=5)
        self.bp_x = Create_text('X', 30, self.fuente_orbi_medium, (45,300), self.ventana, 'center', 'red')
        self.bp_1 = Create_text('', 30, self.fuente_simbolos, (-45,300), self.ventana, 'center', 'red')
        self.bp_2 = Create_text('', 30, self.fuente_simbolos, (-45,300), self.ventana, 'center', 'lightblue')
        self.bp_3 = Create_text('', 30, self.fuente_simbolos, (-45,300), self.ventana, 'center', 'orange')
        self.bp_4 = Create_text('良', 30, self.fuente_simbolos, (-45,300), self.ventana, 'center', 'white')
        self.bp_5 = Create_text('', 30, self.fuente_simbolos, (-45,300), self.ventana, 'center', 'white')
        self.bp_6 = Create_text('', 30, self.fuente_simbolos, (-45,300), self.ventana, 'center', 'white')
        self.bp_0 = Create_text('A', 30, self.fuente_mononoki, (-45,300), self.ventana, 'center', 'red')
        self.bp_s = Create_text('select', 18, self.fuente_orbi_medium, (45,340), self.ventana, 'center', 'black', True, color_rect='white',padding=10, border_radius=10)

        #Input text
        self.text_title_guardar = Create_text('Paso final', 25, 'Assets/Fuentes/Orbitron-ExtraBold.ttf', (self.ventana_rect.centerx,self.ventana_rect.centery-70), self.ventana, 'center', 'black')
        self.input_nombre = Input_text(self.ventana, (self.ventana_rect.centerx-95,self.ventana_rect.centery+10), (25,200), None, 'Nombre del nivel')
        self.all_inputs.append(self.input_nombre)

        self.rect_title_guardar = pag.rect.Rect(0,0,300,250)
        self.rect_title_guardar.center = self.ventana_rect.center

        self.text_X = Create_text('X', 30, 'Assets/Fuentes/Orbitron-ExtraBold.ttf', (730,45), self.ventana, 'left', 'black', True, 'white', border_radius=10000)

        #Barras Verticales
        self.barra1 = Vertical_bars((750,250), self.ventana, 150)
        self.barra1_status = False

        self.barra2 = Vertical_bars((750,450), self.ventana, 150)
        self.barra2_status = False

        self.barra3 = Vertical_bars((750,650), self.ventana, 150)
        self.barra3_status = False

        self.text_list = [self.text_boton1,self.text_boton2,self.text_boton3,self.text_boton4,self.text_boton5,self.text_boton_b,
        self.text_boton_borrar,self.text_boton_borrar_dis,self.text_boton_color_capture,self.text_boton_guardar,self.barra1,self.barra2,
        self.barra3, self.boton_next_U, self.boton_back_U, self.bp_1, self.bp_2, self.bp_3, self.bp_4, self.bp_5, self.bp_6,self.bp_s,
        self.bp_x, self.bp_0]
        
        self.powers = [self.bp_x,self.bp_1, self.bp_2, self.bp_3, self.bp_4, self.bp_5, self.bp_6,self.bp_0]
        for x in self.powers:
            # x.smothmove(1/60,1.3,2,1)
            # x.smothmove(1/60,1.3,.8,.5)
            x.smothmove(1/60,.9,1,1.8)

        # Los colores predeterminados
        for y in range(7): # 5
            for x in range(13): # 10
                self.bloques_colores.append({'rect': pag.rect.Rect(21 * x + 80,21 * y + 500, 20, 20), 'color': (125,125,125)})

        # self.the_colors=[
        #     (0,0,139),(0,255,0),(255,0,0),(135,206,255),(128,50,0),(255,255,0),(255,0,255),(255,128,0),(50,205,20),(0,0,0),
        #     (0,0,255),(70,0,180),(255,127,80),(175,48,96),(240,230,140),(75,0,130),(124,252,0),(173,216,230),(154,205,50),(50,50,50),
        #     (0,139,139),(128,128,0),(205,133,63),(255,165,0),(139,37,0),(218,112,214),(152,251,152),(238,232,170),(219,112,147),(100,100,100),
        #     (102,205,170),(255,192,203),(221,160,221),(250,128,114),(139,69,19),(46,139,87),(255,245,238),(160,82,45),(192,192,192),(127,127,127),
        #     (65,224,208),(70,130,180),(106,90,205),(210,180,140),(216,191,216),(255,99,71),(238,130,238),(208,32,144),(254,222,179),(211,211,211),
        #     (0,255,255),(255,218,185),(255,255,255)]

        self.the_colors = [(0,0,139),(0,255,0),(255,0,0),(135,206,255),(128,50,0),(255,255,0),(255,0,255),(255,128,0),(50,205,20),(0,0,0),
        (0,0,255),(70,0,180),(255,127,80),(175,48,96),(240,230,140),(75,0,130),(124,252,0),(173,216,230),(154,205,50),(50,50,50),(0,139,139),
        (128,128,0),(205,133,63),(255,165,0),(139,37,0),(218,112,214),(238,232,170),(219,112,147),(100,100,100),(102,205,170),(255,192,203),
        (221,160,221),(250,128,114),(139,69,19),(46,139,87),(255,245,238),(160,82,45),(192,192,192),(127,127,127),(65,224,208),(70,130,180),
        (106,90,205),(210,180,140),(216,191,216),(255,99,71),(238,130,238),(208,32,144),(254,222,179),(211,211,211),(0,255,255),(255,218,185),
        (255,255,255),(165,42,42),(255,160,122),(128,0,128),(0,128,0),(218,165,32),(128,128,128),(210,105,30),(255,215,0),(184,134,11),
        (34,139,34),(0,191,255),(30,144,255),(106,90,205),(147,112,219),(186,85,211),(148,0,211),(153,50,204),(139,69,19),(107,142,35),
        (255,250,205),(240,128,128),(255,69,0),(233,150,122),(139,115,85),(0,255,127),(255,105,180),(221,160,221),(238,232,170),(175,238,238),
        (240,230,140),(0,191,255),(95,158,160),(50,205,50),(0,128,128),(139,69,19),(210,105,30),(165,42,42),(255,222,173),(210,180,140)]
        self.the_colors = sorted(self.the_colors, key=lambda c: 0.2126*c[0] + 0.2152*c[1] + 0.0722*c[2])


        for i,c in enumerate(self.the_colors):
            self.bloques_colores[i]['color'] = c
            
        #Nose algo
        self.text_num = [Create_text(f'{n}', 20, self.fuente_orbi_medium, (-100,-100),self.ventana,'center') for n in range(10)]

        #Crear base de datos
        self.Base_de_datos = sqlite3.connect(appdata+'/'+'lvls.sqlite3')
        self.cursor = self.Base_de_datos.cursor()
        try:
            self.cursor.execute('CREATE TABLE FAN_LVLS(ID INTEGER PRIMARY KEY AUTOINCREMENT,NOMBRE VARCHAR(20) UNIQUE)')
        except:
            pass

        self.start(4)
        self.Main_Process()

        
    def update_bloques_rects(self) -> None:
        self.bloques_rects.clear()
        for d in self.bloques:
            self.bloques_rects.append(d['rect'])

    def start(self, mode) -> None:
        self.bloques.clear()

        if mode == 1:
            lvl_map = [
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
            ]

            self.mucho_border_radius = False
            for y in range(len(lvl_map)):
                for x in range(len(lvl_map[y])):
                    if lvl_map[y][x] == 1:
                        self.bloques.append({'rect': pag.rect.Rect(52 * x + 80,22 * y + 100, 50, 20), 'effect': 2, 'color': (125,125,125), 'active': True, 'cambio': True, 'border_radius': 0, 'change': True, 'power':None})

        if mode == 2:
            # lvl_map = []
            # for y in  range(16):
            #     lvl_map.append([1 for x in range(29)])

            lvl_map = [
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
                [1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 , 1 ],
            ]

            self.mucho_border_radius = False
            for y in range(len(lvl_map)):
                for x in range(len(lvl_map[y])):
                    if lvl_map[y][x] == 1:
                        self.bloques.append({'rect': pag.rect.Rect(22 * x + 80,22 * y + 80, 20, 20), 'effect': 2, 'color': (125,125,125), 'active': True, 'cambio': True, 'border_radius': 0, 'change': True, 'power':None})

        elif mode == 3:
            self.mucho_border_radius = True
            for y in range(16):
                for x in range(29):
                    self.bloques.append({'rect': pag.rect.Rect(22 * x + 80,22 * y + 80, 20, 20), 'effect': 2, 'color': (125,125,125), 'active': True, 'cambio': True, 'border_radius': 10000, 'change': True, 'power':None})
            
        elif mode == 4:
            self.mucho_border_radius = False
            for y in range(18):
                for x in range(32):
                    self.bloques.append({'rect': pag.rect.Rect(20 * x + 80,20 * y + 80, 20, 20), 'effect': 2, 'color': (125,125,125), 'active': True, 'cambio': True, 'border_radius': 0, 'change': True, 'power':None})
            
        elif mode == 5:
            self.mucho_border_radius = True
            for y in range(18):
                for x in range(32):
                    self.bloques.append({'rect': pag.rect.Rect(20 * x + 80,20 * y + 80, 20, 20), 'effect': 2, 'color': (125,125,125), 'active': True, 'cambio': True, 'border_radius': 10000, 'change': True, 'power':None})
            
        self.text_boton_b.change_color('green' if self.mucho_border_radius == True else 'black')

                    
        self.update_bloques_rects()

    def Guardar(self) -> None:
        nombre = self.input_nombre.get_text()
        nombre = nombre.replace(' ', '_')
        try:
            if nombre != '' and len(nombre) > 2 and len(nombre) <= 20:
                try:
                    self.cursor.execute("INSERT INTO FAN_LVLS VALUES(NULL,?)",[nombre])
                    self.cursor.execute("CREATE TABLE {} (rect VARCHAR(30), effect INTEGER, color VARCHAR(20), border_radius INTEGER(3), power INTEGER(3))".format(nombre))
                except Exception as err:
                    messagebox(
                        "Error",
                        f"El perfil No pudo ser guardado\n{err}",
                        info=False,
                        error=1,
                        buttons=("Ok",),
                        return_button=1,
                        escape_button=0,
                    )
                for a in self.bloques:
                    if a['active']:
                        datos = [f"{a['rect'].left,a['rect'].top,a['rect'].width,a['rect'].height}",a['effect'],f"{a['color']}", a['border_radius'],a['power']]
                        self.cursor.execute("INSERT INTO {} VALUES(?,?,?,?,?)".format(nombre),datos)
                
                self.Base_de_datos.commit()
            else:
                raise Exception('Nombre no valido')
        except Exception as err:
            messagebox(
                "Error",
                f"El perfil No pudo ser guardado\n{err}",
                info=False,
                error=1,
                buttons=("Ok",),
                return_button=1,
                escape_button=0,
            )

    def title_guardar(self):
        self.input_nombre.typing = True
        while self.bool_title_guardar:
            self.ventana.fill('black')
            mx,my = pag.mouse.get_pos()
            for eventos in pag.event.get():
                if eventos.type == pag.QUIT:
                    pag.quit()
                    sys.exit()
                if eventos.type == pag.KEYDOWN:
                    if eventos.key == K_ESCAPE:
                        self.bool_title_guardar = False
                    elif eventos.key == K_F11:
                        pag.display.toggle_fullscreen()
                    elif eventos.key == K_RETURN:
                        self.Guardar()
                        self.bool_title_guardar = False
                        break
                #Para el input
                for x in self.all_inputs:
                    if x.typing:
                        if eventos.type == TEXTINPUT:
                            x.add_letter(eventos.text)
                        elif eventos.type == KEYDOWN and eventos.key == K_LEFT:
                            x.left()
                        elif eventos.type == KEYDOWN and eventos.key == K_RIGHT:
                            x.right()
                        elif eventos.type == KEYDOWN and eventos.key == K_BACKSPACE:
                            x.del_letter()
                        elif eventos.type == KEYUP and eventos.key == K_BACKSPACE:
                            x.backspace = False
                        elif eventos.type == KEYUP and eventos.key == K_LEFT:
                            x.left_b = False
                        elif eventos.type == KEYUP and eventos.key == K_RIGHT:
                            x.right_b = False
                #Fin del input

                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    if self.text_X.rect.collidepoint(eventos.pos):
                        self.bool_title_guardar = False
                        break

                    # Para los inputs
                    for x in self.all_inputs:
                        x.typing = False
                    for x in self.all_inputs:
                        if x.text_rect.collidepoint(eventos.pos):
                            x.click()
                    #Fin del input

            pag.draw.rect(self.ventana, 'lightgrey', self.rect_title_guardar, border_radius=20)
            self.text_title_guardar.draw()
            self.input_nombre.draw()
            self.text_X.draw()
            pag.display.flip()
            self.relog.tick(60)


    def Main_Process(self):
        while True:
            self.ventana.fill('black')
            mx,my = pag.mouse.get_pos()
            for eventos in pag.event.get():
                if eventos.type == pag.QUIT:
                    pag.quit()
                    sys.exit()
                if eventos.type == pag.KEYDOWN:
                    if eventos.key == K_ESCAPE:
                        pag.quit()
                        sys.exit()
                    elif eventos.key == K_F11:
                        pag.display.toggle_fullscreen()
                    elif eventos.key == K_s:
                        self.bool_title_guardar = True
                        self.title_guardar()
                    elif eventos.key == K_SPACE:
                        self.capturando_color = True
                        self.text_boton_color_capture.change_color('green')
                if eventos.type == MOUSEWHEEL and self.brocha:
                    self.distancia_borrando += eventos.y
                    self.text_boton_borrar_dis.change_text(f'{self.distancia_borrando}')
                if eventos.type == MOUSEBUTTONDOWN and eventos.button == 3:
                        self.text_boton_color_capture.change_color('green')
                        self.capturando_color = True
                elif eventos.type == MOUSEBUTTONUP and eventos.button == 3:
                        self.text_boton_color_capture.change_color('black')
                        self.capturando_color = False
                elif eventos.type == MOUSEBUTTONDOWN and eventos.button == 1:
                    self.click = True
                    for x in self.bloques_colores:
                        if x['rect'].collidepoint(eventos.pos):
                            self.color = x['color']
                            self.barra1.set_volumen(x['color'][0] / 255)
                            self.barra2.set_volumen(x['color'][1] / 255)
                            self.barra3.set_volumen(x['color'][2] / 255)
                    if self.capturando_color:
                        self.capturando_color = False
                    if self.barra1.rect2.collidepoint(eventos.pos):
                        self.barra1_status = True
                    elif self.barra2.rect2.collidepoint(eventos.pos):
                        self.barra2_status = True
                    elif self.barra3.rect2.collidepoint(eventos.pos):
                        self.barra3_status = True
                    elif self.text_boton1.rect.collidepoint(eventos.pos):
                        self.start(1)
                    elif self.text_boton2.rect.collidepoint(eventos.pos):
                        self.start(2)
                    elif self.text_boton3.rect.collidepoint(eventos.pos):
                        self.start(3)
                    elif self.text_boton4.rect.collidepoint(eventos.pos):
                        self.start(4)
                    elif self.text_boton5.rect.collidepoint(eventos.pos):
                        self.start(5)
                    elif self.boton_next_U.rect.collidepoint(eventos.pos):
                        self.upgrade_selected += 1
                        if self.upgrade_selected > 7:
                            self.upgrade_selected = 0
                        for x in self.powers:
                            x.move((-45,300))
                        self.powers[self.upgrade_selected].move((45,300))
                    elif self.boton_back_U.rect.collidepoint(eventos.pos):
                        self.upgrade_selected -= 1
                        if self.upgrade_selected < 0:
                            self.upgrade_selected = 7
                        for x in self.powers:
                            x.move((-45,300))
                        self.powers[self.upgrade_selected].move((45,300))
                    elif self.bp_s.rect.collidepoint(eventos.pos):
                        self.colocando_power = not self.colocando_power
                        if self.colocando_power:
                            self.bp_s.change_color('green')
                        else:
                            self.bp_s.change_color('black')
                    elif self.text_boton_guardar.rect.collidepoint(eventos.pos):
                        self.bool_title_guardar = True
                        self.title_guardar()
                    elif self.text_boton_b.rect.collidepoint(eventos.pos):
                        self.mucho_border_radius = not self.mucho_border_radius
                        self.text_boton_b.change_color('green' if self.mucho_border_radius == True else 'black')
                    elif self.text_boton_color_capture.rect.collidepoint(eventos.pos) and not self.brocha:
                        self.text_boton_color_capture.change_color('green')
                        self.capturando_color = True
                    elif self.text_boton_borrar.rect.collidepoint(eventos.pos):
                        
                        self.brocha = not self.brocha
                        if self.brocha: self.text_boton_borrar.change_color('green')
                        else: self.text_boton_borrar.change_color('black')
                    else:
                        self.text_boton_color_capture.change_color('black')
                        self.cambiando = True
                elif eventos.type == MOUSEBUTTONUP and eventos.button == 1:
                    self.click = False
                    self.cambiando = False
                    self.barra1_status = False
                    self.barra2_status = False
                    self.barra3_status = False
                    for blabla in self.bloques:
                        blabla['cambio'] = True
                    

            # Se dibujan los bloques
            for alala in self.bloques:
                pag.draw.rect(self.ventana, alala['color'], alala['rect'], border_radius=alala['border_radius'])
                if alala['power'] != None:
                    if alala['color'] == 'black' or ((alala['color'][0] + alala['color'][1] + alala['color'][2]) / (255*3) < .4):
                        color = 'white'
                    else:
                        color = 'black'
                    if self.text_num[alala['power']].color != color:
                        self.text_num[alala['power']].change_color(color)
                    self.text_num[alala['power']].move(alala['rect'].center)
                    self.text_num[alala['power']].draw()

            # Se dibujan los bloques de los colores
            pag.draw.rect(self.ventana, 'white', [78,498,21*13 +3,21*7 +3],2)
            for alala in self.bloques_colores:
                pag.draw.rect(self.ventana, alala['color'], alala['rect'])

            # Se dibujan los textos
            for cosa in self.text_list:
                cosa.draw()

            # logica del ...
            if self.capturando_color:
                for blabla in self.bloques:
                    if blabla['rect'].collidepoint(pag.mouse.get_pos()):
                        self.color = (blabla['color'][0],blabla['color'][1],blabla['color'][2])
                        self.barra1.set_volumen(blabla['color'][0] / 255)
                        self.barra2.set_volumen(blabla['color'][1] / 255)
                        self.barra3.set_volumen(blabla['color'][2] / 255)
            if self.barra1_status:
                self.barra1.pulsando_volumen()
                self.color = (255*self.barra1.volumen,255*self.barra2.volumen,255*self.barra3.volumen)
            elif self.barra2_status:
                self.barra2.pulsando_volumen()
                self.color = (255*self.barra1.volumen,255*self.barra2.volumen,255*self.barra3.volumen)
            elif self.barra3_status:
                self.barra3.pulsando_volumen()
                self.color = (255*self.barra1.volumen,255*self.barra2.volumen,255*self.barra3.volumen)

            elif self.colocando_power and self.click:
                for blabla in self.bloques:
                    if blabla['rect'].collidepoint(pag.mouse.get_pos()):
                        if self.upgrade_selected != 0:
                            blabla['power'] = self.upgrade_selected
                        else:
                            blabla['power'] = None

            elif self.cambiando:
                if self.brocha:
                    for x in self.bloques:
                        if Hipotenuza(pag.mouse.get_pos(),x['rect'].center) < self.distancia_borrando:
                            x['color'] = self.color
                            if x['color'] == 'black' or ((x['color'][0] + x['color'][1] + x['color'][2]) / (255*3) < .05):
                                x['active'] = False
                            else:
                                x['active'] = True
                            if self.mucho_border_radius:
                                blabla['border_radius'] = 10000
                            else:
                                blabla['border_radius'] = 0
                else:
                    for blabla in self.bloques:
                        if blabla['rect'].collidepoint(pag.mouse.get_pos()) and blabla['cambio'] and blabla['change']:
                            blabla['color'] = self.color
                            if blabla['color'] == 'black' or ((blabla['color'][0] + blabla['color'][1] + blabla['color'][2]) / (255*3) < .05):
                                blabla['active'] = False
                            else:
                                blabla['active'] = True
                            if self.mucho_border_radius:
                                blabla['border_radius'] = 10000
                            else:
                                blabla['border_radius'] = 0
                            blabla['cambio'] = False

            if self.brocha:
                pag.draw.circle(self.ventana, 'white', pag.mouse.get_pos(), self.distancia_borrando, 3)
            pag.draw.rect(self.ventana, self.color, [600,500,100,100])

            pag.display.flip()
            self.relog.tick(90)

if __name__=='__main__':
    lvl_creator_for_BrickBricker()