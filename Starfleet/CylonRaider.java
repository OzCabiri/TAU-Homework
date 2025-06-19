package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public class CylonRaider extends myAbstractBattleship {

	public CylonRaider(String name, int commissionYear, float maximalSpeed, Set<Cylon> crewMembers,
			List<Weapon> weapons) {
		super(name,commissionYear,maximalSpeed,crewMembers,weapons);
		this.setBaseAnnualMaintenanceCost(3500);
		this.setAnnualMaintenanceCost(calcAnnualMaintenanceCost
				(this.getBaseAnnualCost(),this.calcWeaponsAnnualMaintenanceCost(),
					this.getCrewMembers().size(), this.getMaximalSpeed()));
	}
	
	private static int calcAnnualMaintenanceCost(int base, int weaponscost,int ammountCrewMembers, float maxspeed) {
		return (int) Math.floor(base + weaponscost + 500*ammountCrewMembers + 1200*maxspeed);
	}

}
