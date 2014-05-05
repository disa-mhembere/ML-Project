#!/usr/bin/python

# email_parser.py
# Created on 2014-03-30.
# Email: disa@jhu.edu | lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.

import email
import email.utils
import time
import pdb
import datetime
from math import log
from re import compile

ATTACHMENT_PATT = compile("See attached file")

def count_in( tempList, fromAddress ):
  """ Count the number of in network emails """
  count = 0
  # Checking for sender and receiver domain to be the same
  for x in tempList:

    if x.split('@')[1] == fromAddress.split('@')[1]:
      count+=1
  return count

def count_out( tempList ):
  """ Count the number of out network emails  """
  return None

def get_date( msg ):
  """ Extracts date from the email and returns a String """
  return datetime.datetime.fromtimestamp ( time.mktime( email.utils.parsedate( msg.get("Date") ) ) )

def get_week( msg ):
  """ Extracts week from the date and returns an Integer """
  return get_date(msg).isocalendar()[:2]

def during_business( msg ):
  """ Returns an Integer. 1 if during business and 0 if not"""
  return 1 if 8 < get_date( msg ).hour < 19 else 0

def on_weekday( msg ):
  """ Returns an Integer. 1 if on a weekday and 0 if not. """
  return 1 if get_date( msg ).isoweekday()<6 else 0

def get_from( msg ):
  """ Extracts the "from" from the email as a String """
  return msg.get('From')

def get_to( msg ):
  """ Extracts the "to" from the email as a String """
  if not msg['to']: return ( [ ], 0, 0 )

  toList =  [i.strip() for i in msg.get('To').split(',')]
  count = count_in(toList, msg['From'])
  return ( toList, count, len(toList) - count )

def get_cc( msg ):
  """ Extracts the "cc" from the email as List of Strings """
  if msg.has_key('Cc'):
    toList = [i.strip() for i in msg.get('Cc').split(',')]
    count = count_in(toList)
    return ( toList, count, len(toList) - count)
  else:
    return ( [ ], 0, 0)
def get_bcc( msg ):
  """ Extracts the "bcc" from the email as a List of Strings """
  if msg.has_key('Bcc'):
    toList = [i.strip() for i in msg.get('Bcc').split(',')]
    count = count_in(toList)
    return (toList, count, len(toList)-count)
  else: 
    return ([ ], 0, 0)

# This does not return the length of the attachment because our data does not have an attachment
def get_email_length( msg ):
  """ Extracts the email payload and returns the length of the payload """
  return log(len(msg.get_payload()))

# I assume that this is to check the email contains an attachement or not
# But this does not work and I am trying to think of another way to figure that if there is an attachment.
def get_in_( msg ):
  """ Retuns a true if there is an attachement and a false if there is none """
  return 0 if msg.has_key('X-FileName') else 0

def has_attachment( msg ):
  return len(ATTACHMENT_PATT.findall(msg.get_payload()))

def main():
  """ Test Function for this file. Grabs a random file and passes the contents to get_entry for test """
  
  # I am testing for two diffrent files here. Once which contains an attachment and the other does not.
  test1 = open("/home/klillan1/work/machine_learning/data/enron_mail_20110402/maildir/kean-s/transco/1.",'r')
  test2 = open("/home/klillan1/work/machine_learning/data/enron_mail_20110402/maildir/kitchen-l/inbox/50.", 'r')
  test3 = open('/home/klillan1/work/machine_learning/data/enron_mail_20110402/maildir/allen-p/discussion_threads/3.', 'r')
  pdb.set_trace()
  msg = email.message_from_file(test1)

if __name__ == "__main__":
  main()
