package cs475;

import java.util.List;

/**
 * @author Disa Mhembere
 * @email disa@jhu.edu
 */
public class AccuracyEvaluator extends Evaluator
{

  @Override
  public double evaluate(List<Instance> instances, Predictor predictor)
  {
    int sampleSize = instances.size(); // sample size
    int numCorrect = 0;
    // List<Double> predictions =

    for (Instance inst : instances)
    {
      Label precitedLabel = predictor.predict(inst);

      if (precitedLabel.equals(inst.getLabel())) numCorrect++;
    }
    System.out.println("Accuracy Evaluator Value: " + numCorrect
        / ((double) sampleSize));
    return numCorrect / ((double) sampleSize);
  }

}
