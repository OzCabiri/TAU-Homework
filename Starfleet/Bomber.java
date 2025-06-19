package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public class Bomber extends myAbstractBattleship{

	private int numoftechs;
	
	public Bomber(String name, int commissionYear, float maximalSpeed, Set<CrewMember> crewMembers, List<Weapon> weapons, int numberOfTechnicians){
		super(name, commissionYear, maximalSpeed, crewMembers, weapons);
		this.numoftechs = numberOfTechnicians;
		this.setBaseAnnualMaintenanceCost(5000);
		this.setAnnualMaintenanceCost(calcAnnualMaintenanceCost
				(this.getBaseAnnualCost(),this.calcWeaponsAnnualMaintenanceCost(),numoftechs));
	}
	
	public int getNumberOfTechnicians() {
		return numoftechs;
	}
	
	private static int calcAnnualMaintenanceCost(int base, int weaponscost, int numOfTechs) {
		return Math.round(base + (weaponscost*numOfTechs/10));
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(super.toString());
		sb.append("\n\tNumberOfTechnicians="); sb.append(numoftechs);
		return sb.toString();
	}

}
