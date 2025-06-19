package il.ac.tau.cs.sw1.ex9.starfleet;

import java.util.Comparator;
import java.util.Map;
import java.util.Map.Entry;


public class ComparatorMapEntryByRankPopularity implements Comparator<Map.Entry<OfficerRank, Integer>>{

	@Override
	public int compare(Entry<OfficerRank, Integer> o1, Entry<OfficerRank, Integer> o2) {
		int val = o1.getValue().compareTo(o2.getValue());
		if(val==0)
			return o1.getKey().compareTo(o2.getKey());
		return val;
	}
	
}