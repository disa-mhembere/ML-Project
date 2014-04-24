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
  [to_email_in,  from_email_in, cc_to_email_in, bcc_to_email_in, mean_email_len,
  to_email_outn,  from_email_outn, cc_to_email_outn, bcc_to_email_outn,
  num_attachments, on_weekend, on_weekday, num_emails_dbh, num_emails_abh, degree,
  scan1, triangle, transitivity, normed_eigenvalue
  ]
"""
CC_INDEX_IN = 2
CC_INDEX_OUTN = 7

BCC_INDEX_IN = 3
BCC_INDEX_OUTN = 8

TO_INDEX_IN = 0
TO_INDEX_OUTN = 5

EMAIL_LEN_INDEX = 4
INV_INDEX_START = 15

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
      self.data[week][_id] = np.array([0]*self.num_features, dtype=np.float32) # NOTE: float32
    
    self.data[week][_id] += count_list

  def verify(self, week, _id):
    assert isinstance(_id, int), "ID must be an int"
    if not self.data.has_key(week):
      self.data[week] = {}

    if not self.data[week].has_key(_id):
      self.data[week][_id] = np.array([0]*self.num_features, dtype=np.float32) # NOTE: float32

  def insert_email(self, week, _id, to_email_in, to_email_outn, cc_to_email_in,
     cc_to_email_outn, bcc_to_email_in, bcc_to_email_outn, during_business,
     weekday, email_length, attachment):

    self.verify(week, _id) # Wasteful!
    self.data[week][_id] += [ to_email_in, 0, cc_to_email_in, bcc_to_email_in, email_length,
        to_email_outn, 0, cc_to_email_outn, bcc_to_email_outn, attachment,
        int(not weekday), weekday, during_business, int(not during_business), 0, 0, 0, 0, 0 
        ]

  def update_to(self, week, recepient_id, is_in_network):
    self.verify(week, recepient_id) # Wasteful!

    if is_in_network:
      self.data[week][recepient_id][TO_INDEX_IN] += 1
    else: 
      self.data[week][recepient_id][TO_INDEX_OUTN] += 1


  def update_cc(self, week, recepient_id, is_in_network):
    self.verify(week, recepient_id) # Wasteful!

    if is_in_network:
      self.data[week][recepient_id][CC_INDEX_IN] += 1
    else:
      self.data[week][recepient_id][CC_INDEX_OUTN] += 1


  def update_bcc(self, week, recepient_id, is_in_network):
    self.verify(week, recepient_id) # Wasteful!
    if is_in_network:
      self.data[week][recepient_id][BCC_INDEX_IN] += 1
    else:
      self.data[week][recepient_id][BCC_INDEX_OUTN] += 1

  def _update_inv(self, week, _id, invariants):
    """
    Add the precomputed invariants 
    """
    self.verify(week, _id) # Wasteful!

    self.data[week][_id][INV_INDEX_START:] = invariants

  def finish(self, ):
    for week in self.data.keys():
      for _id in self.data[week].keys():
        sum_emails = self.data[week][_id][TO_INDEX_IN] +\
            self.data[week][_id][TO_INDEX_OUTN] 
        if sum_emails: # Divisor cannot be zero but OK if numerator is 
          self.data[week][_id][EMAIL_LEN_INDEX] /= float(sum_emails)

  def __repr__(self):
    """ Print me """
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
