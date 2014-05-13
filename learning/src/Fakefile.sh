#!/bin/bash

if [[ $# -eq 4 ]]; then
  FV_FILE=$1 # Feature vector files
  MODEL_FILE=$2 # Model file
  CLUSTER_FILE=$3 # Cluster File
  NO_ITERATIONS=$4
else
  echo "usage: Fakefile.sh feature_vector_fn model_fn cluster_output_fn no_iterations"
  exit 1
fi

#ITERS=$3 

set -e

javac -cp .:cs475/lib/commons-cli-1.2.jar cs475/Classify.java
java -Xmx400g -cp .:cs475/lib/commons-cli-1.2.jar cs475.Classify -algorithm weighted_knn -data $FV_FILE -mode train -model_file $MODEL_FILE -cluster_output $CLUSTER_FILE -clustering_training_iterations $NO_ITERATIONS

#/mnt/mrbrain/ML-Project/results/tsfv_undirected_normalized_featreures.fv
#/mnt/mrbrain/ML-Project/results/kunal_test
