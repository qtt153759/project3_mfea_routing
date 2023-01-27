package algo.time;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Comparator;

import problem.Configs;
import problem.ProblemManager;

public class TPopulation {

	private ArrayList<TIndividual> indivs;
	private TIndividual[] best;

	public TPopulation() {
		indivs = new ArrayList<TIndividual>();
		best = new TIndividual[ProblemManager.getTaskNumber()];
	}

	public void init() {
		indivs.clear();
		
//		for (int i = 0; i < ProblemManager.getTaskNumber(); i++) {
//			TIndividual indiv = new TIndividual();
//			int skill = i % ProblemManager.getTaskNumber();
//			indiv.setSkillFactor(skill);
//			indiv.initByGreedyTime();
//			indiv.setFitness(indiv.calculateFitness());
//			indivs.add(indiv);
//		}
		
		for (int i = indivs.size(); i < Configs.P_POP_SIZE; i++) {
			TIndividual indiv = new TIndividual();
			int skill = i % ProblemManager.getTaskNumber();
			indiv.setSkillFactor(skill);
			indiv.randomInit();
			indiv.setFitness(indiv.calculateFitness());
			indivs.add(indiv);
		}
	}

	public void selfUX(TIndividual par1, TIndividual par2) {
		int n = ProblemManager.USSD;
		for (int i = 0; i < n; i++) {
			if (Configs.rand.nextBoolean()) {
				double tmp = par1.getGene(i);
				par1.setGene(i, par2.getGene(i));
				par2.setGene(i, tmp);
			}
		}
	}

	/**
	 * simulated binary crossover
	 * 
	 * @param par1
	 * @param par2
	 * @return
	 */
	public ArrayList<TIndividual> crossover(TIndividual par1, TIndividual par2) {
		double u = Configs.rand.nextDouble();
		double beta;
		if (u <= 0.5) {
			beta = Math.pow(2 * u, 1.0 / (Configs.NC + 1));
		} else {
			beta = Math.pow(1.0 / (2 - 2 * u), 1.0 / (Configs.NC + 1));
		}

		TIndividual c1 = new TIndividual();
		TIndividual c2 = new TIndividual();

		for (int i = 0; i < ProblemManager.USSD; i++) {
			double g1 = 0.5 * ((1 + beta) * par1.getGene(i) + (1 - beta) * par2.getGene(i));
			double g2 = 0.5 * ((1 + beta) * par2.getGene(i) + (1 - beta) * par1.getGene(i));

			c1.setGene(i, Math.max(0, Math.min(1, g1)));
			c2.setGene(i, Math.max(0, Math.min(1, g2)));
		}

		ArrayList<TIndividual> offspring = new ArrayList<TIndividual>();
		offspring.add(c1);
		offspring.add(c2);
		return offspring;
	}

	public void updateEvaluation() {
		ArrayList<TIndividual> indivs = new ArrayList<TIndividual>();
		indivs.addAll(this.getIndivs());

		for (int k = 0; k < ProblemManager.getTaskNumber(); k++) {
			final int task = k;
			indivs.sort(new Comparator<TIndividual>() {
				@Override
				public int compare(TIndividual o1, TIndividual o2) {
					// TODO Auto-generated method stub
					return -Double.valueOf(o1.getFitness(task)).compareTo(o2.getFitness(task));
				}
			});

			for (int rank = 0; rank < indivs.size(); rank++) {
				TIndividual indiv = indivs.get(rank);
				indiv.setFactorialRank(k, rank + 1);
				double scalarFitness = 1.0 / indiv.getFactorialRank(k);
				if (k == 0 || indiv.getScalarFitness() < scalarFitness) {
					indiv.setScalarFitness(scalarFitness);
				}
			}

			if (best[k] == null || best[k].getFitness(k) < indivs.get(0).getFitness(k)) {
				best[k] = indivs.get(0);
			}
		}
	}

	public void executeSelection() {
		this.sortByScalarFitness();
		while (this.getIndivs().size() > Configs.P_POP_SIZE) {
			this.getIndivs().remove(this.getIndivs().size() - 1);
		}
	}

	public void sortByScalarFitness() {
		this.getIndivs().sort(new Comparator<TIndividual>() {
			@Override
			public int compare(TIndividual o1, TIndividual o2) {
				// TODO Auto-generated method stub
				return -Double.valueOf(o1.getScalarFitness()).compareTo(o2.getScalarFitness());
			}
		});
	}

	public ArrayList<TIndividual> getIndivs() {
		return indivs;
	}

	public void setIndivs(ArrayList<TIndividual> indivs) {
		this.indivs = indivs;
	}

	public TIndividual getIndividual(int index) {
		return indivs.get(index);
	}

	public TIndividual[] getBest() {
		return best;
	}

	public void setBest(TIndividual[] best) {
		this.best = best;
	}

	public TIndividual getBest(int task) {
		return best[task];
	}

	public void setBest(int task, TIndividual indiv) {
		best[task] = indiv;
	}

	public TIndividual geTIndividual(int index) {
		return indivs.get(index);
	}

	public void addIndividual(TIndividual indiv) {
		indivs.add(indiv);
	}

	public void addIndividuals(Collection<TIndividual> indivs) {
		this.indivs.addAll(indivs);
	}
}
