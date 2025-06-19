package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public class Fighter extends myAbstractBattleship {
	
	public Fighter(String name, int commissionYear, float maximalSpeed, Set<? extends CrewMember> crewMembers, List<Weapon> weapons){
		super(name,commissionYear,maximalSpeed,crewMembers,weapons);
		this.setBaseAnnualMaintenanceCost(2500);
		this.setAnnualMaintenanceCost(calcAnnualMaintenanceCost
				(this.getBaseAnnualCost(),this.calcWeaponsAnnualMaintenanceCost(),this.getMaximalSpeed()));
	}

	private static int calcAnnualMaintenanceCost(int base, int weaponscost, float maxspeed) {
		return (int) Math.floor(base + weaponscost + 1000*maxspeed);
	}
	
}
