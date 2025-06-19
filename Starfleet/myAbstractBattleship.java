package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.List;
import java.util.Set;

public abstract class myAbstractBattleship extends myAbstractSpaceship {
	
	private List<Weapon> weapons;
	
	public myAbstractBattleship(String _name, int _commissionYear, float _maxSpeed, Set<? extends CrewMember> _crewMembers, List<Weapon> _weapons){
		super(_name,_commissionYear,_maxSpeed,_crewMembers);
		this.weapons = _weapons;
		this.setFirePower(calcFirePower(weapons));
	}
	
	public List<Weapon> getWeapon(){
		return weapons;
	}
	
	protected int calcWeaponsAnnualMaintenanceCost() {
		int cost = 0;
		for(Weapon wp : weapons)
			cost += wp.getAnnualMaintenanceCost();
		return cost;
	}
	
	private static int calcFirePower(List<Weapon> weapons) {
		int firepower=10;
		for(Weapon wp : weapons) {
			firepower += wp.getFirePower();
		}
		return firepower;
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(super.toString());
		sb.append("\n\tWeaponArray="); sb.append(weapons.toString());
		return sb.toString();
	}
}
