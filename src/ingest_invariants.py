#!/usr/bin/python

# runner.py
# Created by Disa Mhembere on 2014-03-30.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

import datetime as dt
import cPickle


def ingest(fn, inv_dir):
  """
  Ingest invariant data from disk onto tsfv object

  @param fn: the tsfv object on disk
  @param inv_dir: the directory containing invariant data
  """

  # Add the invariants. 
  # NOTE: Weeks must be named 0 - NUM_WEEKS
  # arr_fn: Is in usernames 
  f = open(fn, "rb")
  tsfv_obj = cPickle.load(f)
  f.close()
  
  d = dt.date(1998, 11,1)
  weeks 
  for week in glob(os.path.join(inv_dir, "*")):
    for arr_fn in glob(os.path.join(week,"*")): # NOTE: arr_fn is the user_id
      tsfv_obj.update_inv(int(os.path.basename(week)), int(os.path.basename(arr_fn)))

 tsfv_obj.save(os.path.splitext(fn)[0]+"_inv.cPickle")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Get invariants on disk and add to tsfv object")
  parser.add_argument("fn", action="store", help="The tsfv object file name on disk")
  parser.add_argument("inv_dir", action="store", help="The dir containing data")

  result = parser.parse_args()

  ingest(result.data_dir)
