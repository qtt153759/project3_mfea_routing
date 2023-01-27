package algo.time;

import java.util.ArrayList;
import java.util.List;

import problem.Configs;
import problem.ProblemManager;

public class TSolver {

	private static TPopulation pop;

	public static double[][] solve() {
		pop = new TPopulation();
		pop.init();
		pop.updateEvaluation();
		pop.sortByScalarFitness();

		int k = Configs.P_POP_SIZE / 2;
		int gen = 0;
		while (++gen < Configs.P_GENERATIONS) {
			List<TIndividual> offspring = reproduction();

			for (int i = 0; i < k; i++) {
				offspring.add(pop.getIndividual(i));
			}

			pop.getIndivs().clear();
			pop.addIndividuals(offspring);
			pop.updateEvaluation();
			pop.executeSelection();

			System.out.print(gen + "\t");
			for (int i = 0; i < ProblemManager.getTaskNumber(); i++) {
				System.out.print(pop.getBest(i).getFitness(i) + "\t");
			}
			System.out.println();
		}

		double[][] time = new double[ProblemManager.chargers.size()][];
		for (int a=0; a<time.length; a++) {
			TIndividual indiv = pop.getBest(a);
			time[a] = indiv.getChargingTime().clone();
		}
		return time;
	}

	@SuppressWarnings("unchecked")
	public static List<TIndividual> reproduction() {
		ArrayList<TIndividual> offspring = new ArrayList<TIndividual>();

		ArrayList<TIndividual> matingPool = new ArrayList<TIndividual>();
		int k = pop.getIndivs().size();
		for (int i = 0; i < k; i++) {
			matingPool.add(pop.getIndividual(i));
		}

		ArrayList<TIndividual>[] subPop = new ArrayList[ProblemManager.getTaskNumber()];
		for (int i = 0; i < subPop.length; i++) {
			subPop[i] = new ArrayList<TIndividual>();
			for (TIndividual indiv : matingPool) {
				if (indiv.getSkillFactor() == i) {
					subPop[i].add(indiv);
				}
			}
		}

		TIndividual p1, p2, par1, par2;
		while (offspring.size() < Configs.P_POP_SIZE) {
			// select first parent by using binary tournament selection
			p1 = matingPool.remove(Configs.rand.nextInt(matingPool.size() / 2));
			p2 = matingPool.remove(Configs.rand.nextInt(matingPool.size() / 2));

			if (p1.getScalarFitness() >= p2.getScalarFitness()) {
				par1 = p1;
				matingPool.add(p2);
			} else {
				par1 = p2;
				matingPool.add(p1);
			}

			// select the second parent
			p1 = matingPool.remove(Configs.rand.nextInt(matingPool.size() / 2));
			p2 = matingPool.remove(Configs.rand.nextInt(matingPool.size() / 2));

			if (p1.getScalarFitness() >= p2.getScalarFitness()) {
				par2 = p1;
				matingPool.add(p2);
			} else {
				par2 = p2;
				matingPool.add(p1);
			}

			matingPool.add(par1);
			matingPool.add(par2);

			int t1 = par1.getSkillFactor();
			int t2 = par2.getSkillFactor();
			ArrayList<TIndividual> child;
			if (t1 == t2) {
				// intra-taks crossover
				child = pop.crossover(par1, par2);
				for (TIndividual indiv : child) {
					indiv.setSkillFactor(t1);
					indiv.mutation();
				}
				pop.selfUX(child.get(0), child.get(1));
			} else if (Configs.rand.nextDouble() < Configs.RMP) {
				// inter-taks crossover
				child = pop.crossover(par1, par2);
				for (TIndividual indiv : child) {
					indiv.setSkillFactor(Configs.rand.nextBoolean() ? t1 : t2);
					indiv.mutation();
				}
			}

			else {
				subPop[t1].remove(par1);
				TIndividual p = subPop[t1].get(Configs.rand.nextInt(subPop[t1].size()));
				subPop[t1].add(par1);
				ArrayList<TIndividual> child1 = pop.crossover(par1, p);
				for (TIndividual indiv : child1) {
					indiv.mutation();
					indiv.setSkillFactor(t1);
				}
				pop.selfUX(child1.get(0), child1.get(1));

				subPop[t2].remove(par2);
				p = subPop[t2].get(Configs.rand.nextInt(subPop[t2].size()));
				subPop[t2].add(par2);
				ArrayList<TIndividual> child2 = pop.crossover(par2, p);
				for (TIndividual indiv : child2) {
					indiv.mutation();
					indiv.setSkillFactor(t2);
				}
				pop.selfUX(child1.get(0), child1.get(1));

				child = new ArrayList<TIndividual>();
				child.add(child1.get(0));
				child.add(child2.get(0));
			}

			for (TIndividual indiv : child) {
				indiv.setFitness(indiv.calculateFitness());
				offspring.add(indiv);
			}
		}

		return offspring;
	}
}
