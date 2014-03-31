#!/usr/bin/python

# names_id.py
# Created by Disa Mhembere on 2014-03-30.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

import argparse

def get_dict(fn):
  f = open(fn, "rb")
  names = f.read()


def main():
  parser = argparse.ArgumentParser(description="Get the id of a person and \
      associate with id in enron graphs")
  parser.add_argument("name_file", action="store", help="File with names of enron \
      employees in the enron graphs")

  result = parser.parse_args()
  
  get_dict(result.name_file)

if __name__ == "__main__":
  main()
