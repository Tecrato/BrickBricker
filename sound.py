import pygame as pag


class Set_sounds:
    def __init__(self) -> None:
        pag.mixer.init()
        self.boton1 = pag.mixer.Sound('./Assets/sounds/button2.ogg')

        self.ball_pop = pag.mixer.Sound('./Assets/sounds/ballclick2.ogg')
        self.ball_pop2 = pag.mixer.Sound('./Assets/sounds/ballclick1.ogg')

        self.ball_colicion= pag.mixer.Sound('./Assets/sounds/choque.mp3')

        self.lvl_clear = pag.mixer.Sound('./Assets/sounds/lvl clear.mp3')

        self.final_lvl = pag.mixer.Sound('./Assets/sounds/Final lvl.mp3')

        self.loss = pag.mixer.Sound('./Assets/sounds/loss.mp3')

        self.casi = pag.mixer.Sound('./Assets/sounds/casi.mp3')

        self.decepcion = pag.mixer.Sound('./Assets/sounds/reaccion decepcion.mp3')

        self.extra_life = pag.mixer.Sound('./Assets/sounds/extra life.mp3')

        self.slow = pag.mixer.Sound('./Assets/sounds/slow.mp3')

        self.fast = pag.mixer.Sound('./Assets/sounds/fast.mp3')

        self.money = pag.mixer.Sound('./Assets/sounds/money.mp3')

        self.sounds_list = [self.boton1, self.ball_pop, self.ball_pop2,self.ball_colicion,self.lvl_clear,
        self.final_lvl,self.loss,self.casi,self.decepcion,self.extra_life,self.slow,self.fast, self.money]
        self.set_volumen(.5)

    def set_volumen(self, vol) -> None:
        for s in self.sounds_list:
            s.set_volume(vol)
        for s in self.sounds_list[-3:]:
            s.set_volume(vol*.5)