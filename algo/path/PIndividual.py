import sys
from problem.ProblemManager import ProblemManager
from problem.Configs import Configs
from algo.path.Allele import Allele
from elements.Charger import Charger
class PIndividual:
    counter: float
    """n/a"""
    counter = 0

    id: float
    """n/a"""

    path: 'list[int]'
    """n/a"""

    chargingTime: 'list[float]'
    """"""

    gene: 'list[float]'
    """n/a"""

    skillFactor: int

    scalarFitness: float

    fitness: float
    fitness = 0.0

    factorialRank: 'list[int]'

    def __init__(self) -> None:
        self.counter = self.counter + 1
        self.id = self.counter

        self.gene = []
        for i in range(ProblemManager.USSD):
            self.gene.append(Configs.rand.uniform(0,1))

        self.factorialRank = []
        for i in range(ProblemManager.getTaskNumber()):
            self.factorialRank.append(-1)
        
    def randomInit(self):
        for i in range(ProblemManager.USSD):
            self.gene[i] = Configs.rand.uniform(0,1)

    def decoding(self, taskIndex: int):
        self.path = []

        list: 'list[Allele]'
        list = []

        #TODO Subnet may be empty. 
        #not a real copy, just copy list's reference
        sectors = ProblemManager.subNet[taskIndex]

        for index, sector in enumerate(sectors):
            # if sector.getLifetime() > Configs.T:
            #     self.gene[index] = 0.5 + 0.5 * Configs.rand.uniform(0,1)
            if self.gene[index] <= 0.5:
                list.append(Allele(self.gene[index],sector.id))

        if len(list) == 0:
            list.append(Allele(self.gene[0],sectors[0].id))
        
        #bug prone!!
        list.sort()

        for a in list:
            self.path.append(a.sensorId)
        pass

    def calculateFitness(self) -> float:
        """How good the individual is"""
        self.decoding(self.skillFactor)

        w: list[float]
        w = self.getPriority()

        dead = 0
        totalLifetime = 0
        maxLifetime = 0
        totalAfterT=0
        n = len(self.path)
        arriveTime: 'list[float]'
        arriveTime = []
        for i in range(n):
            arriveTime.append(0.0)

        visited: 'list[bool]'
        visited = []
        for i in range(ProblemManager.maxSensorId+1):
            visited.append(False)


        self.chargingTime = []
        for i in range(n):
            self.chargingTime.append(0)

        ch: Charger
        ch = ProblemManager.chargers[self.skillFactor]

        maxCharingTime: float
        maxCharingTime = ch.getMaxChargingTime(self.path)

        #repairing
        arriveTime[0] = ProblemManager.distance[ProblemManager.serviceStation.id][self.path[0]] /ch.speed

        for i in range(n):
            s = ProblemManager.getSensorById(self.path[i])
            self.chargingTime[i] = w[i] * maxCharingTime
            visited[s.id] = True

            eRemain: float
            ub: float
            eRemain = s.E0 - arriveTime[i] * s.p
            # ub = (Configs.S_EMAX - eRemain) / (ch.U - s.p)
            if eRemain < Configs.S_EMIN:
                self.chargingTime[i] = 0
            # elif (self.chargingTime[i] > ub or True):
            #     self.chargingTime[i] = ub
            eAfterT: float
            eAfterT = s.E0 - Configs.T * s.p + self.chargingTime[i] * ch.U
            if ( (eRemain < s.Emin - 1e-3) or (eAfterT < s.Emin - 1e-3) ) :
                dead = dead + 1
			
            lifetime: float
            lifetime = (s.E0 + self.chargingTime[i] * ch.U - s.Emin) / s.p
            totalLifetime += lifetime
            maxLifetime = max(lifetime, maxLifetime)
            totalAfterT+=eAfterT

            if (i < n - 1):
                arriveTime[i + 1] = arriveTime[i] + self.chargingTime[i] \
                        + ProblemManager.distance[self.path[i]][self.path[i+1]] / ch.speed
            
        for s in ProblemManager.subNet[self.skillFactor]:
            if (not visited[s.id]):
                lifetime = s.getLifetime()
                if (lifetime < Configs.T):
                    dead = dead + 1

                totalLifetime += lifetime
                maxLifetime = max(lifetime, maxLifetime)
                eAfterT = s.E0 - Configs.T * s.p
                totalAfterT+=eAfterT



        netSize = len(ProblemManager.subNet[self.skillFactor])
        networkSurvivability = (netSize - dead) / (1.0 * netSize)
        energyRatioAfterT=totalAfterT/(netSize*Configs.S_EMAX)
        #unused
        #avgLifetime = totalLifetime / (1.0 * netSize)

        return networkSurvivability*0.8+0.2*energyRatioAfterT      

    def getPriority(self) -> 'list[float]':
        sum = 0.0
        priority: 'list[float]'
        priority = []
        for i in range (len(self.path)):
            s = ProblemManager.getSensorById(self.path[i])
            priority.append(s.getW())
            sum += priority[i]

        for i in range (len(self.path)):
            priority[i] /= sum

        return priority

    def mutation(self) -> None:
        u: float
        for i in range(len(self.gene)):
            u = Configs.rand.uniform(0,1)
            if u <= 0.5:
                deltaL = pow(2 * u, 1.0 / (Configs.NM + 1)) - 1
                p = self.gene[i] * (1.0 + deltaL)
                self.gene[i] = max(0,min(1,p))
            else:
                deltaR = 1.0 - pow(2 * (1 - u), 1.0 / (Configs.NM + 1))
                p = self.gene[i] + deltaR * (1 - self.gene[i])
                self.gene[i] = max(0,min(1,p))
    
            
    def getFitness(self, task: int) -> float:
        if task == self.skillFactor:
            return self.fitness
        else:
            return -sys.float_info.max

    def clone(self) -> 'PIndividual':
        indiv = PIndividual()
        indiv.gene = self.gene.copy()
        return indiv

    def duplicate(self) -> 'PIndividual':
        """Everything from the old object will be kept

        This is a workaround to bypass the reference problem"""
        indiv = PIndividual()
        indiv.counter = self.counter
        indiv.id = self.id
        indiv.path = self.path.copy()
        indiv.chargingTime = self.chargingTime.copy()
        indiv.gene = self.gene.copy()
        indiv.skillFactor = self.skillFactor
        indiv.scalarFitness = self.scalarFitness
        indiv.fitness = self.fitness
        indiv.factorialRank = self.factorialRank.copy()
        return indiv

    def __eq__(self, other: 'PIndividual'):
        if self.fitness == other.fitness:
            return True
        else:
            return False

    def __lt__(self, other: 'PIndividual'):
        if self.fitness > other.fitness:
            return True
        else:
            return False

    def __gt__(self, other: 'PIndividual'):
        if self.fitness < other.fitness:
            return True
        else:
            return False
    
    












