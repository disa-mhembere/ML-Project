#!/usr/bin/python

# runner.py
# Created by Disa Mhembere on 2014-03-30.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

import argparse
import datetime as dt
import cPickle
from structs.week_time import Weektime
from glob import glob
import os
from utils.r_get_array import get_r_array

def ingest(fn, inv_dir):
  """
  ingest invariant data from disk onto tsfv object

  @param fn: the tsfv object on disk
  @param inv_dir: the directory containing invariant data
  """

  # add the invariants. 
  # note: weeks 
  # arr_fn: is in usernames 
  f = open(fn, "rb")
  tsfv_obj = cPickle.load(f)
  f.close()
  
  base = os.path.abspath(inv_dir)
  week_dir_names = [a for a in os.listdir(inv_dir) if not a.startswith(".")] # No hiddens
  week_dir_names = map(str, sorted(map(int, week_dir_names ))) # must be sorted

  weeks = Weektime((1998,45), len(week_dir_names))

  for week in zip(weeks, week_dir_names):
    for arr_fn in glob(os.path.join(os.path.join(base, week[1]), "*")): # NOTE: arr_fn is the user_id
      inv = get_r_array(arr_fn)
      print "Processing week", week, " for file:", arr_fn, ": INV:", inv, " ..." 
      tsfv_obj.update_inv(week[0], int(os.path.basename(arr_fn)), inv)
  print " Normalizing the tsfv object ...."
  tsfv_obj.normalize()
  print "Saving updated tsfv object ..."
  tsfv_obj.save(os.path.splitext(fn)[0]+"_inv.cPickle")
  print "Roger that!"

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Get invariants on disk and add to tsfv object")
  parser.add_argument("fn", action="store", help="The tsfv object file name on disk")
  parser.add_argument("inv_dir", action="store", help="The dir containing data")

  result = parser.parse_args()

  ingest(result.fn, result.inv_dir)
