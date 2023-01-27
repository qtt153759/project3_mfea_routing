package elements;

import java.util.ArrayList;
import java.util.List;

import problem.Configs;
import problem.ProblemManager;

public class Charger {
	private double E0;
	private double speed;
	private double Pm;
	private double U;

	public Charger(double e0, double speed, double pm, double u) {
		this.setE0(e0);
		this.setPm(pm);
		this.setSpeed(speed);
		this.setU(u);
	}

	public double getMovingTime(List<Integer> path) {
		double res = 0;
		res += ProblemManager.distance[ProblemManager.serviceStation.getId()][path.get(0)];
		res += ProblemManager.distance[path.get(path.size() - 1)][ProblemManager.serviceStation.getId()];
		for (int i = 1; i < path.size(); i++) {
			res += ProblemManager.distance[path.get(i - 1)][path.get(i)];
		}
		return res / this.speed;
	}

	public double getMaxChargingTime(double travelingDistance) {
		return (this.getE0() - travelingDistance * this.getPm() / getSpeed()) / this.getU();
	}

	public double getMaxChargingTime(ArrayList<Integer> path) {
		double movingTime = this.getMovingTime(path);
		if (movingTime > Configs.T) {
			System.err.println("Travling time exceed charging cycle! " +  movingTime);
			System.exit(0);
		}
		double ct = (this.getE0() - movingTime * this.getPm()) / this.getU();
		return Math.min(ct, Configs.T - movingTime);

	}

	public double getMaxChargingTime(int[] path) {
		double movingTime = this.getMovingTime(path);
		if (movingTime > Configs.T) {
			System.err.println("Travling time exceed charging cycle!");
			System.exit(0);
		}
		double ct = (this.getE0() - movingTime * this.getPm()) / this.getU();
		return Math.min(ct, Configs.T - movingTime);

	}

	public double getMovingTime(int[] path) {
		double res = 0;
		int n = path.length;
		res += ProblemManager.distance[ProblemManager.serviceStation.getId()][path[0]];
		res += ProblemManager.distance[path[n - 1]][ProblemManager.serviceStation.getId()];
		for (int i = 1; i < n; i++) {
			res += ProblemManager.distance[path[i - 1]][path[i]];
		}
		return res / this.speed;
	}

	public double getEmove(int[] path) {
		return this.getMovingTime(path) * this.Pm;
	}

	public double getE0() {
		return E0;
	}

	public void setE0(double e0) {
		E0 = e0;
	}

	public double getSpeed() {
		return speed;
	}

	public void setSpeed(double speed) {
		this.speed = speed;
	}

	public double getPm() {
		return Pm;
	}

	public void setPm(double pm) {
		Pm = pm;
	}

	public double getU() {
		return U;
	}

	public void setU(double u) {
		U = u;
	}

}
