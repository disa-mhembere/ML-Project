#!/usr/bin/python

# time_series_fv.py
# Created by on 2014-03-30.
# Email: disa@jhu.edu, lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.

import numpy as np
import cPickle
from os import remove

"""
Feature vector order:
  [to_email_in,  from_email_in, cc_to_email_in, bcc_to_email_in, mean_email_len_in,
  to_email_outn,  from_email_out, cc_to_email_out, bcc_to_email_out, mean_email_len_out,
  num_attachments, on_weekend, on_weekday, num_emails_dbh, num_emails_abh, degree,
  scan1, triangle, transitivity, normed_eigenvalue
  ]
"""
class tsfv(object):
  
  def __init__(self, num_features):
    """ 
    Class representing a time series feature vector for all employess

    @param weeks: the number of weeks in the feature vector
    """
    assert isinstance(num_features, int), "Number of features must be an int"
    self.num_features = num_features
    self.data = {} # **Note: 1-based indexing to match graphs
  
  def insert(self, _id, count_list, week):
    """
    Insert method for a single week for a user
    @param _id: the id of the user 
    @param count_list: the list/np.arrays with counts for a single user email
    @param week: (2-tuple) the week in which you want to add this to
    """
    assert isinstance(_id, int), "ID must be an int"

    if not self.data.has_key(week):
      self.data[week] = {}

    if not self.data[week].has_key(_id):
      self.data[week][_id] = np.array([0]*self.num_features)
    
    self.data[week][_id] += count_list

  def update_to(email_add, week):
    """ for a single email update a users to count """
    pass # TODO

  def insert_email(self, week, _id, to_email_in, to_email_outn, cc_to_email_in,
     cc_to_email_outn, bcc_to_email_in, bcc_to_email_outn, during_business,
     weekday, email_length, attachment):
    # weekend = int(not weekday),
    # outside_business = int(not during_business)
    pass # TODO

  def update_cc(self, week, recepient_id, sender_id):
    pass # TODO

  def update_bcc(self, week, recepient_id, sender_id):
    pass # TODO


  def __repr__(self):
    """ Print me"""
    s = ""
    for week in sorted(self.data.keys()):
      for person_id in sorted(self.data[week].keys()):
        s += "id: %d ==> Counts: %s\n" % (person_id, str(self.data[week][person_id]))
    return s

  def save(self, output_filename):
    f = open(output_filename, "wb")
    cPickle.dump(self, f, protocol=2)
    f.close()

def load(filename):
  f = open(filename, "rb")
  p = cPickle.load(f)
  f.close()
  return p

def mini_test():
  tsfv_obj = tsfv(5)
  tsfv_obj.insert(1, np.array([1, 32, 5, 3, 5]), 1)
  tsfv_obj.insert(1, np.array([2, 2, 2, 2, 2]), 1)
  tsfv_obj.insert(3, np.array([1, 32, 5, 3, 5]), 4)

  print tsfv_obj
  fn =  "rando.cPickle"

  print "Saving %s ..." % fn
  tsfv_obj.save(fn)
  
  print "Loading %s ..." % fn
  t = load(fn)
  print tsfv_obj

  print "Cleaning %s ..." % fn
  remove(fn)

if __name__ == "__main__":
  mini_test()
