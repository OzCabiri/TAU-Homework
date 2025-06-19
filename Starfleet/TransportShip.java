package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Set;

public class TransportShip extends myAbstractSpaceship{

	private int cargocapacity;
	private int passengercapacity;
	
	public TransportShip(String name, int commissionYear, float maximalSpeed, Set<CrewMember> crewMembers, int cargoCapacity, int passengerCapacity){
		super(name, commissionYear, maximalSpeed, crewMembers);
		this.cargocapacity = cargoCapacity;
		this.passengercapacity = passengerCapacity;
		this.setBaseAnnualMaintenanceCost(3000);
		this.setAnnualMaintenanceCost(calcAnnualMaintenanceCost
				(this.getBaseAnnualCost(),cargocapacity,passengercapacity));
	}
	
	public int getCargoCapacity() {
		return cargocapacity;
	}
	
	public int getPassengerCapacity() {
		return passengercapacity;
	}
	
	private static int calcAnnualMaintenanceCost(int base, int cargocap, int passcap) {
		return base+ 5*cargocap + 3*passcap;
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(super.toString());
		sb.append("\n\tCargoCapacity="); sb.append(cargocapacity);
		sb.append("\n\tPassengerCapacity="); sb.append(passengercapacity);
		return sb.toString();
	}

}
