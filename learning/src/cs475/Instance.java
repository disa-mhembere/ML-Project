package cs475;

import java.io.Serializable;

public class Instance implements Serializable
{
  private static final long serialVersionUID = 1L;

  Label _label = null;
  FeatureVector _feature_vector = null;
  Label _orginalLabel = null;

  public Instance(FeatureVector feature_vector, Label label)
  {
    this._feature_vector = feature_vector;
    this._label = label;
    this._orginalLabel = label;
  }

  public Label getLabel()
  {
    return _label;
  }

  public Label get_orginalLabel() {
	return _orginalLabel;
}

public void set_orginalLabel(Label _orginalLabel) {
	this._orginalLabel = _orginalLabel;
}

public void setLabel(Label label)
  {
    this._label = label;
  }

  public FeatureVector getFeatureVector()
  {
    return _feature_vector;
  }

  public void setFeatureVector(FeatureVector feature_vector)
  {
    this._feature_vector = feature_vector;
  }

}
