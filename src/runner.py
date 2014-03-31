#!/usr/bin/python

# runner.py
# Created by Disa Mhembere on 2014-03-30.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

# This will run the email the parser and feature writer
import argparse
import os
from email_parser import *
import email
from structs.time_series_fv import tsfv
from utils.names_to_ids import get_dict

def run(data_dir, names_fn):
  """ 
  Given a directory of emails lets get all features and build a 
  data structures with these features and graph statistics.

  @param data_dir: is the directory with all email mailboxes
  @param names_fn: the file containing the names to email address mapping
  """
  names_dict = get_dict(names_fn)

  for people_dir in os.listdir(data_dir): # Names of employees
    for email_cat in os.listdir(people_dir): # e.g sent, inbox
      for email_fn in os.listdir(email_cat):
        entry = get_entry(email.message_from_file(open(email_fn))







def main():
  parser = argparse.ArgumentParser(description="Extract data from emails and write \
      to file in data format")
  parser.add_argument("data_dir", action="store", help="The dir containing data")
  parser.add_argument("data_dir", action="store", help="The dir containing data")
  parser.add_argument("-O", "--OPT", action="", help="")
  result = parser.parse_args()


if __name__ == "__main__":
  main()
