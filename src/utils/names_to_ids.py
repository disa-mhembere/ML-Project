#!/usr/bin/python

# names_to_ids.py
# Created by Disa Mhembere on 2014-03-30.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

import argparse

def get_dict(fn):
  """"
  Get the email addresses associated with individuals from employees who 
  were included in the Enron graphs
  """
  f = open(fn, "rb")
  lines = f.read().splitlines()
  people_dict = {}

  for idx, line in enumerate(lines):
    people_dict[idx+1] = line.split("\t")[0]+"@enron.com" # TODO: Verify this is ok
  return people_dict

def main():
  parser = argparse.ArgumentParser(description="Get the id of a person and \
      associate with id in enron graphs")
  parser.add_argument("name_file", action="store", help="File with names of enron \
      employees in the enron graphs")

  result = parser.parse_args()
  
  print get_dict(result.name_file)

if __name__ == "__main__":
  main()
