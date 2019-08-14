'''API Methods

This file contains the API methods used to retieve, create, update, and delete contact objects stored in Elastic Search.
The methods in this file allow users to get all contacts, create new contacts with the specified attributes/values,
update an existing contact, get a single contacts information, or delete a contact.

'''

from API_Files.api_errors import bad_request, error_response
from API_Files import contact

def getAllContacts(page_size, page, query, es_object):
  """
  Retrieve multiple Contact from the AddressBook

  Takes in the number of results to display per page, the specified page to view, and the resulting retrieved contacts based on the provided query

  Parameters
  ----------
  page_size: int
    Number of contacts to display per page
  page: int
    Results page number to be viewed
  query: str
    keyword or phrase to search through the contacts for. If left empty, defaults to displaying all contacts.

  Returns
  -------
  list
    Returns a list of all query results on the specified page
  """
  results = es_object.search(index='addressbook', body=
    {'from': page, 'size': page_size, "query": {"query_string": {'default_field': '*', 'query': query}}})

  return results['hits']


def createContact(fullname, firstname, lastname, phone, email, es_object):
  """
  Creates a new Contact in the AddressBook

  Performs checks on fullname, phone, and email to ensure the parameters were entered correctly, validates
  that the specified fullname is unique, and creates the JSON formatted contact in Elasticsearch

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
  es_object: Elasticsearch instance
    Current Elasticsearch instance

  Raises
  ------
  400 Bad Request Error
    If user does not provide values for fullname, phone, or email
    If inputted fullname is not unique

  Returns
  -------
  str
    Returns a string telling the user that the Contact has been created
  """
  # Check that name, phone, and email are not empty
  if not fullname:
    return bad_request("Please provide a unique name for the new Contact.")
  if not phone:
    return bad_request("Please provide a phone number for the new Contact.")
  if not email:
    return bad_request("Please provide an email for the new Contact.")

  # Validate whether name is unique
  search = es_object.search(index='addressbook', body={'query': {'match_phrase': {'fullname':fullname}}})
  if search["hits"]["total"]["value"]>0:
    return bad_request("Name "+fullname+" is not unique. Please enter a unique name.")

  # Check that the phone number and email are properly formatted
  if not contact.formatPhone(phone):
    return "Phone number not properly formatted. Ensure that the entered phone number contains only numbers and is 10 digits long"
  if not contact.formatEmail(email):
    return "Email address not properly formatted. Ensure the entered email follows the format: example@email.com"

  contact_json = contact.toJSON(fullname, firstname, lastname, phone, email) # return contacts data in JSON format
  es_object.index(index='addressbook', doc_type='contact', id=fullname, body=contact_json)
  return 'Contact for '+fullname+' has been successfully created.'


def updateContact(fullname, firstname, lastname, phone, email, es_object):
  """
  Updates an existing Contact in the AddressBook

  Takes in the fullname of the contact to be updated, a firstname, a lastname, a phone number, and an email address. If the firstname, lastname, phone number, and email address are
  not provided by the user, then they default to empty strings. Retrieves the original JSON from Elasticsearch, changes the necessary values,
  then updates the JSON stored in Elasticsearch

  Parameters
  ----------
  fullname: str
    Name of the contact to be updated
  firstname: str
    New first for the contact (default is an empty string)
  lastname: str
    New lastname for the contact (default is an empty string)
  phone: str
    New phone number for the contact (default is an empty string)
  email: str
    New email address for the contact (default is an empty string)
  es_object: Elasticsearch instance
    Current Elasticsearch instance

  Raises
  ------
  400 Bad Request Error
    If contact cannot be found (fullname does not exist)
    If user provides a phone number or email address already in use by another contact

  Returns
  -------
  str
    Returns a string telling the user that the Contact has been updated
  """
  # Check if specified contact exists
  try:
    current_json = es_object.get(index='addressbook', doc_type='contact', id=fullname)['_source']
  except:
    return bad_request("Could not find contact with the name "+fullname+". Please check that the name is correct, or enter a different name.")

  # Check if inputted phone number is already in use
  if phone and phone != current_json['phone'] and es_object.search(index='addressbook', body={'query': {'match_phrase': {"phone":phone}}})['hits']['total']['value']>0:
    return bad_request("Entered phone number is already in use. Please enter a different phone number")
  # Check if inputted email address is already in use
  if email and email != current_json['email'] and es_object.search(index='addressbook', body={'query': {'match_phrase': {"email":email}}})['hits']['total']['value']>0:
    return bad_request("Entered email address is already in use. Please enter a different email address")

  updates = {'firstname': firstname, 'lastname': lastname, 'phone': phone, 'email': email}
  contact_json = contact.updateJSON(current_json, updates)

  # For elasticsearch in python, the function index() is used to both create new data entries and update existing ones
  es_object.index(index='addressbook', doc_type='contact', id=fullname, body=contact_json)

  return "Contact "+fullname+" has been successfully updated."


def deleteContact(fullname, es_object):
  """
  Delete a Contact from the AddressBook

  Takes in the fullname of the contact to be deleted and returns an error if the contact cannot be found.
  Notifies the user if the the deletion was successful or not.

  Parameters
  ----------
  fullname: str
    Unique fullname of the contact to be deleted
  es_object: Elasticsearch instance
    Current Elasticsearch instance

  Raises
  ------
  400 Bad Request Error
    If contact cannot be found (fullname does not exist)

  Returns
  -------
  str
    Returns a string telling the user that the Contact has been deleted
    or returns a string telling the user that the Contact failed to be deleted
  """

  try:
    res = es_object.delete(index="addressbook", doc_type="contact", id=fullname)
  except:
    return bad_request("Could not find contact with the name "+fullname+". Please check that the name is correct, or enter a different name.")

  # Check to ensure that the contact was properly deleted
  if res['result'] == 'deleted':
    return "Contact information for "+fullname+" has successfully been deleted."
  else:
    return "Error: The contact "+fullname+" could not be deleted."


def getContact(fullname, es_object):
  """
  Retrieve a Contact from the AddressBook

  Takes in the fullname of the contact to be retrieved, gets the contacts information from Elasticsearch and returns it

  Parameters
  ----------
  fullname: str
    Unique fullname of the contact to be deleted
  es_object: Elasticsearch instance
    Current Elasticsearch instance

  Raises
  ------
  400 Bad Request Error
    If contact cannot be found (fullname does not exist)

  Returns
  -------
  str
    Returns the specified contacts information in JSON format
  """
  try:
    return es_object.get(index='addressbook', doc_type='contact', id=fullname)['_source']
  except:
    return bad_request("Could not find contact with the name "+fullname+". Please check that the name is correct, or enter a different name.")
