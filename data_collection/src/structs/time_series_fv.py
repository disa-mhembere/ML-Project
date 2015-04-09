#!/usr/bin/python

# time_series_fv.py
# Created by on 2014-03-30.
# Email: disa@jhu.edu, lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.

import numpy as np
import cPickle
from os import remove

from sklearn import preprocessing
import operator
import pdb

"""
Feature vector order:
  [to_email_in,  from_email_in, cc_to_email_in, bcc_to_email_in, mean_email_len,
  to_email_outn,  from_email_outn, cc_to_email_outn, bcc_to_email_outn,
  num_attachments, to_on_weekend, to_on_weekday, to_num_emails_dbh, to_num_emails_abh, 
  from_num_emails_dhb, from_num_emails_abh, from_on_weekend, from_on_weekday, indegree,
  outdegree, scan1, triangle, transitivity, normed_eigenvalue
  ]  
""" # NOTE: business_hours & weekend/day no distinction between from,cc,bcc
FROM_NUM_EMAILS_DHB_INDEX = 14
FROM_NUM_EMAILS_ABH_INDEX = 15
FROM_ON_WEEKEND_INDEX = 16
FROM_ON_WEEKDAY_INDEX = 17

CC_INDEX_IN = 2
CC_INDEX_OUTN = 7

BCC_INDEX_IN = 3
BCC_INDEX_OUTN = 8

TO_INDEX_IN = 0
TO_INDEX_OUTN = 5

EMAIL_LEN_INDEX = 4
INV_INDEX_START = 18

NUM_INVARIANTS = 6

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
    @obsolete
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
    """ Email sent `From` me """

    self.verify(week, _id) 
    self.data[week][_id] += [ to_email_in, 0, cc_to_email_in, bcc_to_email_in, email_length,
        to_email_outn, 0, cc_to_email_outn, bcc_to_email_outn, attachment,
        -weekday if weekday < 0 else 0, weekday if weekday > 0 else 0, 
        during_business if during_business > 0 else 0, 
        -during_business if during_business < 0 else 0, 0, 0, 0, 0
        ] + [0]*NUM_INVARIANTS

  def update_to(self, week, recepient_id, is_in_network, weekday, during_business):
    """" Email sent `to` me """
    self.verify(week, recepient_id) 

    if is_in_network:
      self.data[week][recepient_id][TO_INDEX_IN] += 1
    else: 
      self.data[week][recepient_id][TO_INDEX_OUTN] += 1

    self._update_day_time(week, recepient_id, weekday, during_business)

  def update_cc(self, week, recepient_id, is_in_network, weekday, during_business):
    self.verify(week, recepient_id) 

    if is_in_network:
      self.data[week][recepient_id][CC_INDEX_IN] += 1
    else:
      self.data[week][recepient_id][CC_INDEX_OUTN] += 1

    self._update_day_time(week, recepient_id, weekday, during_business)


  def update_bcc(self, week, recepient_id, is_in_network, weekday, during_business):
    self.verify(week, recepient_id)

    if is_in_network:
      self.data[week][recepient_id][BCC_INDEX_IN] += 1
    else:
      self.data[week][recepient_id][BCC_INDEX_OUTN] += 1

    self._update_day_time(week, recepient_id, weekday, during_business)

  def _update_day_time(self, week, recepient_id, weekday, during_business):
    """ Helper to update the time of day & day for received emails """
    if weekday:
      self.data[week][recepient_id][FROM_ON_WEEKDAY_INDEX] += 1
    else: 
      self.data[week][recepient_id][FROM_ON_WEEKEND_INDEX] += 1

    if during_business:
      self.data[week][recepient_id][FROM_NUM_EMAILS_DHB_INDEX] += 1
    else: 
      self.data[week][recepient_id][FROM_NUM_EMAILS_ABH_INDEX] += 1

  def update_inv(self, week, _id, invariants):
    """
    Add the precomputed invariants 
    """
    self.verify(week, _id)
    self.data[week][_id][INV_INDEX_START:] = invariants

  def finish(self):
    for week in self.data.keys():
      for _id in self.data[week].keys():
        sum_emails = self.data[week][_id][TO_INDEX_IN] +\
            self.data[week][_id][TO_INDEX_OUTN] 
        if sum_emails: # Divisor cannot be zero but OK if numerator is 
          self.data[week][_id][EMAIL_LEN_INDEX] /= float(sum_emails)

  def normalize(self):
    """ Using scikitlearn to normalize the feature value matrix """
    # Iterating over the dict in sorted order to extract feature vectors
    test = []
    for i in sorted( self.data.iteritems(), key=operator.itemgetter(0) ):
      for j in i[1].iteritems():
        test.append(j[1])
    x_train = np.vstack( [ test ] )
    
    # Normalizing the matrix using scikitlearn
    min_max_scaler = preprocessing.MinMaxScaler()
    x_train_minmax = min_max_scaler.fit_transform( x_train )

    # Inserting the array back into the dict
    counter = 0
    for i in sorted( self.data.iteritems(), key=operator.itemgetter(0) ):
      for j in i[1].iteritems():
        self.data.get( i[0] )[ j[0] ] = x_train_minmax[counter]
        counter = counter + 1

  def __repr__(self):
    """ Print me """
    s = ""
    for week in sorted(self.data.keys()):
      for person_id in sorted(self.data[week].keys()):
        s += "id: %d ==> Counts: %s\n" % (person_id, str(self.data[week][person_id]))
    return s
  
  def collapse(self, fn="compositeTSFV.cPickle"):
    """ Collapse time series feature vector in to a single ID feature vector """
    unique_id_count = 0
    composite = {} # key = user_id, value = fv

    for key in self.data.keys(): # (yyyy, week)
      for entry in self.data[key].iteritems(): # (id, FV)
        if composite.has_key(entry[0]):
          composite[entry[0]] += entry[1]
        else: 
          print "Adding new id:", entry[0]
          unique_id_count += 1
          composite[entry[0]] = entry[1]

    print "Unique id's added to compositeTSFV =", unique_id_count
    cPickle.dump(composite, open(fn, "wb"), protocol=2)

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
  tsfv_obj = tsfv(24)
  tsfv_obj.insert_email(week=1, _id=69, to_email_in=5, to_email_outn=10, cc_to_email_in=15, cc_to_email_outn=0, bcc_to_email_in=0, bcc_to_email_outn=0, during_business=1, weekday=1, email_length=1000, attachment=3)

  tsfv_obj.insert_email(week=1, _id=69, to_email_in=10, to_email_outn=5, cc_to_email_in=0, cc_to_email_outn=15, bcc_to_email_in=15, bcc_to_email_outn=15, during_business=0, weekday=14, email_length=1000, attachment=12)
  
  tsfv_obj.insert_email(week=2, _id=70, to_email_in=11, to_email_outn=10, cc_to_email_in=0, cc_to_email_outn=11, bcc_to_email_in=15, bcc_to_email_outn=13, during_business=0, weekday=14, email_length=1000, attachment=12)
  
  tsfv_obj.insert_email(week=3, _id=100, to_email_in=11, to_email_outn=20, cc_to_email_in=0, cc_to_email_outn=11, bcc_to_email_in=15, bcc_to_email_outn=15, during_business=0, weekday=9, email_length=1, attachment=1)

  tsfv_obj.finish()
  tsfv_obj.collapse()
  exit(-1) # TODO: Premature exit


  tsfv_obj.normalize()
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
