#!/usr/bin/python

# email_parser.py
# Created on 2014-03-30.
# Email: disa@jhu.edu | lillaney@jhu.edu
# Copyright (c) 2014. All rights reserved.
"""
Example:
['Message-ID',
'Date',
'From',
'To',
'Subject',
'Cc',
'Mime-Version',
'Content-Type',
'Content-Transfer-Encoding',
'Bcc',
'X-From',
'X-To',
'X-cc',
'X-bcc',
'X-Folder',
'X-Origin',
'X-FileName']
"""
import email
import pdb

def get_date( msg ):
  """ Extracts date from the email and returns a String """
  return msg.get("Date")

def during_business():
  """ Return bool"""
  pass

def get_from( msg ):
  """ Extracts the "from" from the email as a String """
  return msg.get('From')

# I am yet to strip the string here of /r/n/t
def get_to( msg ):
  """ Extracts the "to" from the email as a String """
  return msg.get('To')

# Same as above
def get_cc( msg ):
  """ Extracts the "cc" from the email as List of Strings """
  return msg.get('Cc')

# Same problem
def get_bcc( msg ):
  """ Extracts the "bcc" from the email as a List of Strings """
  return msg.get('Bcc')

# This does not return the length of the attachment becuase our data does not have an attachment
def get_email_length( msg ):
  """ Extracts the email payload and returns the length of the payload """
  return len(msg.get_payload())

# I assume that this is to check the email contains an attachement or not
# But this does not work and I am trying to think of another way to figure that there is an attachment.
def get_in_( msg ):
  """ Retuns a true if there is an attachement and a false if there is none """
  return ( msg.has_key('X-FileName') )

# I think this becomes defunct given the disucssion we had.
def get_entry( msg ):
  """ Returns an entry of type <something> """
  
  pdb.set_trace()
  print get_from(msg)


def main():
  """ Test Function for this file. Grabs a random file and passes the contents to get_entry for test """
  
  # I am testing for two diffrent files here. Once which contains an attachment and the other does not.
  test1 = open("/home/klillan1/work/machine_learning/data/enron_mail_20110402/maildir/kean-s/transco/1.",'r')
  test2 = open("/home/klillan1/work/machine_learning/data/enron_mail_20110402/maildir/kitchen-l/inbox/50.", 'r')
  msg = email.message_from_file(test1)
  get_entry( msg )

if __name__ == "__main__":
  main()
