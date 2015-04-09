package cs475;

import java.io.FileNotFoundException;
import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.util.List;

public abstract class Predictor implements Serializable
{
  private static final long serialVersionUID = 1L;

  public abstract void train(List<Instance> instances) throws FileNotFoundException, UnsupportedEncodingException;

  public abstract Label predict(Instance instance);
}
