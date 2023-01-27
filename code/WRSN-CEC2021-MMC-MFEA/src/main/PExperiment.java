package main;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Random;

import algo.ProblemSolver;
import algo.path.PSolver;
import algo.path.reproduction.MFEA_Reproductioner;
import elements.Charger;
import problem.Configs;
import problem.ProblemManager;
import problem.Solution;

public class PExperiment {

	public static void main(String[] args) throws FileNotFoundException {
		String inputFolder = args[0]; //"data/input/cec_2021_mmc/circle";
		String outputFolder = args[1]; //"data/output/scen1";
		int file = 10;
		int rep = 30;
		
//		String inputFolder = "data/input/cec_2021_mmc/circle/500/500";
//		String outputFolder = "data/output/scen1";

		double xp[] = { 0.7, 0.8, 0.9, 1.0, 1.1, 1.2};
		Configs.U = 5;
		int numberOfMC = 5;
		Configs.speed = 5;
		Configs.E_MC = 108000;

		double netSurvi[][][] = new double[xp.length][file + 1][rep];
		double lifetime[][][] = new double[xp.length][file + 1][rep];
		double movingCost[][][] = new double[xp.length][file + 1][rep];
		double avgLifetime[][][] = new double[xp.length][file + 1][rep];

		PSolver.reproductioner = new MFEA_Reproductioner();
		for (int scale = 0; scale < xp.length; scale++) {
			for (int k = 1; k <= file; k++) {
				for (int seed = 0; seed < rep; seed++) {
					Configs.rand = new Random(seed);
					ProblemManager.init();
					for (int i = 0; i < numberOfMC; i++) {
						ProblemManager.chargers.add(new Charger(Configs.E_MC, Configs.speed, Configs.Pm, Configs.U));
					}
					ProblemManager.readInput(
							inputFolder + "_" + k + ".txt", xp[scale]);

					Solution solution = ProblemSolver.solve();

//					solution.log();
					HashMap<String, Double> result = solution.extractSolution();
					netSurvi[scale][k][seed] = result.get("network_survivability");
					lifetime[scale][k][seed] = result.get("network_lifetime");
					movingCost[scale][k][seed] = result.get("moving_cost");
					avgLifetime[scale][k][seed] = result.get("average_lifetime");

					System.out.println("Done: file" + "_" + k + ", u = " + xp[scale] + ", seed = " + seed);
				}
			}
		}

		PrintWriter out = new PrintWriter(new File(outputFolder + "/survivability.txt"));
		for (int i = 0; i < xp.length; i++) {
			for (int j = 1; j <= file; j++) {
				out.print(xp[i] + "\t");
				for (int k = 0; k < rep; k++) {
					out.print(netSurvi[i][j][k] + "\t");
				}
				out.println();
			}
		}
		out.close();

		out = new PrintWriter(new File(outputFolder + "/lifetime.txt"));
		for (int i = 0; i < xp.length; i++) {
			for (int j = 1; j <= file; j++) {
				out.print(xp[i] + "\t");
				for (int k = 0; k < rep; k++) {
					out.print(lifetime[i][j][k] + "\t");
				}
				out.println();
			}
		}
		out.close();

		out = new PrintWriter(new File(outputFolder + "/emove.txt"));
		for (int i = 0; i < xp.length; i++) {
			for (int j = 1; j <= file; j++) {
				out.print(xp[i] + "\t");
				for (int k = 0; k < rep; k++) {
					out.print(movingCost[i][j][k] + "\t");
				}
				out.println();
			}
		}
		out.close();
		
		out = new PrintWriter(new File(outputFolder + "/avg_dead_duration.txt"));
		for (int i = 0; i < xp.length; i++) {
			for (int j = 1; j <= file; j++) {
				out.print(xp[i] + "_" + j + "\t");
				for (int k = 0; k < rep; k++) {
					out.print(avgLifetime[i][j][k] + "\t");
				}
				out.println();
			}
		}
		out.close();
	}
}
