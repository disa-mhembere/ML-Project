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
  [to_email_in,  from_email_in, cc_to_email_in, bcc_to_email_in, mean_email_len,
  to_email_outn,  from_email_outn, cc_to_email_outn, bcc_to_email_outn,
  num_attachments, to_on_weekend, to_on_weekday, to_num_emails_dbh, to_num_emails_abh, 
  from_num_emails_dhb, from_num_emails_abh, from_on_weekend, from_on_weekday, indegree,
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
  NUM_FEATURES = 24

  tsfv_obj = tsfv(NUM_FEATURES)

  for people_dir in glob(os.path.join(data_dir,"*")): # Names of employees
    print "Processing employee ' %s' ..." % os.path.basename(people_dir)
    
    emails = [] # all emails
    # accumulate all emails filenames
    for root, dirnames, filenames in os.walk(people_dir):
      for filename in filenames:
        full_fn = os.path.join(root, filename)
        if os.path.isfile(full_fn) and (not os.path.basename(full_fn).startswith(".")): emails.append(full_fn)

    for email_fn in emails:
      print "Processing file %s ..." % (email_fn)
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

  if to: # ignore auto-generated emails to the user
    cc, cc_to_email_in, cc_to_email_outn = get_cc(entry) # list of people who are cc'd
    bcc, bcc_to_email_in, bcc_to_email_outn = get_bcc(entry) # bcc'd
    _from = get_from(entry)

    _id = people.get_id(_from)
    weekday = on_weekday(entry) # Number sent out on weekday (+ve)/weekend (-ve)
    dbh = during_business(entry) # Number sent during(+ve)/after(-ve) business hours
    
    # Update for a single mail
    tsfv_obj.insert_email(week, _id, to_email_in, to_email_outn, cc_to_email_in, 
        cc_to_email_outn, bcc_to_email_in, bcc_to_email_outn, dbh, 
        weekday, get_email_length(entry), has_attachment(entry))
    
    sender_domain = _from.split("@")[-1]

    # Update to, cc, bcc
    for recepient in to:
      is_in_network = recepient.split("@")[-1] == sender_domain
      tsfv_obj.update_to(week, people.get_id(recepient), is_in_network, weekday > 0, dbh > 0,)

    for recepient in cc:
      is_in_network = recepient.split("@")[-1] == sender_domain
      tsfv_obj.update_cc(week, people.get_id(recepient), is_in_network, weekday > 0, dbh > 0)

    for recepient in bcc:
      is_in_network = recepient.split("@")[-1] == sender_domain
      tsfv_obj.update_bcc(week, people.get_id(recepient), is_in_network, weekday > 0, dbh > 0)

def main():
  parser = argparse.ArgumentParser(description="Extract data from emails and write \
      to file in data format")
  parser.add_argument("data_dir", action="store", help="The dir containing the email raw data")
  parser.add_argument("names_fn", action="store", help="The file with mapping from email \
      to name data")
  parser.add_argument("-s", "--save_fn", action="store", default="tsfv.cPickle", help="Save file name for cPickle dump of tsfv object")
  parser.add_argument("-n", "--num_features", action="store", type=int, default=20, help="Save filename")
  result = parser.parse_args()
  
  run(result.data_dir, result.names_fn, result.save_fn, result.num_features)

if __name__ == "__main__":
  main()
