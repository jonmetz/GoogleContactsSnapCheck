#!/usr/bin/python
#
# Copyright (C) 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import getopt
import getpass
import atom
import gdata.contacts.data
import gdata.contacts.client
import MySQLdb

class GoogleContacts(object):
  """ContactsSample object demonstrates operations with the Contacts feed."""

  def __init__(self, email, password):
    """Constructor for the ContactsSample object.
    
    Takes an email and password corresponding to a gmail account to
    demonstrate the functionality of the Contacts feed.
    
    Args:
      email: [string] The e-mail address of the account to use for the sample.
      password: [string] The password corresponding to the account specified by
          the email parameter.
    
    Yields:
      A ContactsSample object used to run the sample demonstrating the
      functionality of the Contacts feed.
    """
    self.gd_client = gdata.contacts.client.ContactsClient(source='')
    self.gd_client.ClientLogin(email, password, self.gd_client.source)

  def GetContactsInfo(self, feed):
    for entry in feed.entry:
      if entry.name and entry.phone_number:
        yield (entry.name.full_name.text, [number.text for number in entry.phone_number])
    while feed:
      # Print contents of current feed
      for entry in feed.entry:
        if entry.name and entry.phone_number:
          yield (entry.name.full_name.text, [number.text for number in entry.phone_number])
      # Prepare for next feed iteration
      next = feed.GetNextLink()
      feed = None
      if next:
          # Another feed is available, and the user has given us permission
          # to fetch it
        feed = self.gd_client.GetContacts(uri=next.href)
        feed = self.gd_client.GetContacts(uri=next.href)

  def JoinNums(self, numbers):
    return ["".join(number) for number in numbers]
  
  def CleanPhoneNumbers(self, contacts):
    for contact in contacts:
      numbers = [list(number) for number in contact[1]]
      digits_only = [[char for char in number if char.isdigit()] for number in numbers]
      no_leading_1s = []
      for number in digits_only:
        if number and number[0] == "1":
          no_leading_1s.append(number[1:])
        else:
          no_leading_1s.append(number)
      cleaned_nums = [number[:8] + ["X", "X"] for number in no_leading_1s]        
      yield contact[0], ["".join(number) for number in cleaned_nums]      

  def ListAllContacts(self):
    """Retrieves a list of contacts and displays name and primary email."""
    feed = self.gd_client.GetContacts()
    self.contacts = self.CleanPhoneNumbers(self.GetContactsInfo(feed))
    return self.contacts

  def Run(self):
    """Prompts the user to choose funtionality to be demonstrated."""
    return self.ListAllContacts()

def get_contacts():
  """Demonstrates use of the Contacts extension using the ContactsSample object."""
  # Parse command line options
  try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['user=', 'pw='])
  except getopt.error, msg:
    print 'python contacts_example.py --user [username] --pw [password]'
    sys.exit(2)

  user = ''
  pw = ''
  # Process options
  for option, arg in opts:
    if option == '--user':
      user = arg
    elif option == '--pw':
      pw = arg

  while not user:
    print 'NOTE: Please run these tests only with a test account.'
    user = raw_input('Please enter your username: ')
  while not pw:
    pw = getpass.getpass()
    if not pw:
      print 'Password cannot be blank.'
  try:
    contacts = GoogleContacts(user, pw)
  except gdata.client.BadAuthentication:
    print 'Invalid user credentials given.'
    exit(1)
  contacts_list = contacts.Run()
  return contacts_list

def search_db(contacts):
  compromised = []
  db = MySQLdb.connect(host="localhost", # your host, usually localhost
                       user="snap", # your username
                       passwd="", # your password
                       db="snapchat") # name of the data base
  cursor = db.cursor()
  for contact in contacts:
    name = contact[0]
    if name in compromised:
      continue
    for number in contact[1]:
      db.query("""SELECT * from records where phone='%s';""" % number)
      matches = db.store_result()
      match = matches.fetch_row()
      if match:
        compromised.append(name.strip(' '))
        print "----------------"
      while match:
        print "Match Found for %s: Phone Number: %s username: %s" % (name, number, match[0][1])
        match = matches.fetch_row()
  print "The following contacts may have been compromised by the leak:" 
  for name in compromised: print name
  print "Total: %s" % len(compromised)

def main():
  contacts = get_contacts()
  search_db(contacts)


if __name__ == '__main__':
  main()
  

