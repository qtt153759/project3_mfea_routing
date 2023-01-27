package main;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

import elements.Charger;
import elements.Sensor;
import problem.Configs;
import problem.ProblemManager;

public class MainNoCharge {

	public static void main(String[] args) throws FileNotFoundException {
		String inputFolder = "D:\\Desktop\\wrsn-mmc-cec-2021\\experiments\\test_instances\\circle";
		String outputFolder = "data\\output\\no_charge";
		String netScale[] = {"50", "100", "250", "500", "750", "1000"};

		int file = 10;
		int numberOfMC = 5;
		double xp = 1.0;

		double netSurvi[][] = new double[netScale.length][file + 1];
		double lifetime[][] = new double[netScale.length][file + 1];
		double avgLifetime[][] = new double[netScale.length][file + 1];
		double T[][] = new double[netScale.length][file + 1];

		for (int scale = 0; scale < netScale.length; scale++) {
			for (int k = 1; k <= file; k++) {
				ProblemManager.init();

				for (int i = 0; i < numberOfMC; i++) {
					ProblemManager.chargers.add(new Charger(Configs.E_MC, Configs.speed, Configs.Pm, Configs.U));
				}
				ProblemManager.readInput(
						inputFolder + "\\" + netScale[scale] + "\\" + netScale[scale] + "_" + k + ".txt", xp);

				int n = ProblemManager.initSensors / 5;
				double d = Math.sqrt(2.0 / ProblemManager.getSensorDensity());
				Configs.T = (Configs.DEFAULT_EMC - Configs.Pm * d *  n / Configs.DEFAULT_SPEED) / Configs.DEFAULT_U
						+ n * d / Configs.DEFAULT_SPEED;

				double life = Double.MAX_VALUE;
				int dead = 0;
				for (Sensor s : ProblemManager.sensors) {
					double t = s.getLifetime();
					life = life > t ? t : life;
					if (t < Configs.T) {
						dead++;
					}
					
					avgLifetime[scale][k] += t;
				}
				
				netSurvi[scale][k] = (ProblemManager.initSensors - dead) / (1.0 * ProblemManager.initSensors) * 100;
				lifetime[scale][k] = life;
				T[scale][k] = Configs.T;
				avgLifetime[scale][k] /= (1.0 * ProblemManager.initSensors);
			}
		}

		PrintWriter out = new PrintWriter(new File(outputFolder + "\\survivability.txt"));
		for (int i = 0; i < netScale.length; i++) {
			for (int j = 1; j <= file; j++) {
				out.println(netScale[i] + "_" + j + "\t" + T[i][j] + "\t" + netSurvi[i][j]);
			}
		}
		out.close();

		out = new PrintWriter(new File(outputFolder + "\\lifetime.txt"));
		for (int i = 0; i < netScale.length; i++) {
			for (int j = 1; j <= file; j++) {
				out.println(netScale[i] + "_" + j + "\t" + T[i][j] + "\t" + lifetime[i][j]);
			}
		}
		out.close();
		
		out = new PrintWriter(new File(outputFolder + "\\avg_dead_duration.txt"));
		for (int i = 0; i < netScale.length; i++) {
			for (int j = 1; j <= file; j++) {
				out.println(netScale[i] + "_" + j + "\t" + T[i][j] + "\t" + avgLifetime[i][j]);
			}
		}
		out.close();
	}
}
