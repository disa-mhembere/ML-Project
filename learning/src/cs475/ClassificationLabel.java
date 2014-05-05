package cs475;

import java.io.Serializable;

/**
 * @author Disa Mhembere
 * @email disa@jhu.edu
 */
public class ClassificationLabel extends Label implements Serializable
{
  private static final long serialVersionUID = 1L; // Def serializer
  private int value;

  /**
   * @param value
   */
  public ClassificationLabel(int value)
  {
    this.setValue(value);
  }

  /**
   * Return String representation of label
   */
  @Override
  public String toString()
  {
    return String.valueOf(this.getValue());
  }

  /**
   * Get the value of the label
   * 
   * @return the label value
   */
  public int getValue()
  {
    return value;
  }

  /**
   * Set the label value
   * 
   * @param value
   *          the label value
   */
  public void setValue(int value)
  {
    this.value = value;
  }

  @Override
  public boolean equals(Object object)
  {
    if (object instanceof ClassificationLabel)
    {
      ClassificationLabel other = (ClassificationLabel) object; // cast to
                                                                // RegressionLabel
      return other.getValue() == this.getValue();
    }
    // else it's not even a ClassificationLabel
    return false;
  }

}