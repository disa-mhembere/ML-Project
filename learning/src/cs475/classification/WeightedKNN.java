package cs475.classification;

import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Set;

import cs475.ClassificationLabel;
import cs475.Instance;
import cs475.Label;
import cs475.Predictor;
import cs475.structures.SparseVector;

public class WeightedKNN extends Predictor
{
  
  double [][] distanceMatrix = null;
  List<Instance> instances;
  

  public WeightedKNN( ... ) {
    
  }
  
  private static final long serialVersionUID = 1L;

  @Override
  public void train(List<Instance> instances) {
    distanceMatrix = new double[instances.size()][instances.size()];
    this.instances = instances;
  }
  
  /**
   * Compute the distance matrix from each sample to one another once only
   * @param instances feature vector instances
   */
  void computeDistanceMatrix() {
    for (int i=0; i<this.instances.size(); i++) {
      Instance curr = this.instances.get(i);
      for (int ii=0; ii<this.instances.size(); ii++) {
        distanceMatrix[i][ii] = eucl_dist(curr.getFeatureVector(), 
                                this.instances.get(ii).getFeatureVector()); // Each row belongs to a specific feature vector 
      }
    }
  }

  @Override
  public Label predict(Instance instance)
  {
    computeDistanceMatrix();
    
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