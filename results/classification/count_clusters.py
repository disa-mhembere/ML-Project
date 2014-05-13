import sys

def pprint(d):
  for key in d.keys():
    print key, d[key]

if len(sys.argv) < 2:
  sys.stderr.write("usage: count_clusters.py cluster_filename")
  exit(-1)
  
fn = sys.argv[1]
data = open(fn, "rb")

unique_clusters = {} # k = cluster_id, v = count

for line in  data:
  cluster_id = int(float(line.split(",")[0]))
  if unique_clusters.has_key(cluster_id):
    unique_clusters[cluster_id] += 1
  else:
    unique_clusters[cluster_id] = 1

print "The number of unique clusters =", len(unique_clusters)
print "Largest cluster size = ", max(unique_clusters.values())  
print "The clusters and counts = "
pprint(unique_clusters)

print "Done"
