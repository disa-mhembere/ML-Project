#!/usr/bin/python

# names_to_ids.py
# Created by Disa Mhembere on 2014-03-30.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

import argparse

class People(object):

  def __init__(self, fn):
    self.names = self.get_dict(fn)
    self.max_id = len(self.names)

  def get_id(self, email):
    """
    Get a person's ID given their email address
    If none exists create one and assign ID chronologically

    @param email: the eamil address requires
    """
    _id = self.names.get(email)
    if _id: return _id
    else: return self._gen_id(email)
  
  def _gen_id(self, email):
    """
    Generate a new ID given an email address
    """
    self.max_id += 1
    self.names[email] = self.max_id
    return self.max_id

  def get_dict(self, fn):
    """"
    Get the email addresses associated with individuals from employees who 
    were included in the Enron graphs
    """
    f = open(fn, "rb")
    lines = f.read().splitlines()
    people_dict = {}

    for idx, line in enumerate(lines):
      people_dict[line.split("\t")[0]+"@enron.com"] = idx+1 # NOTE: 1-based indexing

    return people_dict

  def to_file(self, fn):
    s = ""
    for key in self.names.keys():
      s += key + "\t" + str(self.names[key]) + "\n"

    f = open(fn, "wb")
    f.write(s)
    f.close()

def main():
  parser = argparse.ArgumentParser(description="Get the id of a person and \
      associate with id in enron graphs")
  parser.add_argument("name_file", action="store", help="File with names of enron \
      employees in the enron graphs")

  result = parser.parse_args()
  
  peeps = People(result.name_file)
  peeps.get_id("disa@rando.com")

  print peeps.names
  print peeps.get_id("disa@rando.com")
  print peeps.names

  peeps.to_file("testpeople.txt")

if __name__ == "__main__":
  main()
