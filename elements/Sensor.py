from elements.Node import Node

class Sensor(Node):

    Emax: float
    Emin: float
    E0  : float
    p   : float

    def __init__(self, id: int, x: float, y: float, e0: float, pi: float, emax: float, emin: float):
        super(Sensor, self).__init__(id, x, y)
        self.E0 = e0
        self.p = pi
        self.Emax = emax
        self.Emin = emin

    def getW(self) -> float:
        return self.p / self.E0

    def getLifetime(self) -> float:
        return (self.E0 - self.Emin) / self.p

    def getEmin(self):
        return self.Emin

    def getEmax(self):
        return self.Emax

    def getP(self):
        return self.p
    
    def getE0(self):
        return self.E0