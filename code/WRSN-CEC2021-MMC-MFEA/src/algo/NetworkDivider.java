package algo;

import java.util.ArrayList;
import java.util.List;

import elements.Sensor;
import problem.Configs;
import problem.ProblemManager;

public class NetworkDivider {

	@SuppressWarnings("unchecked")
	public static ArrayList<Sensor>[] cluster(int sectorsNo, List<Sensor> sensors) {
		double phi = 2.0 * Math.PI / (1.0 * sectorsNo);
		ArrayList<Sensor>[] result = new ArrayList[sectorsNo];

		for (int k = 0; k < sectorsNo; k++) {
			result[k] = new ArrayList<Sensor>();
			for (Sensor s : sensors) {
				double firstX = 1;
				double firstY = 0;
				double secondX = s.getX()-ProblemManager.serviceStation.getX();
				double secondY = s.getY()-ProblemManager.serviceStation.getY();
				
				double dotProduct = firstX * secondX +  firstY * secondY;
				double lengthProduct = Math.sqrt(Math.pow(firstX,2)+Math.pow(firstY,2)) * Math.sqrt(Math.pow(secondX,2)+Math.pow(secondY,2));
				
				double cosphi = dotProduct / lengthProduct;
				double angle = Math.acos(cosphi);

				if (secondY < 0) {
					angle = 2*Math.PI - angle;
				}

				if (angle > k * phi && angle < (k + 1) * phi) {
					result[k].add(s);
				}
			}
		}

		return result;
	}
}
