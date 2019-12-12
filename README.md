# Address_Book_API
Coding Challenge Submission - Harrison Ratcliffe

## Table of Contents:
* [Description](#description)
* [Technologies](#technologies)
* [Setup and Installation](#setup-and-installation)
* [Usage](#usage)

## Description:
For this coding challenge, I implemented an Address Book API using the Python framework Flask, in conjunction with Elasticsearch. I also used HTTPie, a command line HTTP client for Python, which allowed me to send requests to the API. Per the requirements specified in the coding challenge, this API allows users to make HTTP requests in order to create, retrieve, update, or delete individual contacts in the address book, as well as retrieve multiple contacts at once based upon a query string. The API includes errors when contacts cannot be found or the information sent by the user cannot be interpreted by the API. Tests have also been included for the functions in the API, and the ports for Flask and Elasticsearch can be configured within the file Address_Book.py. I've included some installation steps below, feel free to reach out if you have any questions!
	
## Technologies:
Python packages and frameworks installed for this project:
* Python version: 3.7.4
* Flask version: 1.1.1
* elasticsearch version: 7.0.2
* httpie version: 1.0.2 (https://httpie.org/doc)

These are the main Python packages I used. A full list of dependencies can be found in requirments.txt. Please note that httpie is not included in requirements.txt since it is not required to run my code. I included it under technologies to show how I personally went about testing HTTP requests for the API. If you wish to install httpie, use ```pip install httpie```.

Other Technologies used:
* ElasticSearch version 7.3.0 (https://www.elastic.co/downloads/elasticsearch)

	
## Setup and Installation:
1. Download and install Python onto your machine (https://www.python.org/downloads/)
2. Download and install Elastic Search from their website (https://www.elastic.co/downloads/elasticsearch)
3. Clone or Download Repository from GitHub
4. Next, start an instance of Elastic Search: In a shell or terminal, navigate to where you saved Elastic Search and run the command
  ```
  bin\elasticsearch
  ```
5. In another a shell or terminal, navigate to the cloned/downloaded repository
6. Once there, run the following command to install the necessary Python dependencies from requirements.txt:
  ```
  pip install -r requirements.txt
  ```
7. Next, run the following commands to start the Address_Book.py Flask app:

  For Windows:
  ```
  set FLASK_APP=Address_Book.py
  flask run
  ```
  For MAC:
  ```
  export FLASK_APP=Address_Book.py
  flask run
  ```
8. Once both Address_Book.py and Elastic Search are running, you can send http requests to the API using the program of your choice. I ended up using httpie due to previous experience with it. The ports for Flask and Elasticsearch can be configured in Address_Book.py.

## Usage:
Below are the defined endpoints for interacting with the API, with basic descriptions and example usage:
 * GET path/contact?pageSize={}&page={}&query={}
   - Used to retrieve multiple contacts from the address book based on a query. `pageSize` is the number of contacts per page, `page` is the current results page, and `query` is the keyword or phrase to search for. 
   - EX: GET http://127.0.0.1:5000/contact?pageSize=10&page=1&query=Jim
   
 * POST path/contact?fullname={}&firstname={}&lastname={}&phone={}&email={}
   - Used to create a new Contact in the address book. `fullname` is a unique name assinged to the contact, `firstname` is the contacts firstname, `lastname` is the contacts lastname, `phone` is the contacts phone number, and `email` is the contacts email. address.
   - EX: POST http://127.0.0.1:5000/contact?fullname=JohnDoe&firstname=John&lastname=Doe&phone=3014445762&email=JohnDoe@example.com
 
 * GET path/contact/{fullname}
   - Retrieves the specified contacts information from the address book. `fullname` is the contacts unique name.
   - EX: GET http://127.0.0.1:5000/contact/John 
 
 * PUT path/contact/{fullname}?firstname={}&lastname={}&phone={}&email={}
   - Updates the contacts information with the values passed into the request. 
   - EX: PUT http://127.0.0.1:5000/contact/JohnDoe?firstname=John&lastname=Doe&phone=3014445799&email=JohnDoe@example.com
 
 * DELETE path/contact/{fullname}
   - Deletes the specified contact from the address book. `fullname` is the contacts unique name.
   - EX: POST http://127.0.0.1:5000/contact/John 
