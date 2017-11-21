import urllib.request
import time
import csv
import sqlite3
from sqlite3 import *

try:
	import json
except ImportError:
	import simplejson as json

start = time.time()
	
def request(api_path):
	url = 'https://api.guildwars2.com/v2/' + api_path
	try:
		temp = urllib.request.urlopen(url).read().decode('utf-8')
		return json.loads(temp)
	except:
		pass

array = request('recipes')

length = len(array)

j = 0
csvfile = open("recipe.csv", 'w', newline = '')
f = csv.writer(csvfile)
while j < (length):
    x = 0
    request_string = 'recipes?ids='
    while x < 200 and j < (length):
        request_string += str(array[j])
        if x != 199:
            request_string += ','
        j += 1
        x += 1
    id1 = request(request_string)
    if id1:
       for i in id1:
           test = (i['ingredients'])
           f.writerow([i['id'],i['output_item_id']])
csvfile.close()

try:
    conn = sqlite3.connect('./itemIndex.db')
except Error as e:
    print(e)

cur = conn.cursor()
#cur.execute('create table recipeIndex(recipeID integer primary key, itemID integer);')

readfile = open('recipe.csv')
csvReader = csv.reader(readfile)

for row in csvReader:
    cur.execute('insert into recipeIndex (recipeID, itemID) values (?, ?);', row)

readfile.close()

conn.commit()

end = time.time()

print(end-start)

cursor = cur.execute('select * from recipeIndex')
