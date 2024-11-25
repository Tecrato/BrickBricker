import pygame as pag, time, random
from math import cos,sin,radians,pi
class Background:
	def __init__(self,surface,size, type = 1) -> None:
		self.surface = surface
		self.surface2 = pag.surface.Surface(size)
		self.size = size
		self.type = type
		if self.type == 1:self.scroll = -120
		elif self.type == 2:
			self.surface2 = pag.surface.Surface((size[0],size[1]+400))
			self.scroll = -150
			self.surface2.fill((0,0,0))
			for x in range(0,11):
				polygon = (
					(0,                 (self.size[1]/10+200)+ (200*x) + self.scroll),
					(self.size[0],      (self.size[0]/10) + (200*x) + self.scroll),
					(self.size[0],      (self.size[0]/10+50) + (200*x) + self.scroll),
					(0,                 (self.size[1]/10+250) + (200*x) + self.scroll),
				)
				pag.draw.polygon(self.surface2,(20,60,20), polygon)
				pag.draw.polygon(self.surface2,'black', polygon, 5)
				polygon = (
					(0,                 (self.size[1]/10) + (200*x) + self.scroll),
					(0,                 (self.size[1]/10+50) + (200*x) + self.scroll),
					(self.size[0],      (self.size[0]/10+250) + (200*x) + self.scroll),
					(self.size[0],      (self.size[0]/10+200) + (200*x) + self.scroll),
				)
				pag.draw.polygon(self.surface2,(20,60,20), polygon)
				pag.draw.polygon(self.surface2,'black', polygon, 5)
		elif self.type == 3:
			self.last_time = time.time()
			self.squares = []
			self.timer = 0
	def draw(self) -> None:
		if self.type == 1:
			self.surface2.fill((0,0,20))
			self.scroll -= .5
			if self.scroll <= -240: self.scroll = -120
			for x in range(11):
				polygon = (
					(0,                 (self.size[1]/10+100)+ (120*x) + self.scroll),
					(self.size[0],      (self.size[0]/10) + (120*x) + self.scroll),
					(self.size[0],      (self.size[0]/10+50) + (120*x) + self.scroll),
					(0,                 (self.size[1]/10+150) + (120*x) + self.scroll),
				)
				pag.draw.polygon(self.surface2,(20,60,20), polygon)
				pag.draw.polygon(self.surface2,'black', polygon, 5)
			self.surface.blit(self.surface2,(0,0))
		elif self.type == 2:
			self.scroll -= .5
			if self.scroll <= -400: self.scroll = -200
			
			self.surface.blit(self.surface2,(0,0+ self.scroll))
		elif self.type == 3:
			self.surface2.fill((0,0,0))
			if time.time() - self.last_time > self.timer:
				radio = random.randint(10,50)
				left = random.randint(0,self.size[0])
				angle = random.randint(0,360)
				giro = random.random()*0.7 +0.1
				self.squares.append({'top':-radio,'left':left,'angle':angle, 'radio':radio,'giro':giro})
				self.timer = random.random()*2.5 + 0.5
				self.last_time = time.time()
			for i,poly in sorted(enumerate(self.squares),reverse=True):
				poly['top']+=1
				poly['angle']+=poly['giro']
				if poly['top'] > self.size[1]+poly['radio']:
					self.squares.pop(i)
				polygon = [
					[poly['left'] + cos(radians(poly['angle'])) * poly['radio'],poly['top'] - sin(radians(poly['angle'])) * poly['radio']],
					[poly['left'] + cos(radians(poly['angle'])+pi/2) * poly['radio'],poly['top'] - sin(radians(poly['angle'])+pi/2) * poly['radio']],
					[poly['left'] + cos(radians(poly['angle'])+pi) * poly['radio'],poly['top'] - sin(radians(poly['angle'])+pi) * poly['radio']],
					[poly['left'] + cos(radians(poly['angle'])-pi/2) * poly['radio'],poly['top'] - sin(radians(poly['angle'])-pi/2) * poly['radio']],
				]
				pag.draw.polygon(self.surface2,'darkgrey', polygon,5)
			self.surface.blit(self.surface2,(0,0))
		