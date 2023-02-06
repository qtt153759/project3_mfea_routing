from algo.path.PPopulation import PPopulation
from algo.path.reproduction.Reproductioner import Reproductioner
from problem.Solution import Solution
from problem.Configs import Configs
from problem.ProblemManager import ProblemManager
class PSolver:
    #private static PPopulation pop;
    pop: PPopulation

    #public static Reproductioner reproductioner;
    reproductioner: Reproductioner

    @staticmethod
    def solve() -> Solution:

        #generate an initial population (1)
        PSolver.pop = PPopulation()
        PSolver.pop.randomInit()

        #
        PSolver.pop.updateEvaluation()
        PSolver.pop.sortByScalarFitness()

        k = int(Configs.P_POP_SIZE / 2)
        gen = 0
        while gen < Configs.P_GENERATIONS:
            gen += 1
            print(f"gen: {gen}")
            offspring = PSolver.reproductioner.reproduction(PSolver.pop)

            for i in range(k):
                offspring.append(PSolver.pop.indivs[i])

            PSolver.pop.indivs.clear()
            PSolver.pop.addIndividuals(offspring)
            PSolver.pop.updateEvaluation()
            PSolver.pop.executeSelection()

# //			System.out.print(gen + "\t");
# //			for (int i = 0; i < ProblemManager.getTaskNumber(); i++) {
# //				System.out.print(pop.getBest(i).getFitness(i) + "\t");
# //			}
# //			System.out.println();

        return Solution(PSolver.pop.best)
    

