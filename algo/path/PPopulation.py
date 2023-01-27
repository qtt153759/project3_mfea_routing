from problem.Configs import Configs
from problem.ProblemManager import ProblemManager
from algo.path.PIndividual import PIndividual
from multipledispatch import dispatch
class PPopulation:

    #private ArrayList<PIndividual> indivs
    indivs: 'list[PIndividual]'
    indivs = []

    #private PIndividual[] best
    best: 'list[PIndividual]'
    best = []




    def randomInit(self) -> None:
        self.indivs.clear()
        for i in range(Configs.P_POP_SIZE):
            #mỗi individual ~ 1 charger, có P_POP_SIZE charger trong quần thể (PPopulation)
            indiv = PIndividual()

            #chia đều các charger cho các subnet
            skill = i % ProblemManager.getTaskNumber()
            indiv.skillFactor = skill


            indiv.randomInit()
            indiv.fitness = indiv.calculateFitness()

            self.indivs.append(indiv)
        
    
    def selfUX(self,par1: PIndividual, par2: PIndividual) -> None:
        n = ProblemManager.USSD
        for i in range(n):
            if Configs.rand.uniform(0,1):
                tmp = par1.gene[i]
                par1.gene[i] = par2.gene[i]
                par2.gene[i] = tmp
    
    def crossover(self,par1: PIndividual, par2: PIndividual) -> 'list[PIndividual]':
        u = Configs.rand.uniform(0,1)
        beta = 0
        if u <= 0.5:
            beta = pow(2 * u, 1.0 / (Configs.NC + 1))
        else:
            beta = pow(1.0 / (2 - 2 * u), 1.0 / (Configs.NC + 1))
        
        c1 = PIndividual()
        c2 = PIndividual()

        for i in range(ProblemManager.USSD):
            g1 = 0.5 * ((1 + beta) * par1.gene[i] + (1 - beta) * par2.gene[i])
            g2 = 0.5 * ((1 + beta) * par2.gene[i] + (1 - beta) * par1.gene[i])

            c1.gene[i] = max(0, min(1, g1))
            c2.gene[i] = max(0, min(1, g2))

        offspring: 'list[PIndividual]'
        offspring = []
        #ArrayList<PIndividual> offspring = new ArrayList<PIndividual>();
        offspring.append(c1)
        offspring.append(c2)
        return offspring
    

    def updateEvaluation(self) -> None:
        #ArrayList<PIndividual> indivs = new ArrayList<PIndividual>();
        indivs: 'list[PIndividual]'
        indivs = []
        indivs = indivs + self.indivs
        
        for k in range(ProblemManager.getTaskNumber()):

            #greater fitness <->
            indivs.sort(reverse=True, key=lambda x: x.getFitness(k))

            for rank in range(len(indivs)):
                indiv = indivs[rank]
                indiv.factorialRank[k] = rank+1
                scalarFitness = 1.0 / indiv.factorialRank[k]
                if (k == 0 or indiv.scalarFitness < scalarFitness):
                    indiv.scalarFitness = scalarFitness
            if (len(self.best) <= k):
                self.best.append(indivs[0].duplicate())
                
                continue
            if (self.best[k].getFitness(k) < indivs[0].getFitness(k)):
                self.best[k] = indivs[0].duplicate()

    def executeSelection(self) -> None:
        self.sortByScalarFitness()
        while (len(self.indivs) > Configs.P_POP_SIZE):
            del self.indivs[len(self.indivs) - 1]


    def sortByScalarFitness(self) -> None:
        self.indivs.sort(key=lambda indiv: -indiv.scalarFitness)
    

    def getIndivs(self) -> "list[PIndividual]":
        return self.indivs

    def setIndivs(self, indivs: 'list[PIndividual]'):
        self.indivs = indivs.copy()

    def getIndividual(self, index: int) -> PIndividual:
        return self.indivs[index]

    @dispatch(list)
    def getBest(self) -> 'list[PIndividual]': #type:ignore
        return self.best

    @dispatch(list)
    def setBest(self, best: 'list[PIndividual]'): #type:ignore
        self.best = best.copy()

    @dispatch(int)
    def getBest(self, task:int) -> PIndividual:
        return self.best[task]

    @dispatch(int, PIndividual)
    def setBest(self, task: int, indiv: PIndividual):
        self.best[task] = indiv

    def getPIndividual(self, index:int) -> PIndividual:
        return self.indivs[index]

    @dispatch(PIndividual)
    def addIndividual(self, indiv: PIndividual): #type:ignore
        self.indivs.append(indiv)

    @dispatch(list)
    def addIndividuals(self, indivs: 'list[PIndividual]'):
        self.indivs = self.indivs + indivs

    

