package algo;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import elements.Sensor;
import problem.Configs;
import problem.ProblemManager;

class Centroid {
	private final double DIFF = 1E-3;

	double x;
	double y;

	public Centroid() {

	}

	public Centroid(double x, double y) {
		this.x = x;
		this.y = y;
	}

	public double getDistance(double x, double y) {
		return Math.sqrt((this.x - x) * (this.x - x) + (this.y - y) * (this.y - y));
	}

	public boolean isDifference(Centroid c) {
		return this.getDistance(c.x, c.y) > DIFF;
	}
}

public class NetworkClustering {

	private static final double MIN_X = 0;
	private static final double MAX_X = 1000;
	private static final double MIN_Y = 0;
	private static final double MAX_Y = 1000;

	private static final double MAX_ITERATIONS = 1000;

	private static ArrayList<Centroid> generateRandomCentroids(int k) {
		ArrayList<Centroid> centroids = new ArrayList<Centroid>();
		while (centroids.size() < k) {
			Centroid c = new Centroid();
			c.x = Configs.rand.nextDouble() * (MAX_X - MIN_X) + MIN_X;
			c.y = Configs.rand.nextDouble() * (MAX_Y - MIN_Y) + MIN_Y;
			centroids.add(c);
		}
		return centroids;
	}

	private static Centroid getNearestCentroid(Sensor p, ArrayList<Centroid> centroids) {
		double minDis = centroids.get(0).getDistance(p.getX(), p.getY());
		int index = 0;
		for (int i = 1; i < centroids.size(); i++) {
			Centroid c = centroids.get(i);
			double dis = c.getDistance(p.getX(), p.getY());
			if (dis < minDis) {
				minDis = dis;
				index = i;
			}
		}

		return centroids.get(index);
	}

	private static void assignToCluster(Sensor p, Centroid centroid, Map<Centroid, List<Sensor>> clusters) {
		if (clusters.get(centroid) == null) {
			clusters.put(centroid, new ArrayList<Sensor>());
		}
		clusters.get(centroid).add(p);
	}

	private static Centroid getCentroid(List<Sensor> points) {
		double xmean = 0, ymean = 0;
		for (Sensor s : points) {
			xmean += s.getX();
			ymean += s.getY();
		}
		return new Centroid(xmean / points.size(), ymean / points.size());
	}

	private static ArrayList<Centroid> relocateCentroids(List<Centroid> centroids,
			Map<Centroid, List<Sensor>> clusters) {
		ArrayList<Centroid> newCentroids = new ArrayList<Centroid>();
		for (Centroid c : centroids) {
			newCentroids.add(getCentroid(clusters.get(c)));
		}
		return newCentroids;
	}

	private static boolean checkTermination(ArrayList<Centroid> oldCentroids, ArrayList<Centroid> newCentroids) {
		for (int i = 0; i < oldCentroids.size(); i++) {
			Centroid old = oldCentroids.get(i);
			Centroid newCen = newCentroids.get(i);
			if (old.isDifference(newCen)) {
				return false;
			}
		}
		return true;
	}

	@SuppressWarnings({ "unchecked", "rawtypes" })
	public static ArrayList<Sensor>[] cluster(int k, List<Sensor> sensors) {
		Map<Centroid, List<Sensor>> clusters;

		ArrayList<Sensor> points = new ArrayList<Sensor>();
		points.addAll(ProblemManager.sensors);

		ArrayList<Centroid> centroids = generateRandomCentroids(k);
		ArrayList<Centroid> oldCentroids = new ArrayList<Centroid>();

		int iter = 0;
		while (true) {
			clusters = new HashMap<>();
			for (Sensor p : points) {
				Centroid centroid = getNearestCentroid(p, centroids);
				assignToCluster(p, centroid, clusters);
			}

			oldCentroids.clear();
			oldCentroids.addAll(centroids);

			centroids = relocateCentroids(centroids, clusters);

			if (++iter > MAX_ITERATIONS || checkTermination(oldCentroids, centroids)) {
				break;
			}
			System.out.println("ok");
		}

		ArrayList[] result = new ArrayList[k];
		for (int i = 0; i < k; i++) {
			result[i] = new ArrayList<Sensor>();
			result[i].addAll(clusters.get(oldCentroids.get(i)));
		}

		return result;
	}
}
