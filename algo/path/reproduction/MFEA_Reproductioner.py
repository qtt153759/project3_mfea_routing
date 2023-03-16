from algo.path.PPopulation import PPopulation
from algo.path.PIndividual import PIndividual
from problem.Configs import Configs
from algo.path.reproduction.Reproductioner import Reproductioner

from problem.ProblemManager import ProblemManager

class MFEA_Reproductioner(Reproductioner):

    def reproduction(self, pop) -> 'list[PIndividual]':
        """ generated source for method reproduction """
        offspring: 'list[PIndividual]'
        matingPool: 'list[PIndividual]'
        offspring = []
        matingPool = []
        k = len(pop.indivs) / 2
        
        for i in range(int(k)):
            matingPool.append(pop.getIndividual(i))
        subPop: 'list[list[PIndividual]]'
        subPop = []
        for i in range(ProblemManager.getTaskNumber()):
            subPop.append([])
            for indiv in matingPool:
                if indiv.skillFactor == i:
                    subPop[i].append(indiv)
        p1 = PIndividual()
        p2 = PIndividual()
        par1 = PIndividual()
        par2 = PIndividual()
        while len(offspring) < Configs.P_POP_SIZE:
            #  select first parent by using binary tournament selection
            p1 = matingPool.pop(Configs.rand.randint(0, len(matingPool) -1))
            p2 = matingPool.pop(Configs.rand.randint(0, len(matingPool) -1))
            if p1.scalarFitness >= p2.scalarFitness:
                par1 = p1
                matingPool.append(p2)
            else:
                par1 = p2
                matingPool.append(p1)
            #  select the second parent
            p1 = matingPool.pop(Configs.rand.randint(0, len(matingPool) -1))
            p2 = matingPool.pop(Configs.rand.randint(0, len(matingPool) -1))
            if p1.scalarFitness >= p2.scalarFitness:
                par2 = p1
                matingPool.append(p2)
            else:
                par2 = p2
                matingPool.append(p1)
            matingPool.append(par1)
            matingPool.append(par2)
            t1 = par1.skillFactor
            t2 = par2.skillFactor
            if t1 == t2:
                #  intra-taks crossover
                child = pop.crossover(par1, par2)
                for indiv in child:
                    indiv.skillFactor = t1
                    indiv.mutation()
                pop.selfUX(child[0], child[1])
            elif Configs.rand.uniform(0, 1) < Configs.RMP:
                #  inter-taks crossover
                child = pop.crossover(par1, par2)
                for indiv in child:
                    if Configs.rand.uniform(0,1) >= 0.5:
                        indiv.skillFactor = t1
                    else:
                        indiv.skillFactor = t2
                    indiv.mutation()
            else:
                subPop[t1].remove(par1)
                p = subPop[t1][Configs.rand.randint(0, len(subPop[t1])-1)]
                subPop[t1].append(par1)
                child1 = pop.crossover(par1, p)
                for indiv in child1:
                    indiv.mutation()
                    indiv.skillFactor = t1
                pop.selfUX(child1[0], child1[1])
                subPop[t2].remove(par2)
                p = subPop[t2][Configs.rand.randint(0, len(subPop[t2])-1)]
                subPop[t2].append(par2)
                child2 = pop.crossover(par2, p)
                for indiv in child2:
                    indiv.mutation()
                    indiv.skillFactor = t2
                pop.selfUX(child1[0], child1[1])
                child = []
                child.append(child1[0])
                child.append(child2[0])
            for indiv in child:
                indiv.fitness = indiv.calculateFitness()
                offspring.append(indiv)
        print(len(offspring))
        if Configs.mode=="two_opt":
            for i in range(len(offspring)):
                if Configs.rand.uniform(0,1)<0.1:
                    # print("before ",i,offspring[i].fitness)
                    # tmp=offspring[i].fitness
                    offspring[i]=offspring[i].tsp_2_opt()
                    # print("after",i,tmp-offspring[i].fitness)

        elif Configs.mode=="three_opt":
            for i in range(len(offspring)):
                if Configs.rand.uniform(0,1)<0.1:
                    tmp= offspring[i].fitness
                    offspring[i]=offspring[i].tsp_3_opt()
                    # print("after",i,tmp-offspring[i].fitness)
        return offspring