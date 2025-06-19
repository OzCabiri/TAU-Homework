package il.ac.tau.cs.sw1.ex9.starfleet;


import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.HashMap;
import java.util.HashSet;
import java.util.ArrayList;


public class StarfleetManager {

	/**
	 * Returns a list containing string representation of all fleet ships, sorted in descending order by
	 * fire power, and then in descending order by commission year, and finally in ascending order by
	 * name
	 */
	public static List<String> getShipDescriptionsSortedByFirePowerAndCommissionYear (Collection<Spaceship> fleet) {
		List<Spaceship> sortedShips = new ArrayList<>();
		sortedShips.addAll(fleet);
		sortedShips.sort(new ComparatorShipByFPandCY());
		
		List<String> shipDescriptions = new ArrayList<>();
		for(Spaceship ship : sortedShips)
			shipDescriptions.add(ship.toString());
		
		return shipDescriptions;
	}

	/**
	 * Returns a map containing ship type names as keys (the class name) and the number of instances created for each type as values
	 */
	public static Map<String, Integer> getInstanceNumberPerClass(Collection<Spaceship> fleet) {
		Map<String, Integer> numPerClass = new HashMap<>();
		for(Spaceship ship : fleet) {
			numPerClass.put(ship.getClass().getSimpleName(),numPerClass.getOrDefault(ship.getClass().getSimpleName(), 0)+1);
		}
		return numPerClass;
	}


	/**
	 * Returns the total annual maintenance cost of the fleet (which is the sum of maintenance costs of all the fleet's ships)
	 */
	public static int getTotalMaintenanceCost (Collection<Spaceship> fleet) {
		int totalcost = 0;
		for(Spaceship ship : fleet) {
			totalcost += ship.getAnnualMaintenanceCost();
		}
		return totalcost;
	}


	/**
	 * Returns a set containing the names of all the fleet's weapons installed on any ship
	 */
	public static Set<String> getFleetWeaponNames(Collection<Spaceship> fleet) {
		Set<String> weaponsSet = new HashSet<>();
		for(Spaceship ship : fleet) {
			if(ship instanceof myAbstractBattleship) {
				myAbstractBattleship battleship = (myAbstractBattleship)ship;
				for(Weapon wp : battleship.getWeapon())
					weaponsSet.add(wp.getName());	
			}	
		}
		return weaponsSet;
	}

	/*
	 * Returns the total number of crew-members serving on board of the given fleet's ships.
	 */
	public static int getTotalNumberOfFleetCrewMembers(Collection<Spaceship> fleet) {
		int totalCrewMembers = 0;
		for(Spaceship ship : fleet) {
			totalCrewMembers += ship.getCrewMembers().size();
		}
		return totalCrewMembers;
	}

	/*
	 * Returns the average age of all officers serving on board of the given fleet's ships. 
	 */
	public static float getAverageAgeOfFleetOfficers(Collection<Spaceship> fleet) {
		float numOfOfficers = 0;
		float totalAge = 0;
		for(Spaceship ship : fleet) {
			for(CrewMember member : ship.getCrewMembers()) {
				if(member instanceof Officer) {
					numOfOfficers++;
					totalAge += member.getAge();
				}
			}
		}
		return totalAge/numOfOfficers;
	}

	/*
	 * Returns a map mapping the highest ranking officer on each ship (as keys), to his ship (as values).
	 */
	public static Map<Officer, Spaceship> getHighestRankingOfficerPerShip(Collection<Spaceship> fleet) {
		Map<Officer, Spaceship> highestRankingOfficers = new HashMap<>();
		Officer commandingOfficer = null;
		for(Spaceship ship : fleet) {
			commandingOfficer = getHighestRankingOfficerInShip(ship);
			if(commandingOfficer!=null)
				highestRankingOfficers.put(commandingOfficer, ship);
		}
		return highestRankingOfficers;
	}
	private static Officer getHighestRankingOfficerInShip(Spaceship ship) {
		Officer commandingOfficer = null;
		for(CrewMember member : ship.getCrewMembers()) {
			if(member instanceof Officer) {
				Officer currOfficer = (Officer)member;
				if(commandingOfficer==null)
					commandingOfficer = currOfficer;
				else {
					if(currOfficer.getRank().compareTo(commandingOfficer.getRank())>0)
						commandingOfficer = currOfficer;
				}
			}
		}
		return commandingOfficer;
	}

	/*
	 * Returns a List of entries representing ranks and their occurrences.
	 * Each entry represents a pair composed of an officer rank, and the number of its occurrences among starfleet personnel.
	 * The returned list is sorted ascendingly based on the number of occurrences.
	 */
	public static List<Map.Entry<OfficerRank, Integer>> getOfficerRanksSortedByPopularity(Collection<Spaceship> fleet) {
		Map<OfficerRank, Integer> popularRankMap = createPopularRankMap(fleet);
		List<Map.Entry<OfficerRank, Integer>> popularRankList = new ArrayList<>();
		popularRankList.addAll(popularRankMap.entrySet());
		popularRankList.sort(new ComparatorMapEntryByRankPopularity());
		return popularRankList;
	}
	private static Map<OfficerRank, Integer> createPopularRankMap(Collection<Spaceship> fleet){
		Map<OfficerRank, Integer> popularRankMap = new HashMap<>();
		Officer currOfficer = null;
		for(Spaceship ship : fleet) {
			for(CrewMember member : ship.getCrewMembers()) {
				if(member instanceof Officer) {
					currOfficer = (Officer)member;
					popularRankMap.put(currOfficer.getRank(), popularRankMap.getOrDefault(currOfficer.getRank(), 0)+1);
				}
			}
		}
		return popularRankMap;
	}

}
