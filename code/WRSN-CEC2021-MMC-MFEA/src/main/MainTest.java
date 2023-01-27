package main;

import java.util.Random;

import algo.ProblemSolver;
import algo.path.PSolver;
import algo.path.reproduction.GA_Reproductioner;
import algo.path.reproduction.MFEA_Reproductioner;
import elements.Charger;
import problem.Configs;
import problem.ProblemManager;
import problem.Solution;

public class MainTest {

	public static void main(String[] args) {
		String input = "C:\\Users\\Duong\\OneDrive - Hanoi University of Science and Technology\\Documents\\20221\\EvolutionAlgorithm\\code\\WRSN-CEC2021-MMC-MFEA\\data\\ga100.txt";
		ProblemManager.init();
		int k = 5;
		Configs.rand = new Random(0);
		Configs.U = 5;
		Configs.speed = 5;
		Configs.E_MC = 108000;

		ProblemManager.readInput(input, 1.0);
		for (int i = 0; i < k; i++) {
			ProblemManager.chargers.add(new Charger(Configs.E_MC, Configs.speed, Configs.Pm, Configs.U));
		}

		PSolver.reproductioner = new MFEA_Reproductioner();
		Solution solution = ProblemSolver.solve();
		solution.log();
	}
}
