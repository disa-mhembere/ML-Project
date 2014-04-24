#!/usr/bin/python

# r_get_array.py
# Created by Disa Mhembere on 2014-04-24.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

import rpy2.robjects as robjects
import numpy as np

def get_r_list(fn):
  """
  Load an r list and return a numpy array
  
  @param fn: the filename of the array
  """
  func = robjects.r("""
  fn <- function(fn){
  load(fn) # array MUST be named arr
  arr
  }
  """)

  return np.array(func(fn))

def test():
  print get_r_list("./test.Rbin")
  print "If no error was thrown and an array printed all good ..."

if __name__ == "__main__":
  test()
