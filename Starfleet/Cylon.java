package il.ac.tau.cs.sw1.ex9.starfleet;

public class Cylon extends myAbstractCrewMember {

	private int modelnumber;
	
	public Cylon(String name, int age, int yearsInService, int modelNumber) {
		super(age,yearsInService,name);
		this.modelnumber = modelNumber;
	}
	
	public int getModelNumber() {
		return modelnumber;
	}

}
