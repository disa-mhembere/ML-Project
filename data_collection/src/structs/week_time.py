#!/usr/bin/python

# time_series_fv.py
# Created by on 2014-03-30.
# Email: disa@jhu.edu, lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.

YEAR_WEEKS = {1998:53, 1999:52, 2000:52, 2001:52, 2002:52, 2003:52}

class Weektime(object):
  
  def __init__(self, start, num_weeks):
    self.year, self.week = start
    self.num_weeks = num_weeks
    self.iterdweek = 0

  def __iter__(self):
    return self
  
  def __next__(self):
    return self.next()

  def next(self):
    if self.iterdweek > self.num_weeks:
      raise StopIteration()

    if self.week >= YEAR_WEEKS[self.year]:
      self.year += 1
      self.week = 1
    else: self.week += 1
    self.iterdweek += 1
    return (self.year, self.week)

def mini_test():
  weeks = Weektime((1998,9), 189)
  for week in weeks:
    print week

if __name__ == "__main__":
  mini_test()
