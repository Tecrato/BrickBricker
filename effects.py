import pygame as pag
from numpy import random,sin,cos,radians


from Utilidades.particles import Particles


class Effect:
    """### Descripcion
    Con esta clase podras crear effectos pre-establecidos"""
    def __init__(self, type: int, coords: tuple, surface, size: tuple, limit:int = 150, color:tuple = (100,0,0)) -> None:
        self.fr = {
            'type':type,
            'coords':coords,
            'surface':surface,
            'size':size,
            'limit':limit,
            'color':color
        }
        self.type = type
        self.surface = surface
        self.surface_rect = self.surface.get_rect()
        self.color_grade = 1
        self.size_grade = 1
        self.coord = coords
        if type == 0:
            pass
        elif type == 1:
            self.size = size
            self.rect = pag.rect.Rect(coords[0],coords[1],size[0],size[1])
        elif type == 2:
            # Este es la explocion de los bloques
            self.circle_size = size
            self.down = False
        elif type == 3:
            # Esto es para la pantalla de win
            self.particles = []
            for i in range(1,16):
                self.particles.append(Particles(self.surface,3,False,size,3,0,
                    (self.coord),
                    (sin(radians(24*i))*3,cos(radians(24*i))*3),
                    'yellow', (random.randint(0,20),random.randint(0,20),random.randint(0,20))))
        elif self.type == 4:
            self.nose = .05
            self.color_grade = 0.001
            self.color = color
            self.surf = pag.surface.Surface((size[0],size[1]))
        elif self.type ==5:
            # La explosion del power up del fuego
            self.imagen = pag.transform.scale(pag.image.load('./Assets/images/explosion_3_40_128.webp'),(1200,1200))
            self.rect_image = pag.rect.Rect(0, 0, 150, 150)
            self.rect_image.center = coords
            self.lista_rects = []
            self.count = 0
            self.limit = limit
            for y in range(5):
                for x in range(8):
                    self.lista_rects.append(pag.rect.Rect(150 * x, 150 * y, 150, 150))


    def update(self, left = None, dt=1) -> bool:
        if self.type == 1:
            self.color_grade -= .03
            self.rect.top -= 1
            self.rect.left = left if left != None else self.rect.left
            if self.color_grade <= .05:
                return True
        if self.type == 2:
            if self.down:
                self.size_grade *= 0.9
                if self.size_grade <= 0.1:
                    return True
            elif self.color_grade <= 0.05:
                self.down = True
            else:
                self.size_grade *= 1.013
                self.color_grade *= 0.91
        elif self.type == 3:
            for particles in self.particles:
                if particles.update(dt=dt):
                    return True
        elif self.type == 4:
            self.color_grade += self.nose
            if self.color_grade >= 1:
                self.nose = -.05
            if self.color_grade <= 0:
                return True
            self.surf.fill((0,0,0))
            self.surf.fill((int(self.color[0]*self.color_grade),int(self.color[1]*self.color_grade),int(self.color[2]*self.color_grade)))
        elif self.type == 5:
            self.count += 1
            if self.count // round(self.limit / len(self.lista_rects)) >= len(self.lista_rects):
                return True
        return False

    def draw(self) -> None:
        if self.type == 1:
            pag.draw.rect(self.surface, (int(255*self.color_grade),int(255*self.color_grade),int(255*self.color_grade)), self.rect)
        elif self.type == 2:
            radius = round(self.circle_size * self.size_grade)*1.4
            self.surface.blit(self.lighting_func(radius),[self.coord[0]-radius,self.coord[1]-radius], special_flags= pag.BLEND_RGB_ADD)
            pag.draw.circle(self.surface, (int(255*self.color_grade),0,0), self.coord, round(self.circle_size * self.size_grade), 8)
            pag.draw.circle(self.surface, (int(255*self.color_grade),int(255*self.color_grade),0), self.coord, round(self.circle_size * self.size_grade/1.3), 5)
            pag.draw.circle(self.surface, (int(255*self.color_grade),int(255*self.color_grade),0), self.coord, round(self.circle_size * self.size_grade/1.6), 3)
            pag.draw.circle(self.surface, (int(255*self.color_grade),int(255*self.color_grade),0), self.coord, round(self.circle_size * self.size_grade/2.5), 5)
        elif self.type == 3:
            for particles in self.particles:
                particles.draw()
        elif self.type == 4:
            self.surface.blit(self.surf,(0,0), special_flags= pag.BLEND_RGB_ADD)
        elif self.type == 5:
            self.surface.blit(self.imagen, self.rect_image, self.lista_rects[self.count // round(self.limit / len(self.lista_rects))])

    def lighting_func(self,radius):
        surf = pag.surface.Surface((radius*2,radius*2))
        pag.draw.circle(surf, (40,40,40), (radius,radius), radius)
        surf.set_colorkey((0,0,0))
        return surf
    
    def reset(self) -> None:
        self.__init__(self.fr['type'],self.fr['coords'],self.fr['surface'],self.fr['size'],self.fr['limit'],self.fr['color'])