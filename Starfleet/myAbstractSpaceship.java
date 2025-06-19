package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Objects;
import java.util.Set;

public abstract class myAbstractSpaceship implements Spaceship {

	private String name;
	private int commissionyear;
	private float maxspeed;
	private int firepower = 10;
	private Set<? extends CrewMember> crewmembers;
	private int baseannualcost;
	private int annualmaintenancecost;
	
	public myAbstractSpaceship(String _name, int _commissionYear, float _maxSpeed, Set<? extends CrewMember> _crewMembers){
		this.name=_name;
		this.commissionyear=_commissionYear;
		this.maxspeed=_maxSpeed;
		this.crewmembers=_crewMembers;
	}
	
	public String getName() {
		return name;
	}
	
	public int getCommissionYear() {
		return commissionyear;
	}
	
	public float getMaximalSpeed() {
		return maxspeed;
	}
	
	public int getFirePower() {
		return firepower;
	}
	
	public Set<? extends CrewMember> getCrewMembers(){
		return crewmembers;
	}
	
	public int getAnnualMaintenanceCost() {
		return annualmaintenancecost;
	}

	@Override
	public int hashCode() {
		return Objects.hash(name);
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		myAbstractSpaceship other = (myAbstractSpaceship) obj;
		return Objects.equals(name, other.name);
	}
	
	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(this.getClass().getSimpleName());
		sb.append("\n\tName="); sb.append(name);
		sb.append("\n\tCommissionYear="); sb.append(commissionyear);
		sb.append("\n\tMaximalSpeed="); sb.append(maxspeed);
		sb.append("\n\tFirePower="); sb.append(firepower);
		sb.append("\n\tCrewMembers="); sb.append(crewmembers.size());
		sb.append("\n\tAnnualMaintenanceCost="); sb.append(annualmaintenancecost);
		return sb.toString();
	}

	protected int getBaseAnnualCost() {
		return baseannualcost;
	}
	protected void setBaseAnnualMaintenanceCost(int _basecost) {
		this.baseannualcost = _basecost;
	}
	protected void setAnnualMaintenanceCost(int cost) {
		this.annualmaintenancecost = cost;
	}
	protected void setFirePower(int _firePower) {
		this.firepower = _firePower;
	}

}
