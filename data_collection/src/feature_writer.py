#!/usr/bin/python

# feature_writer.py
# Created by on 2014-03-30.
# Email: disa@jhu.edu | lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.

import operator
import argparse
import cPickle
import numpy as np

import pdb

def write_file( tsfvName, writeFile ):
  """ Writes a TSFV to a file. """

  # Read the Pickle file from disk and load it
  fs = open(tsfvName,'r')
  tsfv = cPickle.load(fs)
  filename = open(writeFile, 'wb')

  # Setting the flag for inserting a newline to False
  flag = False
  # Iterating over the TSFV data structure
  for i in sorted( tsfv.data.iteritems(), key=operator.itemgetter(0) ):
    
    print "Week id:", i[0]
    for j in i[1].iteritems():
    
      if np.count_nonzero(j[1]) > 0:
        filename.write( "{} ".format(j[0]) )
      print "\tUser id:", j[0]
      for idx, value in enumerate(j[1]):
     
        # Checking if the value is 0.0. This is for creating a sparse matrix
        if ( value!=0.0 ):

          # Setting the flag to True, will insert a newline at the end of this feaature vector
          flag = True
          # Writing the feature vector to file
          preciseValue = "{:.16f}".format(value)
          filename.write( "{}:{} ".format( idx+1, str(preciseValue) ) )

      # If the feature vector had a single non-zero value then insert a newline
      if ( flag ):
        filename.write('\n')
      flag = False

def write_small_dict( tsfvName, writeFile ):
  """ Writes the TSFV as a dict """

  # Read the Pickle file from disk and load it
  fs = open(tsfvName, 'rb')
  tsfv = cPickle.load(fs)
  filename = open(writeFile, 'wb')

  # Iterating over hte TSFV data structure

  for i in tsfv.data.iteritems():
    for idx,value in enumerate (i[1]):

      if ( value!=0.0) :

        flag = True
        preciseValue = "{:.16f}".format(value)
        filename.write( "{}:{} ".format( idx+1, str(preciseValue) ) )

    if ( flag ):
        filaname.write('\n')
    flag = False

def main():

  # Sample data structure for testing before tsfv
  #x = {1: [1,2], 3: [1,4], 4:[1,3], 2:[1,10], 0:[0,9]}
  #y = {4:x, 1:x, 2:x}

  # Taking arguments from user
  parser = argparse.ArgumentParser(description="Write the tsfv to file")
  parser.add_argument("read_file", action="store", help="File Name to read from")
  parser.add_argument("write_file", action="store", help="File Name to write to")

  result = parser.parse_args()

  # Calling the function to write the feature vector to a file
  #write_file(result.read_file, result.write_file)
  write_small_dict) result.read_file, result.write_file )

if __name__ == "__main__":
  main()
