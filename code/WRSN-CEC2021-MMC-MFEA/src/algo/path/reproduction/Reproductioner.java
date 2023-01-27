package algo.path.reproduction;

import java.util.List;

import algo.path.PIndividual;
import algo.path.PPopulation;

public interface Reproductioner {
	
	public List<PIndividual> reproduction(PPopulation pop);

}
