import math

#TODO: Có vẻ như là một node trên đồ thị
#Tuy nhiên chưa rõ vai trò của Node trong thuật toán
class Node:

    #Node's identifier
    id: int

    #Node's x-position
    x: float

    #Node's y-position
    y: float

    def __init__(self, id: int, x: float, y:float) -> None:
        self.id = id
        self.x = x
        self.y = y

    def getDistance(self, node: 'Node') -> float:
        x_dif = self.x - node.x
        y_dif = self.y - node.y
        return math.sqrt(x_dif*x_dif + y_dif*y_dif)

    def getX(self) -> float:
        return self.x

    def setX(self,x: float) -> None:
        self.x = x

    def getY(self) -> float:
        return self.y

    def setY(self,y: float) -> None:
        self.y = y

    def getId(self) -> int:
        return self.id

    def setId(self, id: int) -> None:
        self.id = id
 
        