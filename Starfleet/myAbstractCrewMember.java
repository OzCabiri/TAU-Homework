package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Objects;

public abstract class myAbstractCrewMember implements CrewMember {

	private String name;
	private int age;
	private int yearsinservice;
	
	public myAbstractCrewMember(int age, int yearsInService, String name){
		this.name = name;
		this.age = age;
		this.yearsinservice = yearsInService;
	}
	
	public String getName() {
		return name;
	}
	
	public int getAge() {
		return age;
	}
	
	public int getYearsInService() {
		return yearsinservice;
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
		myAbstractCrewMember other = (myAbstractCrewMember) obj;
		return Objects.equals(name, other.name);
	}
	
	
}
