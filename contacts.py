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

  def ListAllContacts(self):
    """Retrieves a list of contacts and displays name and primary email."""
    feed = self.gd_client.GetContacts()
    self.contacts= self.GetContactsInfo(feed)
    return self.contacts   

  def Run(self):
    """Prompts the user to choose funtionality to be demonstrated."""
    return self.ListAllContacts()

def main():
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
    return

  contacts_list = contacts.Run()
  return contacts_list

if __name__ == '__main__':
  main()
