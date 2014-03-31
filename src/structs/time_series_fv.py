#!/usr/bin/python

# time_series_fv.py
# Created by on 2014-03-30.
# Email: disa@jhu.edu, lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.
import numpy as np

class tsfv(object):
  
  def __init__(self, num_features, weeks=189):
    """ 
    Class representing a time series feature vector for all employess

    @param weeks: the number of weeks in the feature vector
    """
    assert isinstance(num_features, int), "Number of features must be an int"
    self.num_features = num_features
    self.data = {}
    for week in xrange(weeks):
      self.data[week+1] = {} # **Note: 1-based indexing to match graphs
  
  def insert(self, _id, count_list, week):
    """
    Insert method for a single week for a user
    @param _id: the id of the user 
    @param count_list: the list/np.arrays with counts for a single user email
    @param week: the week in which you want to add this to
    """
    assert isinstance(_id, int), "ID must be an int"

    if not self.data[week].has_key(_id):
      self.data[week][_id] = np.array([0]*self.num_features)
    
    #try:
    self.data[week][_id] += count_list
    #except:
      #import pdb; pdb.set_trace()

  def __repr__(self):
    """ Print me"""
    s = ""
    for week in sorted(self.data.keys()):
      for person_id in sorted(self.data[week].keys()):
        s += "id: %d ==> Counts: %s\n" % (person_id, str(self.data[week][person_id]))
    return s

def mini_test():
  tsfv_obj = tsfv(5, 10)
  tsfv_obj.insert(1, np.array([1, 32, 5, 3, 5]), 1)
  tsfv_obj.insert(1, np.array([2, 2, 2, 2, 2]), 1)
  tsfv_obj.insert(3, np.array([1, 32, 5, 3, 5]), 4)

  print tsfv_obj

if __name__ == "__main__":
  mini_test()
