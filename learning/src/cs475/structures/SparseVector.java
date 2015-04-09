/**
 * 
 */
package cs475.structures;

import java.io.Serializable;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map.Entry;
import java.util.NoSuchElementException;
import java.util.Set;

/**
 * @author Disa Mhembere
 * @email disa@jhu.edu
 * 
 */
public class SparseVector implements Serializable
{
  private static final long serialVersionUID = 1L; // Def serializer
  private HashMap<Integer, Double> vector;

  public SparseVector()
  {
    this.vector = new HashMap<Integer, Double>(); // init
  }

  /**
   * Return the hash map (i.e underlying DS)
   * 
   * @return
   */
  public HashMap<Integer, Double> getVector()
  {
    return this.vector;
  }

  /**
   * Add a value to the feature vector
   * 
   * @param index
   *          the index of the vector where you want to insert
   * @param value
   *          the value associated with the `index'
   */
  public void add(int index, double value)
  {
    this.vector.put(index, value);
  }

  /**
   * Get value associated with vector index position
   * 
   * @param index
   *          the index
   * @return the associated value
   */
  public double get(int index)
  {
    if (!this.vector.containsKey(index))
    {
      return 0; // **Returns 0 if index requested does not exist since its a
                // sparse matrix repr**
    }
    // else
    return this.vector.get(index);
  }

  /**
   * Get an iterator of the data
   * 
   * @return iterator of all values of vector
   */
  public Iterator<Entry<Integer, Double>> getIterator()
  {
    return this.vector.entrySet().iterator();
  }

  /**
   * Get the set of nonzero indices
   * 
   * @return
   */
  public Set<Integer> getNonzeroIdx()
  {
    return this.vector.keySet();
  }

  /**
   * Get the number of nonzero elements in the vector
   * 
   * @return
   */
  public int getNumNonzero()
  {
    return this.vector.keySet().size();
  }

  /**
   * Get the max index of the features in the sparse
   * vector
   * 
   * @return An int with the value of the max index 
   */
  public int getMaxIdx()
  {
    try
    {
      return Collections.max(this.getNonzeroIdx());
    } catch (NoSuchElementException e)
    {
      System.err
          .println("No elements in the sparse matrix returning default 0 ...");
      return 0;
    }
  }
  
  @Override
  public String toString()
  {
    return this.getVector().toString();
  }
  
}