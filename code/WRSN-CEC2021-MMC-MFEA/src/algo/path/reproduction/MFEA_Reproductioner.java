package algo.path.reproduction;

import java.util.ArrayList;
import java.util.List;

import algo.path.PIndividual;
import algo.path.PPopulation;
import problem.Configs;
import problem.ProblemManager;

public class MFEA_Reproductioner implements Reproductioner {

	@Override
	@SuppressWarnings("unchecked")
	public List<PIndividual> reproduction(PPopulation pop) {
		ArrayList<PIndividual> offspring = new ArrayList<PIndividual>();

		ArrayList<PIndividual> matingPool = new ArrayList<PIndividual>();
		int k = pop.getIndivs().size() / 2;
		for (int i = 0; i < k; i++) {
			matingPool.add(pop.getIndividual(i));
		}

		ArrayList<PIndividual>[] subPop = new ArrayList[ProblemManager.getTaskNumber()];
		for (int i = 0; i < subPop.length; i++) {
			subPop[i] = new ArrayList<PIndividual>();
			for (PIndividual indiv : matingPool) {
				if (indiv.getSkillFactor() == i) {
					subPop[i].add(indiv);
				}
			}
		}

		PIndividual p1, p2, par1, par2;
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
			ArrayList<PIndividual> child;
			if (t1 == t2) {
				// intra-taks crossover
				child = pop.crossover(par1, par2);
				for (PIndividual indiv : child) {
					indiv.setSkillFactor(t1);
					indiv.mutation();
				}
				pop.selfUX(child.get(0), child.get(1));
			} else if (Configs.rand.nextDouble() < Configs.RMP) {
				// inter-taks crossover
				child = pop.crossover(par1, par2);
				for (PIndividual indiv : child) {
					indiv.setSkillFactor(Configs.rand.nextBoolean() ? t1 : t2);
					indiv.mutation();
				}
			}

			else {
				subPop[t1].remove(par1);
				PIndividual p = subPop[t1].get(Configs.rand.nextInt(subPop[t1].size()));
				subPop[t1].add(par1);
				ArrayList<PIndividual> child1 = pop.crossover(par1, p);
				for (PIndividual indiv : child1) {
					indiv.mutation();
					indiv.setSkillFactor(t1);
				}
				pop.selfUX(child1.get(0), child1.get(1));

				subPop[t2].remove(par2);
				p = subPop[t2].get(Configs.rand.nextInt(subPop[t2].size()));
				subPop[t2].add(par2);
				ArrayList<PIndividual> child2 = pop.crossover(par2, p);
				for (PIndividual indiv : child2) {
					indiv.mutation();
					indiv.setSkillFactor(t2);
				}
				pop.selfUX(child1.get(0), child1.get(1));

				child = new ArrayList<PIndividual>();
				child.add(child1.get(0));
				child.add(child2.get(0));
			}

			for (PIndividual indiv : child) {
				indiv.setFitness(indiv.calculateFitness());
				offspring.add(indiv);
			}
		}

		return offspring;
	}
}
