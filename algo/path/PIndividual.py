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
    def calculateFitnessWithPath(self) -> float:
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

        totalTimeRatio = 0.0

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
            # elif (self.chargingTime[i] > ub):
            #     self.chargingTime[i] = ub
            eAfterT: float
            eAfterT = s.E0 - Configs.T * s.p + self.chargingTime[i] * ch.U
            if ( (eRemain < s.Emin - 1e-3) or (eAfterT < s.Emin - 1e-3) ) :
                dead = dead + 1
			
            lifetime: float
            lifetime = (s.E0 + self.chargingTime[i] * ch.U - s.Emin) / s.p

            ######
            ratio= (eAfterT/s.p) / Configs.T
            if ratio>1:
                ratio=1
            totalTimeRatio+=ratio 
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
        totalTimeRatio=totalTimeRatio/netSize
        #unused
        #avgLifetime = totalLifetime / (1.0 * netSize)
        # return networkSurvivability
        # print("check",networkSurvivability," va ",totalTimeRatio)


        return networkSurvivability*Configs.networkSurvivabilityFitness+totalTimeRatio*Configs.totalTimeRatioFitness

        
        # return networkSurvivability*0.8+0.2*energyRatioAfterT   

    def calculateFitness(self) -> float:
        """How good the individual is"""
        self.decoding(self.skillFactor) #from gene -> get path
        return self.calculateFitnessWithPath()

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
                # self.gene[i]= 0.5+deltaL*(0.5-self.gene[i])
                self.gene[i] = max(0,min(1,p))
                # print("u<0.5",self.gene[i],p)
            else:
                deltaR = 1.0 - pow(2 * (1 - u), 1.0 / (Configs.NM + 1))
                p = self.gene[i] + deltaR * (1 - self.gene[i])
                # self.gene[i]= 0.5+deltaR*(self.gene[i]-0.5)
                self.gene[i] = max(0,min(1,p))
                # print("u>0.5",self.gene[i],p)
    
            
    def getFitness(self, task: int) -> float:
        if task == self.skillFactor:
            return self.fitness
        else:
            return -sys.float_info.max

    def clone(self) -> 'PIndividual':
        indiv = PIndividual()
        indiv.gene = self.gene.copy()
        indiv.skillFactor=self.skillFactor
        indiv.path=self.path.copy()
        indiv.fitness=self.fitness
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

        # 2 opt
    def tsp_2_opt(self)->'PIndividual':
        if len(self.path)<15:
            return self
        sectors = ProblemManager.subNet[self.skillFactor]
        sectorsDict= {sectors[i].id: i for i in range(0, len(sectors))}
        
        improved = 0
        best_found_individual = self.clone()
        loopCounter = 0
        while improved<10:
            loopCounter += 1
            if loopCounter > 5000: #prevent dead loop
                break
            #print(f"2 opt improved {improved}, loop counter {loopCounter}")
            i =Configs.rand.randint(1,len(best_found_individual.path) - 2)
            j= Configs.rand.randint(i+1,len(best_found_individual.path) - 1)
            
            new_individual = self.swap_2opt(best_found_individual, i, j,sectorsDict)
            new_individual.fitness=new_individual.calculateFitnessWithPath()
            if new_individual.fitness < best_found_individual.fitness:
                best_found_individual = new_individual
                improved += 1
                loopCounter = 0
          
        return best_found_individual

    def swap_2opt(self,best_found_individual:'PIndividual',i:int,j:int,sectorsDict:'dict')->'PIndividual':
        
        new_individual=best_found_individual.clone()
        new_individual.path = best_found_individual.path[0:i]
        new_individual.path.extend(reversed(best_found_individual.path[i:j + 1]))
        new_individual.path.extend(best_found_individual.path[j + 1:])
   
        for t in range(i,j+1):
            a=sectorsDict[best_found_individual.path[t]]
            b=sectorsDict[new_individual.path[t]]
            new_individual.gene[b]=best_found_individual.gene[a]
        return new_individual

# 3 opt
    def tsp_3_opt(self)->'PIndividual':
        if len(self.path)<15:
            return self
        moves_cost:list[PIndividual]
        sectors = ProblemManager.subNet[self.skillFactor]
        sectorsDict= {sectors[i].id: i for i in range(0, len(sectors))}
        loopCounter = 0
        improved = 0
        best_found_individual = self.clone()
        best_found_individual.fitness=best_found_individual.fitness
        while improved<3:
            loopCounter += 1
            if loopCounter > 5000: #prevent dead loop
                break
            #print(f"3 opt improved {improved}, loop counter {loopCounter}")
            k= Configs.rand.randint(2,len(best_found_individual.path) - 2)
            i =Configs.rand.randint(1,k)
            j= Configs.rand.randint(k+1,len(best_found_individual.path) - 1)

        
            moves_cost = self.get_solution_cost_change(best_found_individual, i, j, k)
            # we need the minimum value of substraction of old route - new route
            best_return_3_opt = min(moves_cost, key=lambda item: item.fitness)
            # print(f'compare {best_return_3_opt.fitness} va {best_found_individual.fitness}')
            if best_return_3_opt.fitness < best_found_individual.fitness:
                for t in range(len(best_found_individual.path)):
                    a=sectorsDict[best_found_individual.path[t]]
                    b=sectorsDict[best_return_3_opt.path[t]]
                    best_return_3_opt.gene[b]=best_found_individual.gene[a]
                # print("after opt decreas",best_found_individual.fitness-best_return_3_opt.fitness)
                best_found_individual = best_return_3_opt
                improved += 1
                loopCounter = 0
        # just to start with the same node -> we will need to cycle the results.
        # print(f'{len(best_found_individual.path)}:{improved}:{loopCounter}')
        return best_found_individual

    def get_solution_cost_change(self,best_found_individual:'PIndividual', i:int, j:int, k:int)->'list[PIndividual]':
        number_Of_3_OPT_case=8
        new_individuals:list[PIndividual]
        new_individuals=[]
        for i in range(number_Of_3_OPT_case):
            new_individual=best_found_individual.clone()
            new_individuals.append(new_individual)

        new_individuals[0].path =  new_individuals[0].path[:i + 1] +  new_individuals[0].path[i+1:k + 1] + new_individuals[0].path[k+1: j + 1] + new_individuals[0].path[j+1: ]
        new_individuals[1].path =  new_individuals[1].path[:i + 1] +  new_individuals[1].path[i+1:k + 1] + new_individuals[1].path[j: k: -1] + new_individuals[1].path[j+1: ]
        new_individuals[2].path =  new_individuals[2].path[:i + 1] +  new_individuals[2].path[k:i: -1] +  new_individuals[2].path[k+1: j + 1] +  new_individuals[2].path[j+1: ]
        new_individuals[3].path =  new_individuals[3].path[:i + 1] +  new_individuals[3].path[k:i: -1] +  new_individuals[3].path[j: k: -1] +  new_individuals[3].path[j+1: ]
        new_individuals[4].path =  new_individuals[4].path[:i + 1] +  new_individuals[4].path[k+1: j + 1] +  new_individuals[4].path[i+1:k + 1] +  new_individuals[4].path[j+1: ]
        new_individuals[5].path =  new_individuals[5].path[:i + 1] +  new_individuals[5].path[k+1: j + 1] +  new_individuals[5].path[k:i: -1] +  new_individuals[5].path[j+1: ]
        new_individuals[6].path =  new_individuals[6].path[:i + 1] +  new_individuals[6].path[j: k: -1] +  new_individuals[6].path[i+1:k + 1] +  new_individuals[6].path[j+1: ]
        new_individuals[7].path =  new_individuals[7].path[:i + 1] +  new_individuals[7].path[j: k: -1] +  new_individuals[7].path[k:i: -1] +  new_individuals[7].path[j+1: ]
        
        for i in range(number_Of_3_OPT_case):
            new_individuals[i].fitness=new_individuals[i].calculateFitnessWithPath()
        return new_individuals
            
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
    
    












