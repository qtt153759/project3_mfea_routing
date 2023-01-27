package algo;

import java.util.ArrayList;

import algo.path.PSolver;
import elements.Sensor;
import problem.Configs;
import problem.ProblemManager;
import problem.Solution;

public class ProblemSolver {

	public static Solution solve() {
		ArrayList<Sensor>[] clusters = NetworkDivider.cluster(ProblemManager.getTaskNumber(), ProblemManager.sensors);
		int ussd = 0;
		for (int i = 0; i < clusters.length; i++) {
			ussd = ussd < clusters[i].size() ? clusters[i].size() : ussd;
		}

		ProblemManager.subNet = clusters;
		ProblemManager.USSD = ussd;

		int n = ProblemManager.initSensors / Configs.DEFAULT_MCS;
		double d = Math.sqrt(2.0 / ProblemManager.getSensorDensity());
		Configs.T = (Configs.DEFAULT_EMC - Configs.Pm * d *  n / Configs.DEFAULT_SPEED) / Configs.DEFAULT_U
				+ n * d / Configs.DEFAULT_SPEED;
		Configs.P_POP_SIZE = ProblemManager.getTaskNumber() * Configs.P_POP_SIZE_PER_TASK;
//		System.out.println(Configs.T);

		Solution solution = PSolver.solve();
//		
//		TIndividual.setPath(solution.getPath());
//		TIndividual.setGreedyChargingTime(solution.getTime());
//		solution.setTime(TSolver.solve());
//		
		return solution;
	}

}
