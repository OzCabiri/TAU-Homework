package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Comparator;


public class ComparatorShipByFPandCY implements Comparator<Spaceship>{

	@Override
	public int compare(Spaceship o1, Spaceship o2) {
		int val = Integer.compare(o1.getFirePower(), o2.getFirePower());
		if(val==0) {
			val = Integer.compare(o1.getCommissionYear(), o2.getCommissionYear());
			if(val==0) {
				o1.getName().compareTo(o2.getName());
			}
		}
		return -val;
	}
	
}