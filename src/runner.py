#!/usr/bin/python

# runner.py
# Created by Disa Mhembere on 2014-03-30.
# Email: disa@jhu.edu
# Copyright (c) 2014. All rights reserved.

# This will run the email the parser and feature writer
"""
Key:
  - _in : in network
  - _outn : out of network
  - _dbh : during business hours
  - _abh : aftere business hours

Feature vector order:
  [to_email_in,  from_email_in, cc_to_email_in, bcc_to_email_in, mean_email_len_in, 
  to_email_outn,  from_email_outn, cc_to_email_outn, bcc_to_email_outn, mean_email_len_outn,
  num_attachments, on_weekend, on_weekday, num_emails_dbh, num_emails_abh, indegree, 
  outdegree, scan1, triangle, transitivity, normed_eigenvalue
  ]
"""
import argparse
import os
from email_parser import *
import email
from structs.time_series_fv import tsfv
from utils.names_to_ids import People
from glob import glob

people = None
tsfv_obj = None

def run(data_dir, names_fn, save_fn, NUM_FEATURES):
  """ 
  Given a directory of emails lets get all features and build a 
  data structures with these features and graph statistics.

  @param data_dir: is the directory with all email mailboxes
  @param names_fn: the file containing the names to email address mapping
  @param save_fn: the file name to save pickle dump after
  """

  global people, tsfv_obj

  people = People(names_fn)
  NUM_FEATURES = 20

  tsfv_obj = tsfv(NUM_FEATURES)

  for people_dir in glob(os.path.join(data_dir,"*")): # Names of employees
    print "Processing employee ' %s' ..." % people_dir
    
    emails = [] # all emails
    # accumulate all emails filenames
    for root, dirnames, filenames in os.walk(people_dir):
      for filename in filenames:
        full_fn = os.path.join(root, filename)
        print "Processing file %s" % (full_fn)
        if os.path.isfile(full_fn) and (not os.path.basename(full_fn).startswith(".")): emails.append(full_fn)

    for email_fn in emails:
      entry = email.message_from_file(open(email_fn))
      ingest_email(entry)
  
  tsfv_obj.finish()
  #print tsfv_obj
  print "Mission complete!"
  tsfv_obj.save(save_fn)

  people.to_file("all_emailed.txt")

def ingest_email(entry):
  global people, tsfv_obj

  # This is a single email
  week = get_week(entry) # 2-tuple
  to, to_email_in, to_email_outn = get_to(entry) # list of people whom this is sent to 

  if (to):
    cc, cc_to_email_in, cc_to_email_outn = get_cc(entry) # list of people who are cc'd
    bcc, bcc_to_email_in, bcc_to_email_outn = get_bcc(entry) # bcc'd
    _from = get_from(entry)
    _id = people.get_id(_from)
    weekday = on_weekday(entry)
    
    # Update for a single mail
    tsfv_obj.insert_email(week, _id, to_email_in, to_email_outn, cc_to_email_in, 
        cc_to_email_outn, bcc_to_email_in, bcc_to_email_outn, during_business(entry), 
        weekday, get_email_length(entry), has_attachment(entry))
    
    sender_domain = _from.split("@")[-1]
    # Update cc-ers
    for recepient in to:
      is_in_network = recepient.split("@")[-1] == sender_domain
      tsfv_obj.update_cc(week, people.get_id(recepient), is_in_network)

    for recepient in cc:
      is_in_network = recepient.split("@")[-1] == sender_domain
      tsfv_obj.update_cc(week, people.get_id(recepient), is_in_network)

    for recepient in bcc:
      is_in_network = recepient.split("@")[-1] == sender_domain
      tsfv_obj.update_bcc(week, people.get_id(recepient), is_in_network)


def main():
  parser = argparse.ArgumentParser(description="Extract data from emails and write \
      to file in data format")
  parser.add_argument("data_dir", action="store", help="The dir containing data")
  parser.add_argument("names_fn", action="store", help="The file with mapping from email \
      to name data")
  parser.add_argument("-s", "--save_fn", action="store", default="tsfv.cPickle", help="Save filename")
  parser.add_argument("-n", "--num_features", action="store", type=int, default=20, help="Save filename")
  result = parser.parse_args()
  
  run(result.data_dir, result.names_fn, result.save_fn, result.num_features)

if __name__ == "__main__":
  main()
