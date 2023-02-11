from algo.path.reproduction.Reproductioner import Reproductioner
from algo.path.PIndividual import PIndividual

from algo.path.PPopulation import PPopulation

from problem.Configs import Configs
from problem.ProblemManager import ProblemManager

class GA_Reproductioner(Reproductioner):
    def reproduction(self, pop: PPopulation)-> 'list[PIndividual]':
        offspring: 'list[PIndividual]'
        matingPool: 'list[PIndividual]'
        offspring = []
        matingPool = []
        k = len(pop.indivs) / 2
        for i in range(int(k)):
            matingPool.append(pop.indivs[i])
        p1 = PIndividual()
        p2 = PIndividual()
        par1 = PIndividual()
        par2 = PIndividual()
        while len(offspring) < Configs.P_POP_SIZE:
            #  select first parent by using binary tournament selection
            # print(len(matingPool),Configs.rand.randint(0, len(matingPool)))
            p1 = matingPool.pop(Configs.rand.randint(0, len(matingPool)-1))
            p2 = matingPool.pop(Configs.rand.randint(0, len(matingPool)-1))
            if p1.scalarFitness >= p2.scalarFitness:
                par1 = p1
                matingPool.append(p2)
            else:
                par1 = p2
                matingPool.append(p1)
            #  select the second parent
            p1 = matingPool.pop(Configs.rand.randint(0, len(matingPool)-1))
            p2 = matingPool.pop(Configs.rand.randint(0, len(matingPool)-1))
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
            child: 'list[PIndividual]'
            child = []
            if t1 == t2 or Configs.rand.uniform(0,1) < Configs.RMP:
                child = pop.crossover(par1, par2)
                for indiv in child:
                    skill = Configs.rand.uniform(0,1)
                    if skill >= 0.5:
                        skill = t1
                    else: 
                        skill = t2
                    indiv.skillFactor = skill
                    indiv.fitness =  indiv.calculateFitness()
                    offspring.append(indiv)
            else:
                c1 = par1.clone()
                c1.mutation()
                c1.fitness = c1.calculateFitness()

                c2 = par2.clone()
                c2.mutation()
                c2.fitness = c2.calculateFitness()
                offspring.append(c1)
                offspring.append(c2)
        
        # for i in range(len(offspring)):
        #     if Configs.rand.uniform(0,1)<0.1:
        #         # print("before",offspring[i].fitness)
        #         offspring[i]=offspring[i].tsp_2_opt()
        #         # print("after",offspring[i].fitness)



        return offspring