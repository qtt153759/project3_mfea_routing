package algo.path;

import java.io.Console;
import java.util.List;

import algo.path.reproduction.Reproductioner;
import problem.Configs;
import problem.ProblemManager;
import problem.Solution;

public class PSolver {

	private static PPopulation pop;
	public static Reproductioner reproductioner;

	public static Solution solve() {
		pop = new PPopulation();
		pop.randomInit();
		pop.updateEvaluation();
		pop.sortByScalarFitness();

		int k = Configs.P_POP_SIZE / 2;
		int gen = 0;
		while (++gen < Configs.P_GENERATIONS) {
			System.out.println("gen " + gen);
			List<PIndividual> offspring = reproductioner.reproduction(pop);

			for (int i = 0; i < k; i++) {
				offspring.add(pop.getIndividual(i));
			}

			pop.getIndivs().clear();
			pop.addIndividuals(offspring);
			pop.updateEvaluation();
			pop.executeSelection();

//			System.out.print(gen + "\t");
//			for (int i = 0; i < ProblemManager.getTaskNumber(); i++) {
//				System.out.print(pop.getBest(i).getFitness(i) + "\t");
//			}
//			System.out.println();
		}

		return new Solution(pop.getBest());
	}
}
