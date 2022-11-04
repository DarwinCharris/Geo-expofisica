import math


class Carga():
    def __init__(self, x:float, y:float, carga:float, distancia:float, magnitud:float, vecx:float, vecy:float) -> None:
        self.x = x
        self.y = y
        self.carga = carga
        self.distancia = distancia
        self.magnitud = magnitud
        self.vecx = vecx
        self.vecy = vecy
    def distancia_ap(self,x,y,px,py):
        return  math.sqrt(((px-x)**2)+((py-y)**2))
    def magnitudT(self, carga, distancia):
        return (9000000000*(carga*0.0000001))/(distancia**2)#colocar un x 10 a la respuesta 
    def vectorx(self,qx,px):
        return(px-0)-(qx-0)
    def vectory(self, qy, py):
        val= (py-0)-(qy-0)
        return val
class Punto():
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
    