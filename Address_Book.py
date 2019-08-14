'''Address Book Flask Application

This file creates the Address Book flask instance, allowing users to make HTTP requests to the specified path
in order to interact with the API.

'''

from datetime import datetime
from flask import Flask, request
from elasticsearch import Elasticsearch
from API_Files import api_methods

# Configure the following ports to desired Elasticsearch port and Flask port.
# Defaul Elastic Search port is 9200
elastic_port = 9200
# Default flask port is 5000
flask_port = 5000

# Connect to Elasticsearch cluster
es = Elasticsearch([{'host': 'localhost', 'port':elastic_port}])
# To check connection to elasticsearch, use es.ping()

app = Flask(__name__)

# Endpoint for getting a list of all contacts and additional queries
@app.route('/contact', methods=['GET', 'POST'])
def getContacts():
  # HTTP GET call should be formatted as: GET {path}/contact?pageSize={}&page={}&query={}
  if request.method == 'GET':
    page_size = min(request.args.get('pageSize', 10, type=int), 30)
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '*')
    return api_methods.getAllContacts(page_size, page, query, es)

  # Endpoint for creating new contacts
  # HTTP POST call should be formatted as: POST {path}/contact?fullname={}&firstname={}&lastname={}&phone={}&email={}
  elif request.method== 'POST':
    fullname = request.args.get('fullname', '') # get entered name from request
    firstname = request.args.get('firstname', '') # get entered firstname from request
    lastname = request.args.get('lastname', '') # get entered lastname from request
    phone = request.args.get('phone', '') # get entered phone number from request
    email = request.args.get('email', '') # get entered email from request

    return api_methods.createContact(fullname, firstname, lastname, phone, email, es)


# Endpoints for updating, deleting, or retrieving a single contact
@app.route('/contact/<contact_name>', methods=['GET', 'PUT', 'DELETE'])
def changeContact(contact_name):
  # Update specified contacted with inputted parameters
  # HTTP PUT call should be formatted as: PUT {path}/contact/<contact_name>?phone=''&email=''
  if request.method == 'PUT':
    firstname = request.args.get('firstname', '') # get entered firstname from request
    lastname = request.args.get('lastname', '') # get entered lastname from request
    phone = request.args.get('phone', '') # get entered phone number from request
    email = request.args.get('email', '') # get entered email from request

    return api_methods.updateContact(contact_name, firstname, lastname, phone, email, es)

  # Delete specified contact based on inputted name
  # HTTP DELETE call should be formatted as: DELETE {path}/contact/<contact_name>
  elif request.method == 'DELETE':
    return api_methods.deleteContact(contact_name, es)

  # Get the specified contact based on name and return the formatted json
  # HTTP GET call should be formatted as: GET {path}/contact/<contact_name>
  elif request.method == 'GET':
    return api_methods.getContact(contact_name, es)

if __name__ == "__main__":
  # Default port for Flask is 5000. To change the port, use app.run(port={port}), substituing in your desired port for {port}
  app.run(port=flask_port)
