import sys
import cPickle
import os

def write_subsection(fn, n):
  
  tsfv_obj = cPickle.load(open(fn, "rb"))  

  count = 0 
  d = {}
  for key in sorted(tsfv_obj):
    print "Attempting %d" % key
    d[key] = tsfv_obj[key]
    count += 1

    if count == n: break

  out_fn = "enron_plus_%d_composite.cPickle" % (n-200)
  cPickle.dump(d, open(out_fn ,"wb"))

if len(sys.argv) < 2:
  print "usage: get_partition.py pickle filename, number_of_id"
  exit(-1)
write_subsection(sys.argv[1], int(sys.argv[2])) 
