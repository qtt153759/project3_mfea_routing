package problem;

import java.util.Random;

/**
 * The class {@code Configs} contains all the parameters of the application
 * 
 * @author vancuonglee
 * @Date: 25/12/2020
 * @since 1.0
 */
public class Configs {

	public static Random rand;
	public static double T;
	public static double U;
	public static double speed;
	public static double E_MC;

	public static final double S_EMAX = 10800;
	public static final double S_EMIN = 540;
	public static final double R = 1000;

	public static double Pm = 1;
	public static final double DEFAULT_U = 5;
	public static final double DEFAULT_SPEED = 5;
	public static final double DEFAULT_EMC = 108000;
	public static final int DEFAULT_MCS = 5;

	public static final int P_POP_SIZE_PER_TASK = 100;
	public static int P_POP_SIZE;
	public static final int P_GENERATIONS = 250;
	public static double RMP = 0.3;
	public static final double NC = 15;
	public static final double NM = 15;
}
