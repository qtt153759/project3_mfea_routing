package algo.path;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import elements.Charger;
import elements.Sensor;
import problem.Configs;
import problem.ProblemManager;

public class PIndividual {
	private static long counter = 0;
	private long id;

	private ArrayList<Integer> path;
	private double[] chargingTime;

	private double[] gene;
	
	private int skillFactor;
	private double scalarFitness;
	private double fitness;
	private int[] factorialRank;

	public PIndividual() {
		id = ++counter;
		gene = new double[ProblemManager.USSD];
		this.factorialRank = new int[ProblemManager.getTaskNumber()];
	}

	public void randomInit() {
		for (int i = 0; i < gene.length; i++) {
			gene[i] = Configs.rand.nextDouble();
		}
	}

	@SuppressWarnings("unchecked")
	public void decoding(int taskIndex) {
		path = new ArrayList<Integer>();

		List<Allele> list = new ArrayList<Allele>();
		ArrayList<Sensor> sectors = ProblemManager.subNet[taskIndex];
		int n = sectors.size();

		for (int i = 0; i < n; i++) {
			Sensor s = sectors.get(i);
			if (s.getLifetime() > Configs.T) {
				gene[i] = 0.5 + 0.5 * Configs.rand.nextDouble();
			}
			if (gene[i] <= 0.5) {
				list.add(new Allele(gene[i], s.getId()));
			}
		}

		if (list.size() == 0) {
			list.add(new Allele(gene[0], sectors.get(0).getId()));
		}

		Collections.sort(list);
		for (Allele a : list) {
			path.add(a.getSensorId());
		}
	}

	public double calculateFitness() {
		this.decoding(skillFactor);
		double w[] = this.getPriority();

		int dead = 0;
		double totalLifetime = 0;
		double maxLifetime = 0;

		int n = path.size();
		double[] arriveTime = new double[n];
		boolean visited[] = new boolean[ProblemManager.maxSensorId + 1];
		chargingTime = new double[n];

		Charger ch = ProblemManager.chargers.get(skillFactor);
		double maxChargingTime = ch.getMaxChargingTime(path);

		// repairing
		arriveTime[0] = ProblemManager.distance[ProblemManager.serviceStation.getId()][path.get(0)] / ch.getSpeed();
		for (int i = 0; i < n; i++) {
			Sensor s = ProblemManager.getSensorById(path.get(i));
			chargingTime[i] = w[i] * maxChargingTime;
			visited[s.getId()] = true;

			double eRemain = s.getE0() - arriveTime[i] * s.getP();
			double ub = (Configs.S_EMAX - eRemain) / (ch.getU() - s.getP());
			if (eRemain < Configs.S_EMIN) {
				chargingTime[i] = 0;
			} else if (chargingTime[i] > ub || true) {
				chargingTime[i] = ub;
			}
			double eAfterT = s.getE0() - Configs.T * s.getP() + chargingTime[i] * ch.getU();

			if (eRemain < s.getEmin() - 1e-3 || eAfterT < s.getEmin() - 1e-3) {
				dead++;
			}

			double lifetime = (s.getE0() + chargingTime[i] * ch.getU() - s.getEmin()) / s.getP();
			totalLifetime += lifetime;
			maxLifetime = Math.max(lifetime, maxLifetime);

			if (i < n - 1) {
				arriveTime[i + 1] = arriveTime[i] + chargingTime[i]
						+ ProblemManager.distance[path.get(i)][path.get(i + 1)] / ch.getSpeed();
			}
		}

		for (Sensor s : ProblemManager.subNet[this.skillFactor]) {
			if (!visited[s.getId()]) {
				double lifetime = s.getLifetime();
				if (lifetime < Configs.T) {
					dead++;
				}

				totalLifetime += lifetime;
				maxLifetime = Math.max(lifetime, maxLifetime);
			}
		}

		double netSize = ProblemManager.subNet[this.skillFactor].size();
		double networkSurvivability = (netSize - dead) / (1.0 * netSize);
		double avgLifetime = totalLifetime / (1.0 * netSize);

		return networkSurvivability;
	}

	public double[] getPriority() {
		double[] priority = new double[path.size()];

		double sum = 0;
		for (int i = 0; i < path.size(); i++) {
			Sensor s = ProblemManager.getSensorById(path.get(i));
			priority[i] = s.getW();
			sum += priority[i];
		}

		for (int i = 0; i < path.size(); i++) {
			priority[i] /= sum;
		}

		return priority;
	}

	/**
	 * polynormial mutation
	 */
	public void mutation() {
		double u;
		for (int i = 0; i < gene.length; i++) {
			u = Configs.rand.nextDouble(); // generate random u in [0, 1]
			if (u <= 0.5) {
				double deltaL = Math.pow(2 * u, 1.0 / (Configs.NM + 1)) - 1;
				double p = this.getGene(i) * (1.0 + deltaL);
				this.setGene(i, Math.max(0, Math.min(1, p)));
			} else {
				double deltaR = 1.0 - Math.pow(2 * (1 - u), 1.0 / (Configs.NM + 1));
				double p = this.getGene(i) + deltaR * (1 - this.getGene(i));
				this.setGene(i, Math.max(0, Math.min(1, p)));
			}
		}
	}

	public double[] getGene() {
		return gene;
	}

	public void setGene(double[] gene) {
		this.gene = gene;
	}

	public void setGene(int index, double value) {
		gene[index] = value;
	}

	public double getGene(int index) {
		return gene[index];
	}

	public ArrayList<Integer> getPath() {
		return path;
	}

	public void setPath(ArrayList<Integer> path) {
		this.path = path;
	}

	public int getSkillFactor() {
		return skillFactor;
	}

	public void setSkillFactor(int skillFactor) {
		this.skillFactor = skillFactor;
	}

	public double getScalarFitness() {
		return scalarFitness;
	}

	public void setScalarFitness(double scalarFitness) {
		this.scalarFitness = scalarFitness;
	}

	public double getFitness(int task) {
		if (task == this.skillFactor) {
			return fitness;
		} else {
			return -Double.MAX_VALUE;
		}
	}

	public void setFitness(double value) {
		fitness = value;
	}

	public int[] getFactorialRank() {
		return factorialRank;
	}

	public int getFactorialRank(int task) {
		return factorialRank[task];
	}

	public void setFactorialRank(int[] factorialRank) {
		this.factorialRank = factorialRank;
	}

	public void setFactorialRank(int task, int factorialRank) {
		this.factorialRank[task] = factorialRank;
	}

	public long getId() {
		return id;
	}

	public double[] getChargingTime() {
		return chargingTime;
	}

	public void setChargingTime(double[] chargingTime) {
		this.chargingTime = chargingTime;
	}

	public double getChargingTime(int index) {
		return this.chargingTime[index];
	}

	public PIndividual clone() {
		PIndividual indiv = new PIndividual();
		indiv.setGene(this.getGene().clone());
		return indiv;
	}

}
