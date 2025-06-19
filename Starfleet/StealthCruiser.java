package il.ac.tau.cs.sw1.ex9.starfleet;


import java.util.List;
import java.util.ArrayList;
import java.util.Set;

public class StealthCruiser extends Fighter {
	
	private static int numOfStealthCruisers = 0;
	@SuppressWarnings("serial")
	private static final List<Weapon> defaultWeapon = new ArrayList<>() {{ add(new Weapon("Laser Cannons",10,100)); }};
	
	public StealthCruiser(String name, int commissionYear, float maximalSpeed, Set<CrewMember> crewMembers, List<Weapon> weapons) {
		super(name,commissionYear,maximalSpeed,crewMembers,weapons);
		numOfStealthCruisers++;
	}

	public StealthCruiser(String name, int commissionYear, float maximalSpeed, Set<CrewMember> crewMembers){
		this(name,commissionYear,maximalSpeed,crewMembers,defaultWeapon);
	}
	
	@Override
	public int getAnnualMaintenanceCost() {
		return super.getAnnualMaintenanceCost() + 50*numOfStealthCruisers;
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(this.getClass().getSimpleName());
		sb.append("\n\tName="); sb.append(getName());
		sb.append("\n\tCommissionYear="); sb.append(getCommissionYear());
		sb.append("\n\tMaximalSpeed="); sb.append(getMaximalSpeed());
		sb.append("\n\tFirePower="); sb.append(getFirePower());
		sb.append("\n\tCrewMembers="); sb.append(getCrewMembers().size());
		sb.append("\n\tAnnualMaintenanceCost="); sb.append(getAnnualMaintenanceCost());
		sb.append("\n\tWeaponArray="); sb.append(getWeapon().toString());
		return sb.toString();
	}
	
}
