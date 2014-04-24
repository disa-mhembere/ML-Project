#!/usr/bin/python

# feature_writer.py
# Created by on 2014-03-30.
# Email: disa@jhu.edu | lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.

import operator
import cPickle
import pdb

def write_file( tsfvName ):
  """ Writes a TSFV to a file. """
  fs = open(tsfvName,'r')
  tsfv = cPickle.load(fs)
  filename = open('test','wb')

  for i in sorted( tsfv.iteritems(), key=operator.itemgetter(0) ):
    for j in i[1].iteritems():
      for k in j[1]:
        filename.write( str(k)+'\n' )

def main():

  x = {1: [1,2], 3: [1,4], 4:[1,3], 2:[1,10], 0:[0,9]}
  y = {4:x, 1:x, 2:x}
  write_file(y)

if __name__ == "__main__":
  main()
