package elements;

public class Sensor extends Node {

	private double Emax;
	private double Emin;
	private double E0;
	private double p;

	public Sensor(int id, double x, double y, double e0, double pi, double emax, double emin) {
		super(id, x, y);
		this.setE0(e0);
		this.setP(pi);
		this.setEmax(emax);
		this.setEmin(emin);
	}

	public Sensor() {
		// TODO Auto-generated constructor stub
		super();
	}

	public double getEmax() {
		return Emax;
	}

	public void setEmax(double emax) {
		Emax = emax;
	}

	public double getEmin() {
		return Emin;
	}

	public void setEmin(double emin) {
		Emin = emin;
	}

	public double getE0() {
		return E0;
	}

	public void setE0(double e0) {
		E0 = e0;
	}

	public double getP() {
		return p;
	}

	public void setP(double p) {
		this.p = p;
	}

	public double getW() {
		return this.p / this.E0;
	}

	public double getLifetime() {
		return (this.E0 - this.Emin) / this.p;
	}
}
