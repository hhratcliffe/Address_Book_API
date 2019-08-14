'''Testing for API methods

This file contains the tests for creating, retieving, updating, and deleting contacts in Elastic Search
Tests are executed sequentially to simulate usage of Elastic search
The tests do not interact with the REST API defined in Address_Book.py

When running this file, make sure an instance of Elastic Search is running and configure to the desired port

'''

import unittest
import json
from elasticsearch import Elasticsearch
import sys
sys.path.append('..')
from API_Files import api_methods

es  = Elasticsearch([{'host': 'localhost', 'port':9200}])

class TestElasticMethods(unittest.TestCase):
  def test_add_contact(self):
    '''Test that a contact can be correctly stored'''
    fullname = 'Tom Smith'
    firstname = 'Tom'
    lastname = 'Smith'
    phone = '3014535496'
    email = 'TomSmith@example.com'
    result = api_methods.createContact(fullname, firstname, lastname, phone, email, es)
    self.assertEqual(result, 'Contact for '+fullname+' has been successfully created.')

  def test_get_contact(self):
    '''Test getting a stored contact'''
    fullname = "Tom Smith"
    test_json = json.dumps({'fullname': 'Tom Smith', 'firstname': 'Tom', 'lastname': 'Smith', 'phone': '4435567789', 'email': 'TomSmith2@example.com'})
    result = json.dumps(api_methods.getContact(fullname, es))
    self.assertEqual(result, test_json)

  def test_change_contact(self):
    '''Test updating a stored contact'''
    fullname = 'Tom Smith'
    firstname = 'Tom'
    lastname = 'Smith'
    phone = "4435567789"
    email = "TomSmith2@example.com"
    test_json = json.dumps({'fullname': 'Tom Smith', 'firstname': 'Tom', 'lastname': 'Smith', 'phone': '4435567789', 'email': 'TomSmith2@example.com'})
    result = api_methods.updateContact(fullname, firstname, lastname, phone, email, es)
    self.assertEqual(result, "Contact "+fullname+" has been successfully updated.")
    result_json = json.dumps(es.get(index="addressbook", doc_type="contact", id=fullname)["_source"])
    self.assertEqual(result_json, test_json)

  def test_remove_contact(self):
    '''Test deleting a stored contact'''
    fullname = 'Tom Smith'
    result = api_methods.deleteContact(fullname, es)
    self.assertEqual(result, "Contact information for "+fullname+" has successfully been deleted.")

if __name__ == '__main__':
  unittest.main()
