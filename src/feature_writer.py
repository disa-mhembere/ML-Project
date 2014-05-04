#!/usr/bin/python

# feature_writer.py
# Created by on 2014-03-30.
# Email: disa@jhu.edu | lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.

import operator
import argparse
import cPickle
import pdb

def write_file( tsfvName, writeFile ):
  """ Writes a TSFV to a file. """
  
  fs = open(tsfvName,'r')
  tsfv = cPickle.load(fs)
  filename = open(writeFile, 'wb')
  flag = False

  for i in sorted( tsfv.data.iteritems(), key=operator.itemgetter(0) ):
    
    for j in i[1].iteritems():
      
      for idx, value in enumerate(j[1]):
       
        if ( value!=0.0 ):
          flag = True
          filename.write( "{}:{} ".format( idx+1, str(value) ) )

      if ( flag ):
        filename.write('\n')
      flag = False

def main():

  x = {1: [1,2], 3: [1,4], 4:[1,3], 2:[1,10], 0:[0,9]}
  y = {4:x, 1:x, 2:x}
  #write_file(y)

  parser = argparse.ArgumentParser(description="Write the tsfv to file")
  parser.add_argument("read_file", action="store", help="File Name to read from")
  parser.add_argument("write_file", action="store", help="File Name to write to")

  result = parser.parse_args()

  write_file(result.read_file, result.write_file)

if __name__ == "__main__":
  main()
