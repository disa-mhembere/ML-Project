package cs475.utils;

import java.util.Comparator;

import cs475.ClassificationLabel;
import cs475.Instance;
import cs475.RegressionLabel;

public class InstanceComparator implements Comparator<Instance>{

	@Override
	public int compare(Instance o1, Instance o2) {
		// TODO Auto-generated method stub
		if( o1.getLabel().equals(o2.getLabel()))
			return 0;
		else if( ((RegressionLabel)o1.getLabel()).getValue() > ((RegressionLabel)o2.getLabel()).getValue() )
			return 1;
		else return -1;
	}

}
