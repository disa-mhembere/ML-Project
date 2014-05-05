package cs475;

import java.io.Serializable;

/**
 * @author Disa Mhembere
 * @email disa@jhu.edu
 */

public class RegressionLabel extends Label implements Serializable
{
  private static final long serialVersionUID = 1L; // Def serializer
  private double value;

  public RegressionLabel(double value)
  {
    this.setValue(value);
  }

  @Override
  public String toString()
  {
    return String.valueOf(this.getValue());
  }

  /**
   * Get the label value
   * 
   * @return the value associated with label
   */
  public double getValue()
  {
    return value;
  }

  /**
   * Set the label value
   * 
   * @param value
   *          the label to set
   */
  public void setValue(double value)
  {
    this.value = value;
  }

  @Override
  public boolean equals(Object object)
  {
    if (object instanceof RegressionLabel)
    {
      RegressionLabel other = (RegressionLabel) object; // cast to
                                                        // RegressionLabel
      return other.getValue() == this.getValue();
    }
    // else it's not even a RegressionLabel
    return false;
  }
}