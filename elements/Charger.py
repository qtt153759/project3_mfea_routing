import sys
from multipledispatch import dispatch
try:
    from problem.ProblemManager import ProblemManager
except ImportError:
    import sys
    ProblemManager = sys.modules['problem' + '.ProblemManager']
from problem.Configs import Configs

class Charger:
    
    E0: float
    """Charger's energy capacity"""
    
    speed: float
    """Charger's travel speed"""

    Pm: float
    """Charger's per-second traveling consumption rate"""

    U: float
    """Charger's charging rate"""

    def __init__(self, e0: float, speed: float, pm: float, u: float) -> None:
        self.E0 = e0
        self.speed = speed
        self.Pm = pm
        self.U = u

    def getMovingTime(self, path:'list[int]') -> float:
        """Calculate charger's moving time given a path (list of node to travel to)"""
        pathLength = 0.0
        pathLength += ProblemManager.distance[ProblemManager.serviceStation.getId()][path[0]]
        pathLength += ProblemManager.distance[path[len(path) - 1]][ProblemManager.serviceStation.id]
        for i in range(1,len(path)):
            pathLength += ProblemManager.distance[path[i-1]][path[i]]
        return pathLength/self.speed

    @dispatch(float)
    def getMaxChargingTime(self, travelingDistance: float) -> float: # type: ignore
        """Calculate maximum time that this charger can charge given total moving distance"""
        return (self.E0 - travelingDistance * self.Pm / self.speed) / self.U

    @dispatch(list)
    def getMaxChargingTime(self, path):  # type: ignore
        """Calculate maximum time that this charger can charge in a given moving path\n
            Can not exceed maximum time in config"""
        movingTime = self.getMovingTime(path)
        if movingTime > Configs.T:
            print(f"Traveling time exceed charging cycle! {movingTime}", file=sys.stderr)
            sys.exit(0)

        #( Availale energy - moving time * moving consumption ) / charge rate
        ct = (self.E0 - movingTime*self.Pm) / self.U
        return min(ct, Configs.T - movingTime)

    def getEmove(self, path):
        """Calculate total energy used for moving in a given moving path"""
        return self.getMovingTime(path) * self.Pm

    def getU(self):
        return self.U

