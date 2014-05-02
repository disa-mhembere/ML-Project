# compute.invariants.R
# Created by Disa Mhembere on 2014-05-02.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

require(argparse)
require(igraph)

parser <- ArgumentParser(description="Compute invariants on a dir")
parser$add_argument("gfn", help="The directory with time series graphs")

result <- parser$parse_args()

for (file in list.files(result$gfn)) { # loop through tsgs
  
  deg <- degree(g)
  ss1 <- local.scan(g)
  trans <- transitivity(g, "local")
  tri <- igraph::adjacent.triangles(g)
  eigs <- eigen(get.adjacency(g))$values

  l <- length # typedef
  max.length <- max(l(deg), l(ss1), l(tri), l(eigs), l(trans))
  
  # need to buffer these so we don't get out-of-bounds
  deg <- c(deg, rep(0,max.length - l(deg))) # right pad
  ss1 <- c(ss1, rep(0,max.length - l(ss1)))
  tri <- c(tri, rep(0, max.length - l(tri)))
  trans <- c(trans, rep(0, max.length - l(trans)))
  eigs <- c(eigs, rep(0, max.length - l(eigs)))
  
  week = as.character(as.integer(substring(strsplit(file, "[.]")[[1]][2], 7, 9))-1))
  dir.create(week)
  for (idx in 1:max.length) {
    # order matters
    arr <- [ deg[idx], ss1[idx], tri[idx], trans[idx], eigs[idx] ] 
    save(arr, file=paste0(week,"/",idx)) # Each userid is unique
  }
}
