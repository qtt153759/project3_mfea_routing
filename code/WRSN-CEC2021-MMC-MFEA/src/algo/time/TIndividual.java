package algo.time;

import algo.path.PIndividual;
import elements.Charger;
import elements.Sensor;
import problem.Configs;
import problem.ProblemManager;

public class TIndividual {
	private static long counter = 0;
	private long id;

	private static int[][] path;
	private static double[][] greedyChargingTimeRatio;

	private double[] chargingTime;

	private double[] gene;
	private int skillFactor;
	private double scalarFitness;
	private double fitness;
	private int[] factorialRank;

	public TIndividual() {
		id = ++counter;
		gene = new double[ProblemManager.USSD];
		this.factorialRank = new int[ProblemManager.getTaskNumber()];
	}

	public void randomInit() {
		double sum = 0;
		for (int i = 0; i < gene.length; i++) {
			gene[i] = Configs.rand.nextDouble();
			sum += gene[i];
		}

		for (int i = 0; i < gene.length; i++) {
			gene[i] /= sum;
		}
	}

	public void initByGreedyTime() {
		for (int i=0; i<gene.length; i++) {
			if (i < greedyChargingTimeRatio[skillFactor].length) {
				gene[i] = greedyChargingTimeRatio[skillFactor][i];
			} else {
				gene[i] = Configs.rand.nextDouble();
			}
		}
	}

	public void decoding() {
		Charger ch = ProblemManager.chargers.get(skillFactor);
		double maxChargingTime = ch.getMaxChargingTime(path[skillFactor]);
		int n = path[skillFactor].length;
		this.chargingTime = new double[n];

		for (int i = 0; i < n; i++) {
			chargingTime[i] = maxChargingTime * gene[i];
		}
	}
	
	public void repairTime() {
		this.decoding();
		int n = path[skillFactor].length;
		Charger ch = ProblemManager.chargers.get(skillFactor);
		double maxChargingTime = ch.getMaxChargingTime(path[skillFactor]);
		
		
		double sum = 0;
		for (int i=0; i<n; i++) {
			if (chargingTime[i] < 0) {
				chargingTime[i] = 0;
			}
			sum += chargingTime[i];
		}
		
		if (sum > maxChargingTime) {
			double exceed = sum - maxChargingTime;
			
			double delta[] = new double[n];
			double sumDelta = 0;
			for (int i=0; i<n; i++) {
				delta[i] = Configs.rand.nextDouble();
				sumDelta += delta[i];
			}
			
			for (int i=0; i<n; i++) {
				chargingTime[i] -= exceed * delta[i] / sumDelta;
			}
		}

		double[] arriveTime = new double[n];
		arriveTime[0] = ProblemManager.distance[ProblemManager.serviceStation.getId()][path[skillFactor][0]]
				/ ch.getSpeed();
		for (int i = 0; i < n; i++) {
			Sensor s = ProblemManager.getSensorById(path[skillFactor][i]);

			double eRemain = s.getE0() - arriveTime[i] * s.getP();
			double ub = (Configs.S_EMAX - eRemain) / (ch.getU() - s.getP());

			if (eRemain < Configs.S_EMIN || chargingTime[i] < 0) {
				chargingTime[i] = 0;
			} else if (chargingTime[i] > ub) {
				chargingTime[i] = ub;
			}

			if (i < n - 1) {
				arriveTime[i + 1] = arriveTime[i] + chargingTime[i]
						+ ProblemManager.distance[path[skillFactor][i]][path[skillFactor][i + 1]] / ch.getSpeed();
			}
		}
	}

	public double calculateFitness() {
		this.decoding();
		int dead = 0;
		double totalLifetime = 0;
		double maxLifetime = 0;
		
		int n = path[skillFactor].length;
		double[] arriveTime = new double[n];
		Charger ch = ProblemManager.chargers.get(skillFactor);
		boolean visited[] = new boolean[ProblemManager.maxSensorId + 1];

		// repairing
		this.repairTime();

		// calculate fintess
		for (int i = 0; i < n; i++) {
			Sensor s = ProblemManager.getSensorById(path[skillFactor][i]);
			visited[s.getId()] = true;
			double eRemain = s.getE0() - arriveTime[i] * s.getP();
			double eAfterT = s.getE0() - Configs.T * s.getP() + chargingTime[i] * ch.getU();

			if (eRemain < s.getEmin() || eAfterT < s.getEmin()) {
				dead++;
			}
			
			double lifetime = (s.getE0() + chargingTime[i] * ch.getU() - s.getEmin()) / s.getP();
			totalLifetime += lifetime;
			maxLifetime = Math.max(lifetime, maxLifetime);
		}

		for (Sensor s : ProblemManager.subNet[this.skillFactor]) {
			if (!visited[s.getId()]) {
				double eAfterT = s.getE0() - Configs.T * s.getP();
				if (eAfterT < Configs.S_EMIN) {
					dead++;
				}
				
				double lifetime = s.getLifetime();
				totalLifetime += lifetime;
				maxLifetime = Math.max(lifetime, maxLifetime);
			}
		}

		double netSize = ProblemManager.subNet[this.skillFactor].size();
		double networkSurvivability = (netSize - dead) / netSize;

		return networkSurvivability;
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

	public static int[][] getPath() {
		return path;
	}

	public static void setPath(int[][] path) {
		TIndividual.path = path;
	}

	public double getFitness() {
		return fitness;
	}

	public static void setGreedyChargingTime(double[][] time) {
		TIndividual.greedyChargingTimeRatio = new double[time.length][];

		for (int a = 0; a < time.length; a++) {
			double maxChargingTime = ProblemManager.chargers.get(a).getMaxChargingTime(path[a]);
			TIndividual.greedyChargingTimeRatio[a] = new double[time[a].length];
			for (int i = 0; i < time[a].length; i++) {
				TIndividual.greedyChargingTimeRatio[a][i] = time[a][i] / maxChargingTime;
			}
		}
	}
}
