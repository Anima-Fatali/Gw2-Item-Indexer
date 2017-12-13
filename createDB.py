import time
import csv
import requests

import sqlite3
from sqlite3 import *

try:
	import json
except ImportError:
	import simplejson as json

start = time.time()

def createItemCSV():
        
        array = requests.get('https://api.guildwars2.com/v2/items').json()

        length = len(array)

        j = 0
        csvfile = open("itemDB.csv", 'w', newline = '')
        f = csv.writer(csvfile)
        while j < (length):
            x = 0
            request_string = 'https://api.guildwars2.com/v2/items?ids='
            while x < 200 and j < (length):
                request_string += str(array[j])
                if x != 199:
                    request_string += ','
                j += 1
                x += 1
            id1 = requests.get(request_string).json()
            if id1:
                for i in id1:
                        f.writerow([i['name'],i['id'],i['type'],i['level'],
                                i['rarity'],i['vendor_value'],i['chat_link'],
                                i['icon']])

        csvfile.close()

def createRecipeCSV():
        array = requests.get('https://api.guildwars2.com/v2/recipes').json()

        length = len(array)

        j = 0
        csvfile = open("recipeDB.csv", 'w', newline = '')
        f = csv.writer(csvfile)
        while j < (length):
            x = 0
            request_string = 'https://api.guildwars2.com/v2/recipes?ids='
            while x < 200 and j < (length):
                request_string += str(array[j])
                if x != 199:
                    request_string += ','
                j += 1
                x += 1
            id1 = requests.get(request_string).json()
            if id1:
               for i in id1:
                   f.writerow([i['id'],i['output_item_id']])
        csvfile.close()

def createDB():
        try:
            conn = sqlite3.connect('./itemIndex.db')
        except Error as e:
            print(e)


        cur = conn.cursor()
        try:
                cur.execute('create table itemIndex(name text, itemID integer primary key, type text, level integer, rarity text, vendor_value integer, chat_link text, icon text);')
                cur.execute('create table recipeIndex(recipeID integer primary key, itemID integer, foreign key(itemID) references itemIndex(itemID));')
                        
        except Error as e:
                print(e)

        #Add data to the itemIndex table
        readfile = open('itemDB.csv')
        csvReader = csv.reader(readfile)

        for row in csvReader:
            cur.execute('insert into itemIndex (name, itemID, type, level, rarity, vendor_value, chat_link, icon) values (?, ?, ?, ?, ?, ?, ?, ?);', row)

        readfile.close()

        #Add data to the recipeIndex table
        readfile = open('recipeDB.csv')
        csvReader = csv.reader(readfile)

        for row in csvReader:
            cur.execute('insert into recipeIndex (recipeID, itemID) values (?, ?);', row)

        readfile.close()

        conn.commit()


createItemCSV()
createRecipeCSV()
createDB()

end = time.time()

print(end-start)
