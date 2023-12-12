import pygame as pag, os, random
from pygame._sdl2 import messagebox
from pathlib import Path

class Set_music:
    def __init__(self, aleatorio: bool = True) -> None:
        self.canciones = []
        self.mode = 1
        self.p_musica = ['.mp3', '.obb', '.wav', '.ogg']
        self.pausar_musica = False
        self.escoger = ''
        self.aleatorio = aleatorio
        pag.mixer_music.set_endevent(50000)

    def load_music(self, dir = None) -> str:
        # BASE_DIR = '/'.join(__file__.split('\\')[:-1])
        BASE_DIR = Path(__file__).resolve().parent
        self.canciones.clear()
        self.music_dir = dir
        if self.music_dir == '' or self.music_dir == None:
            return False

        try:
            os.chdir(self.music_dir)
            for filename in os.listdir():
                name, extension = os.path.splitext(self.music_dir + filename)
                if extension in self.p_musica:
                    self.canciones.append(filename)
            if len(self.canciones) < 1:
                return False
            return self.change()
        except NotADirectoryError:
            try:
                self.music_var = pag.mixer_music.load(dir)
                self.canciones.append(dir)
                return self.change()
            except:
                messagebox(
                    "Error",
                    "A ocurrido un error al cargar la carpeta/cancion\n\nPor favor, comprueba que si es una cancion individual\n y que esté en un formato adecuado",
                    info=False,
                    error=1,
                    buttons=("Ok",),
                    return_button=1,
                    escape_button=0,
                )
        finally:

            os.chdir(BASE_DIR)

        
    def change(self, song: str = None) -> str:
        if self.mode == 2:
            pag.mixer_music.play()
            if self.pausar_musica:
                pag.mixer_music.pause()
            self.escoger = self.canciones[0].split('\\')[-1]
        else:
            BASE_DIR = '/'.join(__file__.split('\\')[:-1])
            os.chdir(self.music_dir)
            if song != None: self.escoger = song
            elif self.aleatorio: self.escoger = random.choice(self.canciones)
            else:
                try:
                    self.escoger = self.canciones[self.canciones.index(self.escoger)+1] if self.escoger != '' or None else self.canciones[0]
                except:
                    self.escoger = self.canciones[0]
            self.music_var = pag.mixer_music.load(f'{self.escoger}')
            pag.mixer_music.play()
            if self.pausar_musica:
                pag.mixer_music.pause()
            os.chdir(BASE_DIR)
        return {'text':self.escoger, 'index': self.canciones.index(self.escoger)}

    def pause(self, boolean = None) -> bool:
        if boolean != None:
            self.pausar_musica = boolean
            if self.pausar_musica: pag.mixer_music.pause()
            else: pag.mixer_music.unpause()
            return self.pausar_musica
        if not self.pausar_musica: 
            pag.mixer_music.pause()
        else:
            pag.mixer_music.unpause()
        self.pausar_musica = not self.pausar_musica
        return self.pausar_musica

    def random(self, val = None):
        if val != None:
            self.aleatorio = val
        else:
            self.aleatorio = not self.aleatorio
        return self.aleatorio