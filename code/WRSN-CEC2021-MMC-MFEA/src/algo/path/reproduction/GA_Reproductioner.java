package algo.path.reproduction;

import java.util.ArrayList;
import java.util.List;

import algo.path.PIndividual;
import algo.path.PPopulation;
import problem.Configs;

public class GA_Reproductioner implements Reproductioner {

	@Override
	public List<PIndividual> reproduction(PPopulation pop) {
		ArrayList<PIndividual> offspring = new ArrayList<PIndividual>();

		ArrayList<PIndividual> matingPool = new ArrayList<PIndividual>();
		int k = pop.getIndivs().size() / 2;
		for (int i = 0; i < k; i++) {
			matingPool.add(pop.getIndividual(i));
		}

		PIndividual p1, p2, par1, par2;
		while (offspring.size() < Configs.P_POP_SIZE) {
			// select first parent by using binary tournament selection
			p1 = matingPool.remove(Configs.rand.nextInt(matingPool.size()));
			p2 = matingPool.remove(Configs.rand.nextInt(matingPool.size()));

			if (p1.getScalarFitness() >= p2.getScalarFitness()) {
				par1 = p1;
				matingPool.add(p2);
			} else {
				par1 = p2;
				matingPool.add(p1);
			}

			// select the second parent
			p1 = matingPool.remove(Configs.rand.nextInt(matingPool.size()));
			p2 = matingPool.remove(Configs.rand.nextInt(matingPool.size()));

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
			if (t1 == t2 || Configs.rand.nextDouble() < Configs.RMP) {
				child = pop.crossover(par1, par2);
				for (PIndividual indiv : child) {
					int skill = Configs.rand.nextBoolean() ? t1 : t2;
					indiv.setSkillFactor(skill);
					indiv.setFitness(indiv.calculateFitness());
					offspring.add(indiv);
				}
			} else {
				PIndividual c1 = par1.clone();
				c1.setSkillFactor(t1);
				c1.mutation();
				c1.setFitness(c1.calculateFitness());

				PIndividual c2 = par2.clone();
				c2.setSkillFactor(t2);
				c2.mutation();
				c2.setFitness(c2.calculateFitness());

				offspring.add(c1);
				offspring.add(c2);
			}
		}

		return offspring;
	}

}
