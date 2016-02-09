# -*- coding: utf-8 -*-

'''

Open Weather Api is a json weather api to get weather data for most major cities.

In this exercise we are going to populate a small local database with all the min and max temperatures for last 16 days for a city.

We will use a json api to get the data, then store parts of that data in sqlite, which is small sql database.

Steps:

1) First inspect what is returned in json_data. You can use python print statements also download and use the chrome json formatter: https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=en 

2) The data returned has a key "list" which is an array of hashes (horray!). Each element in the array is one day's temp info.

3) Write a loop to print out each days "min" and "max" temp as well as the "dt" key. dt is short for datetime.
			for item in data:
			print "the min and max temperatures for that unixe date %d is :" % (item['dt'])
			print "min: ",item['temp']['min']
			print "max",item['temp']['max']

each item in data is a day
in each day/item is a dictionary, and item[key=temp] shows various temperature for that day

for item in data:
	print item['temp']
DB)

4) Create a table to store this information. The table should be able to store

- id sql field type - INTEGER PRIMARY KEY
- city_name  sql field type - text
- datetime (dt) sql field type - text
- min_temp  sql field type - real
- max_temp  sql field type- real

5) Refactor your loop so that instead of just printing it inserts new rows for each day into the table.

6) Write queries to find the day with lowest temperature and the highest.

7) Write a query to find the average temp.

Extension:

Expand the code to be able to ask a user for a city, then populate the db with that cities data. 
Then allow the user to find maxes for one city or across all cities.


Further Reading:

http://zetcode.com/db/sqlitepythontutorial/

'''
import sys
import requests
import sqlite3
connection_object=None
city=""

def get_city_name_and_organise_the_required_data():
	a=raw_input("input your city here")
	city=a.lower()
	url = "http://api.openweathermap.org/data/2.5/forecast/daily?mode=json&units=metric&q="+city+"&cnt=16&appid=44db6a862fba0b067b1930da0d769e98"
	json_data = requests.get(url).json()
	data=json_data['list']
	#city_data=json_data['city']['name']
	return (city,a,json_data,data)

def connect_to_db(city): 
	filename_with_city_name = city + '.sqlite'
	connection_object =sqlite3.connect(filename_with_city_name)
	return connection_object

def create_temperatures_table(connection_object):
	cursor = connection_object.cursor()
	#cursor.execute("DROP TABLE IF EXISTS temperatures")
	cursor.execute('''CREATE TABLE IF NOT EXISTS temperatures (id INTEGER PRIMARY KEY, dt DATE, min REAL,max REAL)''')
	connection_object.commit()

def populate_temperatures(connection_object,data):
	'''still using the cursor to execute changes'''
	cursor = connection_object.cursor()
	print data
	for item in data:
		print item
		#item['dt']
		cursor.execute('''INSERT INTO temperatures (dt,min,max) VALUES (?,?,?)''', (item['dt'],item['temp']['min'],item['temp']['max']))
	connection_object.commit()

def traverse_temperatures(connection_object):
	cursor = connection_object.cursor()
	cursor.execute('''select * from temperatures''')
	print cursor.fetchall()
	return cursor.fetchall()
	
def close_connection(connection_object):
	connection_object.close()

def main():
	city,a,json_data,data= get_city_name_and_organise_the_required_data()
	c=connect_to_db(city)
	create_temperatures_table(c)
	populate_temperatures(c,data)
	traverse_temperatures(c)
	close_connection(c)

main()

#print json_data


	



