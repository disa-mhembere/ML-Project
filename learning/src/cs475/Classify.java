package cs475;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.LinkedList;
import java.util.List;

import org.apache.commons.cli.Option;
import org.apache.commons.cli.OptionBuilder;

import cs475.classification.*;

public class Classify
{
  static public LinkedList<Option> options = new LinkedList<Option>();
//  static int gd_iterations = 20;
  
  public static void main(String[] args) throws IOException
  {
    // Parse the command line.
    String[] manditory_args = { "mode" };
    createCommandLineOptions();
    CommandLineUtilities.initCommandLineParameters(args, Classify.options,
        manditory_args);

    String mode = CommandLineUtilities.getOptionValue("mode");
    String data = CommandLineUtilities.getOptionValue("data");
    String predictions_file = CommandLineUtilities
        .getOptionValue("predictions_file");
    String algorithm = CommandLineUtilities.getOptionValue("algorithm");
    String model_file = CommandLineUtilities.getOptionValue("model_file");
    
//    if (CommandLineUtilities.hasArg("gd_iterations"))
//        gd_iterations = CommandLineUtilities.getOptionValueAsInt("gd_iterations");
    

    // required training args
    if (mode.equalsIgnoreCase("train"))
    {
      if (data == null || algorithm == null || model_file == null)
      {
        System.out
            .println("Train requires the following arguments: data, algorithm, model_file");
        System.exit(0);
      }
      // Load the training data
      DataReader data_reader = new DataReader(data, true);
      List<Instance> instances = data_reader.readData();
      data_reader.close();

      // Train the model
      Predictor predictor = train(instances, algorithm);
      saveObject(predictor, model_file);

      // required test args
    }
    else if (mode.equalsIgnoreCase("test"))
    {
      if (data == null || predictions_file == null || model_file == null)
      {
        System.out
            .println("Test requires the following arguments: data, predictions_file, model_file");
        System.exit(0);
      }

      // Load the test data.
      DataReader data_reader = new DataReader(data, true);
      List<Instance> instances = data_reader.readData();
      data_reader.close();

      // Load the model.
      Predictor predictor = (Predictor) loadObject(model_file);
      evaluateAndSavePredictions(predictor, instances, predictions_file);
    }
    else
    {
      System.out.println("Requires mode argument.");
    }
  }

  private static Predictor train(List<Instance> instances, String algorithm)
  {

    Predictor predictor = null;

    if (algorithm.equalsIgnoreCase("weighted_knn"))
    	System.out.println("Hello");
//      predictor = new MajorityClassifier();
    
    else if(algorithm.equalsIgnoreCase("svm"))
      ; // TODO: Stub
//      predictor = new MarginPerceptron(online_learning_rate, online_training_iterations);
    
    else
    {
      System.err.printf("Unknown algorithm '%s' selected!", algorithm);
      System.exit(-1);
    }
    
    
    // Train the model using "algorithm" on "data"
    predictor.train(instances);
    new AccuracyEvaluator().evaluate(instances, predictor);

    return predictor;
  }

  private static void evaluateAndSavePredictions(Predictor predictor,
      List<Instance> instances, String predictions_file) throws IOException
  {
    PredictionsWriter writer = new PredictionsWriter(predictions_file);

    if (null == predictor)
    {
      System.err
          .println("The model file does not yet exist. Train the model before testing!");
      System.exit(-1);
    }

    // Evaluate the model if labels are available.
    if (instances.get(0).getLabel() != null)
    {
      new AccuracyEvaluator().evaluate(instances, predictor);
    }

    for (Instance instance : instances)
    {
      Label label = predictor.predict(instance);
      writer.writePrediction(label);
    }

    writer.close();
  }

  public static void saveObject(Object object, String file_name)
  {
    try
    {
      ObjectOutputStream oos = new ObjectOutputStream(new BufferedOutputStream(
          new FileOutputStream(new File(file_name))));
      oos.writeObject(object);
      oos.close();
    } catch (IOException e)
    {
      System.err.println("Exception writing file " + file_name + ": " + e);
    }
  }

  /**
   * Load a single object from a filename.
   * 
   * @param file_name
   * @return
   */
  public static Object loadObject(String file_name)
  {
    ObjectInputStream ois;
    try
    {
      ois = new ObjectInputStream(new BufferedInputStream(new FileInputStream(
          new File(file_name))));
      Object object = ois.readObject();
      ois.close();
      return object;
    } catch (IOException e)
    {
      System.err.println("Error loading: " + file_name);
    } catch (ClassNotFoundException e)
    {
      System.err.println("Error loading: " + file_name);
    }
    return null;
  }

  public static void registerOption(String option_name, String arg_name,
      boolean has_arg, String description)
  {
    OptionBuilder.withArgName(arg_name);
    OptionBuilder.hasArg(has_arg);
    OptionBuilder.withDescription(description);
    Option option = OptionBuilder.create(option_name);

    Classify.options.add(option);
  }

  private static void createCommandLineOptions()
  {
//    TODO: Stub
//    registerOption("online_learning_rate", "double", true, "The learning rate for perceptron.");
    
  }
}
