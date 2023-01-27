package problem;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;

import algo.path.PIndividual;
import elements.Charger;
import elements.Sensor;

public class Solution {

	private int[][] path;
	private double[][] time;

	public Solution(int[][] path, double[][] time) {
		this.path = path;
		this.time = time;
	}

	public Solution(PIndividual[] indivs) {
		int V = ProblemManager.chargers.size();
		path = new int[V][];
		time = new double[V][];

		for (int a = 0; a < V; a++) {
			ArrayList<Integer> tour = indivs[a].getPath();
			path[a] = new int[tour.size()];
			time[a] = new double[tour.size()];

			for (int i = 0; i < tour.size(); i++) {
				path[a][i] = tour.get(i);
				time[a][i] = indivs[a].getChargingTime(i);
			}
		}
	}

	public HashMap<String, Double> extractSolution() {
		int V = path.length;
		double totalDead = 0;
		double sumEAfterT = 0;
		double minLifetime = Double.MAX_VALUE;
		double totalLifetime = 0;

		for (int a = 0; a < V; a++) {
			Charger ch = ProblemManager.chargers.get(a);
			int leng = path[a].length;
			double arriveTime[] = new double[leng];
			boolean[] visited = new boolean[ProblemManager.maxSensorId + 1];
			int dead = 0;
			double sumE = 0;
			arriveTime[0] = ProblemManager.distance[ProblemManager.serviceStation.getId()][path[a][0]] / Configs.speed;
			for (int i = 0; i < leng; i++) {
				visited[path[a][i]] = true;
				Sensor s = ProblemManager.getSensorById(path[a][i]);
				double eRemain = s.getE0() - arriveTime[i] * s.getP();
				double eAfterT = s.getE0() - Configs.T * s.getP() + time[a][i] * ch.getU();

				if (eRemain < s.getEmin() || eAfterT < s.getEmin()) {
					dead++;
				} else {
					sumE += eAfterT;
					double t = (eAfterT - s.getEmin()) / s.getP();
					minLifetime = t < minLifetime ? t : minLifetime;
				}
				
				double lifetime = (s.getE0() + time[a][i] * ch.getU() - s.getEmin()) / s.getP();
				totalLifetime += lifetime;

				if (i < leng - 1) {
					arriveTime[i + 1] = arriveTime[i]
							+ ProblemManager.distance[path[a][i]][path[a][i + 1]] / ch.getSpeed() + time[a][i];
				}
			}

			for (Sensor s : ProblemManager.subNet[a]) {
				if (!visited[s.getId()]) {
					double eAfterT = s.getE0() - Configs.T * s.getP();
					if (eAfterT < Configs.S_EMIN) {
						dead++;
					} else {
						sumE += eAfterT;
						double t = eAfterT / s.getP();
						minLifetime = t < minLifetime ? t : minLifetime;
					}
					
					totalLifetime += s.getLifetime();
				}
			}

			totalDead += dead;
			sumEAfterT += sumE;
		}

		double networkSurvivability = 100 * (ProblemManager.initSensors - totalDead)
				/ (1.0 * ProblemManager.initSensors);
		double avgE = sumEAfterT / (1.0 * ProblemManager.initSensors);
		double avgDeadDuration = totalLifetime / (1.0 * ProblemManager.initSensors);
		double emove = 0;
		for (int a = 0; a < V; a++) {
			emove += ProblemManager.chargers.get(a).getEmove(path[a]);
		}

		HashMap<String, Double> result = new HashMap<String, Double>();
		result.put("network_survivability", networkSurvivability);
		result.put("network_lifetime", minLifetime + Configs.T);
		result.put("average_energy", avgE);
		result.put("moving_cost", emove);
		result.put("average_lifetime", avgDeadDuration);

		return result;
	}

	public void log() {
		int V = path.length;
		System.out.println("Number of charging vehicles: " + V);
		System.out.println("Survey time: " + Configs.T);

		double totalDead = 0;
		double totalLifetime = 0;

		for (int a = 0; a < V; a++) {
			Charger ch = ProblemManager.chargers.get(a);
			int leng = path[a].length;
			double arriveTime[] = new double[leng];
			boolean[] visited = new boolean[ProblemManager.maxSensorId + 1];
			int dead = 0;

			System.out.println("Vehicle " + a);
			System.out.print("Charging tour: ");
			for (int i = 0; i < leng; i++) {
				System.out.print(path[a][i] + " ");
				visited[path[a][i]] = true;
			}
			System.out.println();

			double sum = 0;
			System.out.print("Charging time: ");
			for (int i = 0; i < leng; i++) {
				System.out.print(time[a][i] + " ");
				sum += time[a][i];
			}
			System.out.println();

			System.out.println("Traveling energy: " + ch.getEmove(path[a]));
			System.out.println("Charging energy: " + sum * ch.getU());
			System.out.println("Total energy used: " + (ch.getEmove(path[a]) + sum * ch.getU()));
			System.out.println("Charging round duration: " + (ch.getEmove(path[a]) / ch.getPm() + sum));

			DecimalFormat formatter = new DecimalFormat("#0.00");
			System.out
					.println("ID | P | E_0 | time_arrive | E_remain | charging_time | E_after_charge | E_after_cycle");
			arriveTime[0] = ProblemManager.distance[ProblemManager.serviceStation.getId()][path[a][0]] / Configs.speed;
			for (int i = 0; i < leng; i++) {
				Sensor s = ProblemManager.getSensorById(path[a][i]);
				double eRemain = s.getE0() - arriveTime[i] * s.getP();
				double eAfterCharged = eRemain + time[a][i] * (ch.getU() - s.getP());
				double eAfterT = s.getE0() - Configs.T * s.getP() + time[a][i] * ch.getU();

				String sensorDetails = s.getId() + " | " + formatter.format(s.getP()) + " | "
						+ formatter.format(s.getE0()) + " | " + formatter.format(arriveTime[i]) + " | "
						+ formatter.format(eRemain) + " | " + formatter.format(time[a][i]) + " | "
						+ formatter.format(eAfterCharged) + " | " + formatter.format(eAfterT);

				if (eRemain < s.getEmin() || eAfterT < s.getEmin()) {
					System.err.println(sensorDetails);
					dead++;
				} else {
					System.out.println(sensorDetails);
				}

				double lifetime = (s.getE0() + time[a][i] * ch.getU() - s.getEmin()) / s.getP();
				totalLifetime += lifetime;

				if (i < leng - 1) {
					arriveTime[i + 1] = arriveTime[i]
							+ ProblemManager.distance[path[a][i]][path[a][i + 1]] / ch.getSpeed() + time[a][i];
				}
			}

			for (Sensor s : ProblemManager.subNet[a]) {
				if (!visited[s.getId()]) {
					double eAfterT = s.getE0() - Configs.T * s.getP();
					String sensorDetails = s.getId() + " | " + formatter.format(s.getP()) + " | "
							+ formatter.format(s.getE0()) + " | " + formatter.format(eAfterT);

					if (eAfterT < Configs.S_EMIN) {
						System.err.println(sensorDetails);
						dead++;
					} else {
						System.out.println(sensorDetails);
					}

					totalLifetime += s.getLifetime();
				}
			}

			totalDead += dead;
		}

		double networkSurvivability = 100 * (ProblemManager.initSensors - totalDead)
				/ (1.0 * ProblemManager.initSensors);

		double emove = 0;
		for (int a = 0; a < V; a++) {
			emove += ProblemManager.chargers.get(a).getEmove(path[a]);
		}

		System.out.println("Network survivability: " + networkSurvivability + "%");
		System.out.println("Average dead duration: " + (totalLifetime / (1.0 * ProblemManager.initSensors)));
		System.out.println("Traveling energy: " + emove);
	}

	public int[][] getPath() {
		return path;
	}

	public void setPath(int[][] path) {
		this.path = path;
	}

	public double[][] getTime() {
		return time;
	}

	public void setTime(double[][] time) {
		this.time = time;
	}
}
