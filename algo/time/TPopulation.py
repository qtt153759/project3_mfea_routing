from problem.Configs import Configs
from algo.time.TIndividual import TIndividual
from problem.ProblemManager import ProblemManager

class TPopulation(object):
    """ generated source for class TPopulation """
    indivs: 'list[TIndividual]'
    indivs = []

    best: 'list[TIndividual]'
    best = []

    def __init__(self):
        """ generated source for method __init__ """
        pass

    def init(self):
        """ generated source for method init """
        self.indivs.clear()
        for i in range(len(self.indivs), Configs.P_POP_SIZE):
            indiv = TIndividual()
            skill = i % ProblemManager.getTaskNumber()
            indiv.skillFactor = skill
            indiv.randomInit()
            indiv.fitness = indiv.calculateFitness()
            self.indivs.append(indiv)

    def selfUX(self, par1: TIndividual, par2: TIndividual):
        """ generated source for method selfUX """
        n = ProblemManager.USSD
        for i in range(n):
            if Configs.rand.uniform(0,1) < 0.5:
                tmp = par1.gene[i]
                par1.gene[i] =  par2.gene[i]
                par2.gene[i] = tmp

    # 
    # 	 * simulated binary crossover
    # 	 * 
    # 	 * @param par1
    # 	 * @param par2
    # 	 * @return
    # 	 
    def crossover(self, par1: TIndividual, par2: TIndividual):
        """ generated source for method crossover """
        u = Configs.rand.uniform(0, 1)
        beta = 0.0
        if u <= 0.5:
            beta = pow(2 * u, 1.0 / (Configs.NC + 1))
        else:
            beta = pow(1.0 / (2 - 2 * u), 1.0 / (Configs.NC + 1))

        c1 = TIndividual()
        c2 = TIndividual()

        for i in range(ProblemManager.USSD):
            g1 = 0.5 * ((1 + beta) * par1.gene[i] + (1 - beta) * par2.gene[i])
            g2 = 0.5 * ((1 + beta) * par2.gene[i] + (1 - beta) * par1.gene[i])

            c1.gene[i] = max(0, min(1, g1))
            c2.gene[i] = max(0, min(1, g2))

        offspring: 'list[TIndividual]'
        offspring = []
        offspring.append(c1)
        offspring.append(c2)
        return offspring

    def updateEvaluation(self):
        indivs: 'list[TIndividual]'
        indivs = self.indivs.copy()

        for k in range(ProblemManager.getTaskNumber()):
            task = k
            indivs.sort(key=lambda indiv: -indiv.getFitness(task))
            for rank in range(len(indivs)):
                indiv = indivs[rank]
                indiv.factorialRank[k] =  rank + 1
                scalarFitness = 1.0 / indiv.factorialRank[k]
                if k == 0 or indiv.scalarFitness < scalarFitness:
                    indiv.scalarFitness = scalarFitness

            if self.best[k] == None or self.best[k].getFitness(k) < indivs[0].getFitness(k):
                self.best[k] = indivs[0]

    def executeSelection(self):
        self.sortByScalarFitness()
        while len(self.indivs) > Configs.P_POP_SIZE:
            self.indivs.pop(len(self.indivs)-1)

    def sortByScalarFitness(self):
        self.indivs.sort(key=lambda indiv: -indiv.scalarFitness)

    # def getIndivs(self):
    #     """ generated source for method getIndivs """
    #     return self.indivs

    # def setIndivs(self, indivs):
    #     """ generated source for method setIndivs """
    #     self.indivs = indivs

    # def getIndividual(self, index):
    #     """ generated source for method getIndividual """
    #     return self.indivs[index]

    # @overloaded
    # def getBest(self):
    #     """ generated source for method getBest """
    #     return self.best

    # @overloaded
    # def setBest(self, best):
    #     """ generated source for method setBest """
    #     self.best = best

    # @getBest.register(object, int)
    # def getBest_0(self, task):
    #     """ generated source for method getBest_0 """
    #     return self.best[task]

    # @setBest.register(object, int, TIndividual)
    # def setBest_0(self, task, indiv):
    #     """ generated source for method setBest_0 """
    #     self.best[task] = indiv

    # def geTIndividual(self, index):
    #     """ generated source for method geTIndividual """
    #     return self.indivs.get(index)

    # def addIndividual(self, indiv):
    #     """ generated source for method addIndividual """
    #     self.indivs.add(indiv)

    # def addIndividuals(self, indivs):
    #     """ generated source for method addIndividuals """
    #     self.indivs.addAll(indivs)

