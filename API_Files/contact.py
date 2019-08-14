"""Contact Specification and Methods

This file contains the data model definiton for methods for the JSON Contact objects stored using Elastic Search
as well as the methods used to alter them

Each Contact stored in ElasticSearch is given a unique fullname, an optional first name, an optional last name, a phone number, and an email
The JSON structure for a Contact is as follows:
Contact = {
  'fullname': fullname,
  'firstname': firstname,
  'lastname': lastname,
  'phone': phone,
  'email': email
}

Contact Attributes:
  fullname: str
    A Unique Name for the contact. Cannot be shared with any other contacts.

  firstname: str
    The first name for the contact. A contacts first name defaults to an empty string unless provided and is not required for contacts.

  lastname: str
    The last name for the contact. Like firstname, it defaults to an empty string unless provided and is not required for contacts.

  phone: str
    A phone number for the contact. The phone number must be 10 digits long, and can only be numbers.
    Other characters or symbols will throw an error. Required for each contact.

  email: str
    An email address for the contact. Email address must follow the formatting "example@example.com".
    Other formats will throw an error. Required for each contact.
"""

import json
import re

def toJSON(fullname, firstname, lastname, phone, email):
  """
  Formats the contacts inputted information into JSON to be stored in Elasticsearch

  Parameters
  ----------
  fullname: str
    Unique name for the new contact. Contacts full name
  firstname: str
    Contacts first name, does not have to be unique
  lastname: str
   Contacts last name, does not have to be unique
  phone: str
    Phone number for the new contact
  email: str
    Email address for the new contact

  Returns
  -------
  dict
    python dictionary of data formatted into JSON

  """

  data = {
    'fullname': fullname,
    'firstname': firstname,
    'lastname': lastname,
    'phone': phone,
    'email': email
  }
  return json.dumps(data)

def updateJSON(data, updates):
  """
  Takes in JSON from Elasticsearch as a dictionary, updates it with the specified changes, and returns it
  If empty values are present in updates, they will not be updated

  Parameters
  ----------
  data: dict
    Original JSON retrieved from ElasticSearch
  updates: dict
    Dictionary of updated values

  Returns
  -------
  dict
    python dictionary of data formatted into JSON
  """
  for key,value in updates.items():
    if value is not '':
      data[key] = value

  return json.dumps(data)

def formatPhone(phone):
  """
  Takes in a phone number and validates it againsts defined constraints

  Parameters
  ----------
  phone: str
    The phone number for a contact

  Returns
  -------
  bool
    boolean value of true if formatted correctly, false if not.
  """
  # Check phone number length
  if len(phone) != 10:
    return False
  # Check if the phone number contains only digits
  if phone.isdigit() == False:
    return False

  return True

def formatEmail(email):
  """
  Takes in an email address and validates it againsts defined formatting constraints

  Parameters
  ----------
  email: str
    The email address for a contact

  Returns
  -------
  bool
    boolean value of true if formatted correctly, false if not.
  """
  email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
  if re.search(email_regex, email):
    return True
  return False
