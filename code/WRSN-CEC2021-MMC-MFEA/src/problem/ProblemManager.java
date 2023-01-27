package problem;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

import elements.Charger;
import elements.Node;
import elements.Sensor;

/**
 * @author vancuonglee
 * @Date 25/12/2020
 * @since 1.0
 *
 */
public class ProblemManager {

	/**
	 * unify search space demension
	 */
	public static int USSD;

	/**
	 * clustered network, each charger will take care of one sub network
	 */
	public static ArrayList<Sensor>[] subNet;

	/**
	 * The list of mobile chargers, indexed from 0 to V-1
	 */
	public static ArrayList<Charger> chargers;

	/**
	 * list of n sensors. Sensors must be indexed from 1 to n
	 */
	public static ArrayList<Sensor> sensors;

	/**
	 * the node stands for the service station. The station is indexed 0 and may or
	 * may not co-related with the base station
	 */
	public static Node serviceStation;

	/**
	 * list of nodes, including all sensors and the service station.
	 */
	public static ArrayList<Node> nodes;

	/**
	 * mapping from id to sensor
	 */
	public static HashMap<Integer, Sensor> _map;

	/**
	 * number of deployed sensors on the network
	 */
	public static int initSensors;

	/**
	 * the node distance matrix
	 */
	public static double[][] distance;

	/**
	 * the maximun sensor id
	 */
	public static int maxSensorId;

	public static void init() {
		sensors = new ArrayList<Sensor>();
		nodes = new ArrayList<Node>();
		_map = new HashMap<Integer, Sensor>();
		chargers = new ArrayList<Charger>();
	}

	public static void readInput(String file, double xp) {
		try {
			Scanner in = new Scanner(new File(file));

			int id = 0;

			// read service station info
			ProblemManager.serviceStation = new Node(id, in.nextDouble(), in.nextDouble());

			// read all the sensors
			while (in.hasNext()) {
				double x = in.nextDouble();
				double y = in.nextDouble();
				double p = in.nextDouble();
				double e0 = in.nextDouble();
				Sensor sensor = new Sensor(++id, x, y, e0, p * xp, Configs.S_EMAX, Configs.S_EMIN);
				ProblemManager.sensors.add(sensor);
				_map.put(sensor.getId(), sensor);
			}

			maxSensorId = id;

			initSensors = sensors.size();

			nodes.add(ProblemManager.serviceStation);
			nodes.addAll(sensors);

			distance = new double[ProblemManager.maxSensorId + 1][ProblemManager.maxSensorId + 1];
			for (Node p : nodes) {
				for (Node q : nodes) {
					distance[p.getId()][q.getId()] = p.getDistance(q);
				}
			}

			in.close();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public static Sensor getSensorById(int id) {
		return _map.get(id);
	}

	public Node getNodeById(int id) {
		if (id == 0) {
			return serviceStation;
		} else {
			return getSensorById(id);
		}
	}

	public static double getSensorDensity() {
		return sensors.size() / (Math.PI * Configs.R * Configs.R);
	}

	public static int getTaskNumber() {
		return chargers.size();
	}

	public static double getMinimumLifeTime() {
		double res = 1e9;
		for (Sensor s : sensors) {
			double lifetime = (s.getE0() - s.getEmin()) / s.getP();
			res = res > lifetime ? lifetime : res;
		}
		return res;
	}

	public static double getAverageLifeTime() {
		double res = 0;
		for (Sensor s : sensors) {
			res += (s.getE0() - s.getEmin()) / s.getP();
		}
		res /= sensors.size();
		return res;
	}

	public static double getSumP() {
		double res = 0;
		for (Sensor s : sensors) {
			res += s.getP();
		}
		return res;
	}
}
