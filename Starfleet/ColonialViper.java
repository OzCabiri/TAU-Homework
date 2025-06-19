package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public class ColonialViper extends myAbstractBattleship  {

	public ColonialViper(String name, int commissionYear, float maximalSpeed, Set<CrewWoman> crewMembers,
			List<Weapon> weapons) {
		super(name,commissionYear,maximalSpeed,crewMembers,weapons);
		this.setBaseAnnualMaintenanceCost(4000);
		this.setAnnualMaintenanceCost(calcAnnualMaintenanceCost
				(this.getBaseAnnualCost(),this.calcWeaponsAnnualMaintenanceCost(),
					this.getCrewMembers().size(), this.getMaximalSpeed()));
	}
	
	private static int calcAnnualMaintenanceCost(int base, int weaponscost,int ammountCrewMembers, float maxspeed) {
		return (int) Math.floor(base + weaponscost + 500*ammountCrewMembers + 500*maxspeed);
	}

}
