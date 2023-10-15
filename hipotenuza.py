import pygame as pag
def Hipotenuza(objeto1, objeto2) -> int:
    v1 = pag.math.Vector2(0, 0)
    v2 = pag.math.Vector2(objeto2[0]-objeto1[0], objeto2[1]-objeto1[1])
    
    hipotenuza = v1.distance_to(v2)
    return hipotenuza
def Angulo(objeto1, objeto2) -> int:
    v1 = pag.math.Vector2(0, 0)
    v2 = pag.math.Vector2(objeto2[0]-objeto1[0], objeto2[1]-objeto1[1])
    angulo = v1.angle_to(v2)
    return angulo if angulo > 0 else 180 + (180+angulo)