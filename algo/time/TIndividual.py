import sys

from algo.path.PIndividual import PIndividual
from elements.Charger import Charger
from elements.Sensor import Sensor
from problem.Configs import Configs
from problem.ProblemManager import ProblemManager
from typing import overload

class TIndividual:
	#private static long counter = 0;
    counter = 0
    """private static long counter"""

	#private static int[][] path;
    path: 'list[list[int]]'
    """private static int[][] path"""
    path = []   

	#private static double[][] greedyChargingTimeRatio;
    greedyChargingTimeRatio: 'list[list[float]]'
    """private static double[][] greedyChargingTimeRatio"""
    greedyChargingTimeRatio = []

	#private long id;
    id: int

	#private double[] chargingTime;
    chargingTime: 'list[float]'
    chargingTime = []

    #private double[] gene;
    gene: 'list[float]'
    gene = []

    #private int skillFactor;
    skillFactor: int

    #private double scalarFitness;
    scalarFitness: float

    #private double fitness;
    fitness: float

    #private int[] factorialRank;
    factorialRank: 'list[int]'
    factorialRank = []

    def __init__(self) -> None:
        TIndividual.counter += 1
        self.id = self.counter
        self.gene = []
        for i in range(ProblemManager.USSD):
            self.gene.append(float())
        self.factorialRank = []
        for i in range(ProblemManager.getTaskNumber()):
            self.factorialRank.append(int())


    def randomInit(self) -> None:
        sum = 0.0
        for i in range(len(self.gene)):
            self.gene[i] = Configs.rand.uniform(0,1)
            sum += self.gene[i]

        for i in range(len(self.gene)):
            self.gene[i] /= sum


    def initByGreedyTime(self) -> None:
        for i in range(len(self.gene)):
            if (i < len(self.greedyChargingTimeRatio[self.skillFactor])):
                self.gene[i] = self.greedyChargingTimeRatio[self.skillFactor][i]
            else:
                self.gene[i] = Configs.rand.uniform(0,1)
            
    def decoding(self) -> None:
        ch = ProblemManager.chargers[self.skillFactor]
        maxChargingTime = ch.getMaxChargingTime(TIndividual.path[self.skillFactor])
        n = len(TIndividual.path[self.skillFactor])


        for i in range(n):
            self.chargingTime.append(maxChargingTime * self.gene[i]) 

    def repairTime(self) -> None:
        self.decoding()
        n = len(TIndividual.path[self.skillFactor])
        ch = ProblemManager.chargers[self.skillFactor]
        maxChargingTime = ch.getMaxChargingTime(TIndividual.path[self.skillFactor])
        

        sum = 0.0
        for i in range(n):
            if (self.chargingTime[i] < 0):
                self.chargingTime[i] = 0
            sum += self.chargingTime[i]
        
        if (sum > maxChargingTime):
            exceed = sum - maxChargingTime
            delta = []
            sumDelta = 0.0
            for i in range(n):
                delta.append(Configs.rand.uniform(0,1))
                sumDelta += delta[i]
            
            for i in range(n):
                self.chargingTime[i] -= exceed * delta[i] / sumDelta
            
        arriveTime: 'list[float]'
        arriveTime = [0.0] * n
        arriveTime[0] = ProblemManager.distance[ProblemManager.serviceStation.id][TIndividual.path[self.skillFactor][0]] / ch.speed
        for i in range(n):
            s = ProblemManager.getSensorById(TIndividual.path[self.skillFactor][i])

            eRemain = s.E0 - arriveTime[i] * s.p
            ub = (Configs.S_EMAX - eRemain) / (ch.U - s.p)

            if eRemain < Configs.S_EMIN or self.chargingTime[i] < 0:
                self.chargingTime[i] = 0
            elif self.chargingTime[i] > ub:
                self.chargingTime[i] = ub
            

            if i < n - 1:
                arriveTime[i + 1] = arriveTime[i] + self.chargingTime[i] \
                        + ProblemManager.distance[TIndividual.path[self.skillFactor][i]][TIndividual.path[self.skillFactor][i + 1]] / ch.speed

    def calculateFitness(self) -> float:
        self.decoding()
        dead = 0
        totalLifetime = 0.0
        maxLifetime = 0.0
        
        n = len(TIndividual.path[self.skillFactor])
        arriveTime = [0.0] * n
        ch = ProblemManager.chargers[self.skillFactor]
        visited = [False]*(ProblemManager.maxSensorId + 1)

        # repairing
        self.repairTime()

        # calculate fintess
        for i in range(n):
            s = ProblemManager.getSensorById(TIndividual.path[self.skillFactor][i])
            visited[s.id] = True
            eRemain = s.E0 - arriveTime[i] * s.p
            eAfterT = s.E0 - Configs.T * s.p + self.chargingTime[i] * ch.getU()

            if eRemain < s.getEmin() or eAfterT < s.getEmin():
                dead += 1
            
            
            lifetime = (s.getE0() + self.chargingTime[i] * ch.getU() - s.getEmin()) / s.getP()
            totalLifetime += lifetime
            maxLifetime = max(lifetime, maxLifetime)
        

        for s in ProblemManager.subNet[self.skillFactor]:
            if not visited[s.getId()]:
                eAfterT = s.getE0() - Configs.T * s.getP()
                if eAfterT < Configs.S_EMIN:
                    dead+=1
                
                lifetime = s.getLifetime()
                totalLifetime += lifetime
                maxLifetime = max(lifetime, maxLifetime)

        netSize = len(ProblemManager.subNet[self.skillFactor])
        networkSurvivability = (netSize - dead) / netSize

        return networkSurvivability


    
    def mutation(self) -> None:
        """polynormial mutation"""
        u = 0.0
        for i in range(len(self.gene)):
            u = Configs.rand.uniform(0,1); # generate random u in [0, 1]
            if (u <= 0.5):
                deltaL = pow(2 * u, 1.0 / (Configs.NM + 1)) - 1
                p = self.gene[i] * (1.0 + deltaL)
                self.gene[i] = max(0, min(1, p))
            else:
                deltaR = 1.0 - pow(2 * (1 - u), 1.0 / (Configs.NM + 1))
                p = self.gene[i] + deltaR * (1 - self.gene[i])
                self.gene[i] = max(0, min(1, p))



    def setGene(self, _gene: 'list[float]'):
        self.gene = _gene



    # public void setGene(int index, double value):
    #     gene[index] = value;
    # }



    # public int getSkillFactor() {
    #     return skillFactor;
    # }

    # public void setSkillFactor(int skillFactor) {
    #     this.skillFactor = skillFactor;
    # }

    # public double getScalarFitness() {
    #     return scalarFitness;
    # }

    # public void setScalarFitness(double scalarFitness) {
    #     this.scalarFitness = scalarFitness;
    # }

    def getFitness(self, task: int) -> float:
        if (task == self.skillFactor):
            return self.fitness
        else:
            return sys.float_info.max

    # public void setFitness(double value) {
    #     fitness = value;
    # }

    # public int[] getFactorialRank() {
    #     return factorialRank;
    # }

    # public int getFactorialRank(int task) {
    #     return factorialRank[task];
    # }

    # public void setFactorialRank(int[] factorialRank) {
    #     this.factorialRank = factorialRank;
    # }

    # public void setFactorialRank(int task, int factorialRank) {
    #     this.factorialRank[task] = factorialRank;
    # }

    # public long getId() {
    #     return id;
    # }

    # public double[] getChargingTime() {
    #     return chargingTime;
    # }

    # public void setChargingTime(double[] chargingTime) {
    #     this.chargingTime = chargingTime;
    # }

    # public double getChargingTime(int index) {
    #     return this.chargingTime[index];
    # }

    def clone(self) -> PIndividual:
        indiv =  PIndividual()
        indiv.gene = self.gene.copy()
        return indiv

    # public static int[][] getPath() {
    #     return path;
    # }

    # public static void setPath(int[][] path) {
    #     TIndividual.path = path;
    # }

    # public double getFitness() {
    #     return fitness;
    # }
    @staticmethod
    def setGreedyChargingTime(time: 'list[list[float]]') -> None:
        n = len(time)

        TIndividual.greedyChargingTimeRatio = [] * n

        for a in range(n):
            maxChargingTime = ProblemManager.chargers[a].getMaxChargingTime(TIndividual.path[a])
            TIndividual.greedyChargingTimeRatio[a] = [0.0] * len(time[a])
            for i in range(len(time[a])):
                TIndividual.greedyChargingTimeRatio[a][i] = time[a][i] / maxChargingTime


