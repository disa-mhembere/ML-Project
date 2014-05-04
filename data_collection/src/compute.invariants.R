# compute.invariants.R
# Created by Disa Mhembere on 2014-05-02.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

require(argparse)
require(igraph)

parser <- ArgumentParser(description="Compute invariants on a dir")
parser$add_argument("gfn", help="The directory with time series graphs")
parser$add_argument("-o", "--outdir", default="data", help="Output directory")
parser$add_argument("-l", "--lose.direction", action="store_true", help="Lose directionality after computing degree")

result <- parser$parse_args()

dir.create(result$outdir, showWarnings=FALSE) # if not exists
for (file in list.files(result$gfn)) { # loop through tsgs

  cat("Processing", file, " ...\n")

  g <- read.graph(paste0(result$gfn,"/",file), directed=TRUE)
  
  in.deg <- degree(g, mode="in")
  out.deg <- degree(g, mode="out")

  if (result$lose.direction) {
    cat("Dropping directionality ..\n")
    g <- as.undirected(g) # Undirect me
  }

  ss1 <- local.scan(g)
  trans <- transitivity(g, "local")
  trans[is.nan(trans)] <- 0
  tri <- igraph::adjacent.triangles(g)
  eigs <- eigen(get.adjacency(g))$values

  l <- length # typedef
  max.length <- max(l(in.deg), l(out.deg),l(ss1), l(tri), l(eigs), l(trans))

  #cat("Degree before", in.deg, "\n")
  #cat("Eigs before", eigs, "\n")
  
  # need to buffer these so we don't get out-of-bounds
  in.deg <- c(in.deg, rep(0,max.length - l(in.deg))) # right pad
  out.deg <- c(out.deg, rep(0,max.length - l(out.deg))) # right pad
  ss1 <- c(ss1, rep(0,max.length - l(ss1)))
  tri <- c(tri, rep(0, max.length - l(tri)))
  trans <- c(trans, rep(0, max.length - l(trans)))
  eigs <- c(eigs, rep(0, max.length - l(eigs)))
  
  #cat("Eigs after", eigs, "\n")
  #cat("Degree after", in.deg, "\n")

  week = as.character(as.integer(substring(strsplit(file, "[.]")[[1]][2], 7, 9))-1)
  cat("Writing week", week, " ...\n", "ID: ")
  dir.create(paste0(result$outdir,"/", week), showWarnings=FALSE)
  for (idx in 1:max.length) {
    cat(idx, " ")
    # order matters
    arr <- c(in.deg[idx], out.deg[idx], ss1[idx], tri[idx], trans[idx], eigs[idx])
    #cat("arr at week ", idx, arr, "...\n")
    save(arr, file=paste0(result$outdir,"/", week,"/",idx)) # Each userid is unique
  }
  cat("\n") 
}

cat("Saved all invariants to: ", result$outdir, "!\n")
