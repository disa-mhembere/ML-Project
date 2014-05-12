#!/bin/bash

if [[ $# -eq 2 ]]; then
  FV_FILE=$1 # Feature vector files
  MODEL_FILE=$2 # Model file
else
  echo "usage: Fakefile.sh feature_vector_fn model_fn"
  exit 1
fi

#ITERS=$3 

set -e

javac -cp .:cs475/lib/commons-cli-1.2.jar cs475/Classify.java
java -cp .:cs475/lib/commons-cli-1.2.jar cs475.Classify -algorithm weighted_knn -data $FV_FILE -mode train -model_file $MODEL_FILE

#/mnt/mrbrain/ML-Project/results/tsfv_undirected_normalized_featreures.fv
#/mnt/mrbrain/ML-Project/results/kunal_test
