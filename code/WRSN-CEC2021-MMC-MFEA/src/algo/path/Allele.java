package algo.path;

public class Allele implements Comparable {

	private double value;
	private int sensorId;

	public Allele(double value, int sensorId) {
		this.setSensorId(sensorId);
		this.setValue(value);
	}

	public double getValue() {
		return value;
	}

	public void setValue(double value) {
		this.value = value;
	}

	public int getSensorId() {
		return sensorId;
	}

	public void setSensorId(int sensorId) {
		this.sensorId = sensorId;
	}

	@Override
	public int compareTo(Object o) {
		//similar to __gt__ python
		// TODO Auto-generated method stub
		Allele a = (Allele) o;
		return Double.valueOf(this.value).compareTo(a.getValue());
	}

}
