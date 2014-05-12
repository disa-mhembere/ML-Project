package cs475.classification;

import java.io.FileNotFoundException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

import cs475.ClassificationLabel;
import cs475.Instance;
import cs475.Label;
import cs475.Predictor;
import cs475.structures.SparseVector;
import cs475.utils.Printer;

public class WeightedKNN extends Predictor
{
  List<SparseVector> distanceMatrix; // The
  
  List<Instance> instances;
  int number_itrerations = 0;
  

  public WeightedKNN( int iterations) {
    number_itrerations = iterations;
  }
  
  private static final long serialVersionUID = 1L;

  
  public Label getVote(Instance instance, int instanceIndex){
	  
	  // Data Structure to store the weight for each Label
	  HashMap<Label, Double> countKeeper = new HashMap<Label, Double>();
	  
	  // Iterating over the instance list and update the HashMap
	  for (int i=0; i<this.instances.size(); i++){
		  Label clusterId = this.instances.get(i).getLabel();
		  
		  double clusterWeight = distanceMatrix.get(i).get(instanceIndex);
		  
		  if ( countKeeper.containsKey( clusterId ))
			  countKeeper.put(clusterId, countKeeper.get(clusterId) + (Double)(clusterWeight));
		  else
			  countKeeper.put(clusterId, clusterWeight);		  
	  }
	  
	  //Iterating over the HashMap to get a key associated with the maximum value
	  Map.Entry<Label, Double> maxEntry = null;
	  
	  for(Map.Entry<Label, Double> entry : countKeeper.entrySet()){
		  //System.out.println(entry.getKey()+" "+entry.getValue());
		  if (maxEntry == null || entry.getValue().compareTo(maxEntry.getValue()) > 0){
			  maxEntry = entry;
		  }
	  }
	  
	  return maxEntry.getKey();
  }
  @Override
  public void train(List<Instance> instances) throws FileNotFoundException, UnsupportedEncodingException {
    distanceMatrix = new ArrayList<SparseVector>();
    
    // distanceMatrix = new double[instances.size()][instances.size()];
    
    this.instances = instances;
    
    // Computing the distance matrix once for every train
    computeDistanceMatrix();
    
    System.out.println("Training");
    for ( int l=0; l<number_itrerations; l++){
    	// Iterating over all the instances
        for (int i=0; i<this.instances.size(); i++) {
        	instances.get(i).setLabel( getVote(this.instances.get(i), i) );
        }
    }
    //Printer.printInstanceList(instances);
    Printer.printLabelList(instances);
    Printer.writeLabelList(instances);
  }
  
  /**
   * Compute the distance matrix from each sample to one another once only
   * @param instances feature vector instances
   */
  void computeDistanceMatrix() {
	  
	System.out.println("Computing Distance Matrix");
    for (int i=0; i<this.instances.size(); i++) {
      Instance curr = this.instances.get(i);
      SparseVector newSV = new SparseVector();
      
      for (int ii=0; ii<this.instances.size(); ii++) {
        newSV.add(ii, eucl_dist(curr.getFeatureVector(), 
                        this.instances.get(ii).getFeatureVector())); // Each row belongs to a specific feature vector 
      }
      distanceMatrix.add(newSV); // The row to the distance Matrix
    }
    // Makes the feature vector null
    clearListInstances();
    
  }
  
  /**
   * Clear the feature vector in List od instances
   * @param instances feature vector instances
   */
  void clearListInstances() {
	 
	  System.out.println("Garbage Collecting");
	  //Garbage Collect feature vectors
	   for (int i=0;i<this.instances.size(); i++){
	    this.instances.get(i).setFeatureVector(null);
	   }
	   System.gc();
  }

  @Override
  public Label predict(Instance instance)
  {	  
    if (null == distanceMatrix)
      throw new IllegalStateException("You must train before you can predict -- genius!");
    return new ClassificationLabel(getCluster(instance));
  }
  
  /**
   * Return which cluster a specific instance should belong to
   * @param instance
   * @return
   */
  private int getCluster(Instance instance)
  {
    // TODO Auto-generated method stub
    return 0;
  }
  
  /**
   * Get the Euclidean distance between 2 SparseVectors `
   * @param u a sparseVector
   * @param v another sparseVector
   * @return the euclidean distance 
   */
  private double eucl_dist(SparseVector u, SparseVector v)
  {
    Set<Integer> indexes = new HashSet<Integer>();
    indexes.addAll(u.getVector().keySet()); // Add all nnz indexes from u
    indexes.addAll(v.getVector().keySet()); // Add all nnz from v
    
    Iterator<Integer> itr = indexes.iterator();
    double squareDiff = 0;
    while (itr.hasNext())
    {
      int idx = itr.next();
      
      double diff = u.get(idx) - v.get(idx); 
      squareDiff += (diff*diff);
    }
    return Math.sqrt(squareDiff);
  }
  

  /**
   * Tester Main
   * @param args
   */
  public static void main(String[] args)
  {
    // TODO Auto-generated method stub

  }


}