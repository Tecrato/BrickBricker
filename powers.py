import pygame as pag
class PowerUp:
    def __init__(self, surface, pos, type, size):
        self.surface = surface
        self.pos = pag.math.Vector2(pos)
        self.type = type
        self.size = size
        self.outline = False
        self.count = 0
        self.font= pag.font.Font('Assets/Fuentes/Symbols.ttf',size)

        if self.type == 1:
            self.color = 'red'
            self.txt = self.font.render('',1,self.color)
            self.mask = pag.mask.from_surface(self.txt)
        elif self.type == 2:
            self.color = 'lightblue'
            self.txt = self.font.render('',1,self.color)
            self.mask = pag.mask.from_surface(self.txt)
        elif self.type == 3:
            self.color = 'orange'
            self.txt = self.font.render('',1,self.color)
            self.mask = pag.mask.from_surface(self.txt, threshold=90)
        elif self.type == 4:
            self.color = 'white'
            self.txt = self.font.render('良',1,self.color)
            self.mask = pag.mask.from_surface(self.txt)
        elif self.type == 5:
            self.color = 'white'
            self.txt = self.font.render('',1,self.color)
            self.mask = pag.mask.from_surface(self.txt)
        elif self.type == 6:
            self.color = 'white'
            self.txt = self.font.render('',1,self.color)
            self.mask = pag.mask.from_surface(self.txt, threshold=50)


        self.rect = self.txt.get_rect()
        self.rect.center = self.pos
    def draw(self) -> None:
        self.surface.blit(self.txt, self.rect)

        self.count += 1
        if self.count >= 40:
            self.outline = not self.outline
            self.count = 0
        if self.outline:
            points = [(x+self.rect.left,y+self.rect.top) for x,y in self.mask.outline()]
            pag.draw.lines(self.surface, 'white', 1, points,3)

    def move(self,dt=1):
        self.pos.y +=  1.5
        self.rect.center = self.pos

    def colicion(self,rects):
        if choque := self.rect.collidelist(rects) == 0:
            return True
        elif choque == 4:
            return 'Destroy'
        else:
            return False