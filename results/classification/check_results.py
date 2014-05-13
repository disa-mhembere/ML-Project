import sys, os
import pdb

def get_vips(fn):
  f = open(fn, "rb")
  vip = range(1,185)
  vip_clusters = {}

  for line in f:
    count_vips_found = 0
    cluster_id, _id = line.split(",")
    cluster_id = int(float(cluster_id.strip()))
    _id = int(float(_id.strip()))

    if _id in vip:
      count_vips_found += 1
      if vip_clusters.has_key(cluster_id):
        vip_clusters[cluster_id].append(_id)
      else:
        vip_clusters[cluster_id] = [_id]

    if count_vips_found == len(vip): break
  return vip_clusters

def get_stats(vip_clusters):
  TOTAL_KNOWN = 184
  print "Number of clusters,", len(vip_clusters)
  max_len_cluster = (-1, 0) # id, len

  for entry in vip_clusters.iteritems():
    if len(entry[1]) > max_len_cluster[1]:
      max_len_cluster = entry[0], len(entry[1])

  misclassified = TOTAL_KNOWN - len(vip_clusters[max_len_cluster[0]])
  print "Number misclassified,", misclassified
  print "% misclassified,", 100*(float(misclassified)/TOTAL_KNOWN)
  
# main
if len(sys.argv) < 2:
  print "usage: check_results.py clusterfile"
  exit(-1)

cl = get_vips(sys.argv[1])
get_stats(cl)

