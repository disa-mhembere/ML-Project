#!/usr/bin/python

# runner.py
# Created by Disa Mhembere on 2014-03-30.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

# This will run the email the parser and feature writer
"""
Key:
  - _in : in network
  - _out : outn of network
  - _dbh : during business hours
  - _abh : aftere business hours

Feature vector order:
  [to_email_in,  from_email_in, cc_to_email_in, bcc_to_email_in, mean_email_len_in, 
  to_email_outn,  from_email_out, cc_to_email_out, bcc_to_email_out, mean_email_len_out,
  num_attachments, on_weekend, on_weekday, num_emails_dbh, num_emails_abh, degree, 
  scan1, triangle, transitivity, normed_eigenvalue
  ]


"""
import argparse
import os
from email_parser import *
import email
from structs.time_series_fv import tsfv
from utils.names_to_ids import People

def run(data_dir, names_fn):
  """ 
  Given a directory of emails lets get all features and build a 
  data structures with these features and graph statistics.

  @param data_dir: is the directory with all email mailboxes
  @param names_fn: the file containing the names to email address mapping
  """
  names_dict = People(names_fn)
  WEEKS = 189
  NUM_FEATURES = 20

  tsfv_obj = tsfv(NUM_FEATURES, WEEKS)

  for people_dir in os.listdir(data_dir): # Names of employees
    for email_cat in os.listdir(people_dir): # e.g Cat = category sent, inbox
      for email_fn in os.listdir(email_cat):

        entry = email.message_from_file(open(email_fn))
        # This is a single email
        _week = get_week(entry)
        assert _week > 0 and _week <= WEEKS, "Week specified out of range of WEEKS = %d" % WEEKS
        _to = get_to(entry)
        _from =

        fv = [get()] # featurevectors









def main():
  parser = argparse.ArgumentParser(description="Extract data from emails and write \
      to file in data format")
  parser.add_argument("data_dir", action="store", help="The dir containing data")
  parser.add_argument("data_dir", action="store", help="The dir containing data")
  parser.add_argument("-O", "--OPT", action="", help="")
  result = parser.parse_args()


if __name__ == "__main__":
  main()
