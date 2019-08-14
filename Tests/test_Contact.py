'''Testing for methods in Contact.py

This file contains unit tests for the methods in Contact.py
This file can be run independently from Address_Book.py and Elastic Search instances

'''

import unittest
import json
import sys
sys.path.append('..')

from API_Files.contact import toJSON, updateJSON, formatPhone, formatEmail

class TestContactMethods(unittest.TestCase):
  def test_to_json(self):
    '''Test if toJSON properly puts inputted values into JSON format'''
    fullname = "John Doe"
    firstname = "John"
    lastname = "Doe"
    phone = "3015558899"
    email = "JohnDoe@gmail.com"

    test_json = json.dumps({'fullname': 'John Doe', 'firstname': 'John', 'lastname': 'Doe', 'phone': '3015558899', 'email': 'JohnDoe@gmail.com'})
    result_json = toJSON(fullname, firstname, lastname, phone, email)
    self.assertEqual(result_json, test_json)

  def test_update_json(self):
    '''Test if updateJSON properly updates and returns the contacts JSON'''
    u_firstname = "Johnathon"
    u_phone = "5557569967"
    u_email = "JDoe@gmail.com"

    original_json = {'fullname': 'John Doe', 'firstname': 'John', 'lastname': 'Doe', 'phone': '3015558899', 'email': 'JohnDoe@gmail.com'}
    test_update_json = json.dumps({'fullname': 'John Doe', 'firstname': 'Johnathon', 'lastname': 'Doe', 'phone': '5557569967', 'email': 'JDoe@gmail.com'})
    result_json = updateJSON(original_json, {'firstname': u_firstname, 'phone': u_phone, 'email': u_email})
    self.assertEqual(result_json, test_update_json)

  def test_phone_formatting(self):
    '''Test if formatPhone correctly checks formatting'''
    # Using a correctly formatted phone number
    self.assertTrue(formatPhone("2408765687"))
    # Using a phone number that is too short
    self.assertFalse(formatPhone("2408765"))
    # Using a phone number that is too long
    self.assertFalse(formatPhone("24087656872345"))
    # Using a phone numbe that contains non-digit characters
    self.assertFalse(formatPhone("1245t8r3h2"))

  def test_email_format(self):
    '''Test if formatEmail correctly validates email formatting'''
    # Using a two correctly formatted emails
    self.assertTrue(formatEmail("example@example.com"))
    self.assertTrue(formatEmail("temp.email@gmail.org"))
    # Using a two incorrectly formatted emails
    self.assertFalse(formatEmail("bademail.com"))
    self.assertFalse(formatEmail("alsobad@email"))

if __name__=='__main__':
  unittest.main()
