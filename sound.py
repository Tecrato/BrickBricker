from pygame import mixer


class Set_sounds:
    def __init__(self) -> None:
        mixer.init()
        self.boton1 = mixer.Sound('./Assets/sounds/button2.ogg')

        self.ball_pop = mixer.Sound('./Assets/sounds/ballclick2.ogg')
        self.ball_pop2 = mixer.Sound('./Assets/sounds/ballclick1.ogg')

        self.decepcion = mixer.Sound('./Assets/sounds/reaccion decepcion.mp3')

        self.ball_colicion= mixer.Sound('./Assets/sounds/choque.mp3')

        self.lvl_clear = mixer.Sound('./Assets/sounds/lvl clear.mp3')

        self.final_lvl = mixer.Sound('./Assets/sounds/Final lvl.mp3')

        self.loss = mixer.Sound('./Assets/sounds/loss.mp3')

        self.casi = mixer.Sound('./Assets/sounds/casi.mp3')

        self.extra_life = mixer.Sound('./Assets/sounds/extra life.mp3')

        self.slow = mixer.Sound('./Assets/sounds/slow.mp3')

        self.fast = mixer.Sound('./Assets/sounds/fast.mp3')

        self.money = mixer.Sound('./Assets/sounds/money.mp3')

        self.sounds_list = [self.boton1, self.ball_pop, self.ball_pop2,self.ball_colicion,self.lvl_clear,
        self.final_lvl,self.loss,self.casi,self.decepcion,self.extra_life,self.slow,self.fast, self.money]
        self.set_volumen(.5)

    def set_volumen(self, vol) -> None:
        for s in self.sounds_list:
            s.set_volume(vol)
        # for s in self.sounds_list[-3:]:
        #     s.set_volume(vol*.5)