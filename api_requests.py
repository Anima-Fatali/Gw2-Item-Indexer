try:
	import json
except ImportError:
	import simplejson as json

import sqlite3
from sqlite3 import *
import urllib.request
import csv
import os

import requests

global API_KEY
global count
count = 0
def isApiActive():
        try:
                url = 'https://api.guildwars2.com/v2'
                response = urllib.request.urlopen(url)
                status = response.getcode()
                return True
        except urllib.error.HTTPError as e:
                print(e)
                return False

def setApiKey(apikey):
        global API_KEY
        API_KEY = apikey

def getApiKey():
        global API_KEY
        print(API_KEY)
        return API_KEY

def searchAccount(item_id):
    global API_KEY
    global count

    if(os.path.isfile('./temp.csv') is False):
        csvfile = open('temp.csv', 'w', newline = '')
        f = csv.writer(csvfile)        
        searchCharacters(f)
        searchBank(f)
        csvfile.close()
        try:
            conn = sqlite3.connect('./temp.db')
            conn.row_factory = lambda cursor, row: row[0]

        except Error as e:
            print(e)
            
        cur = conn.cursor()

        cur.execute('create table temp(itemID integer, count integer);')

        readfile = open('temp.csv')
        csvReader = csv.reader(readfile)

        for row in csvReader:
            cur.execute('insert into temp (itemID, count) values (?, ?);', row)

        readfile.close()

        conn.commit()

    else:
        try:
            conn = sqlite3.connect('./temp.db')
            conn.row_factory = lambda cursor, row: row[0]

        except Error as e:
            print(e)
            
    cur = conn.cursor()


    tempC = cur.execute('select count from temp where itemID is ' + str(item_id))
    tempC = tempC.fetchall()
    for i in tempC:
        count += i

    return count


def searchBank(f):
    global count

    materials = requests.get('https://api.guildwars2.com/v2/account/materials?access_token=' + API_KEY)
    bank = requests.get('https://api.guildwars2.com/v2/account/bank?access_token=' + API_KEY)


    for i in materials.json():
            f.writerow((i['id'],i['count']))


    for j in bank.json():
        if(j):
            f.writerow((j['id'],j['count']))


def searchCharacters(f):
    global count
    characterList = requests.get('https://api.guildwars2.com/v2/characters?access_token=' + API_KEY).json()

    while characterList:
        character = characterList[0]
        character = character.replace(' ', '%20')                
        characterURL = 'https://api.guildwars2.com/v2/characters/' + character + '?access_token=' + API_KEY

        inventoryJSON = requests.get(characterURL).json()
        
        i = 0
        if(inventoryJSON):
                bags = inventoryJSON['bags']
                numOfBags = (len(bags))
                while(i < numOfBags):
                    bag = bags[i]
                    if (bag):                 
                        j = 0
                        bag_i = bag['inventory']
                        bag_size = len(bag_i)
                        while(j < bag_size):
                            item = bag_i[j]
                            if(item):
                                f.writerow((item['id'],item['count']))
                            j += 1
                    i += 1
        del characterList[0]


def request(api_path):
	url = 'https://api.guildwars2.com/v2/' + api_path
	try:
		temp = urllib.request.urlopen(url).read().decode('utf-8')
		return json.loads(temp)
	except:
		pass

def requestItem(searchGet):
        if isApiActive() is False:
                return(False)        
        try:
                conn = sqlite3.connect('./itemIndex.db')
        except Error as e:
                print(e)
                
        itemName = searchGet

        itemJSON = None

        conn.row_factory = lambda cursor, row: row[0]   #prevents fetchall() from return a tuple
        cur = conn.cursor()
        stringtemp = 'select itemID from itemIndex where name like "' + itemName + '" limit 1'
        #print(stringtemp)
        cur.execute(stringtemp)
        id = cur.fetchall()
        if id:
            id = str(id[0])
            url = 'https://api.guildwars2.com/v2/items?ids=' + id
            try:
                temp = urllib.request.urlopen(url).read().decode('utf-8')
                itemJSON = json.loads(temp)
            except:
                pass
               
            cur.close()
            return itemJSON
        else:
            cur.close()
            return None

def requestSellPrice(itemID):
        commerceJSON = request('commerce/prices/' + str(itemID))

        sell_price = commerceJSON['sells']['unit_price']
        
        return sell_price

def requestBuyPrice(itemID):
        commerceJSON = request('commerce/prices/' + str(itemID))

        buy_price = commerceJSON['buys']['unit_price']

        return buy_price
        

def requestItemByID(itemID):
    if itemID:
        itemID = str(itemID)
        url = 'https://api.guildwars2.com/v2/items?ids=' + itemID
				
        try:
            temp = urllib.request.urlopen(url).read().decode('utf-8')
            itemJSON = json.loads(temp)
        except:
            pass
			
    return itemJSON
		
    return None

def requestRecipe(itemID):
        if isApiActive()is False:
                return False
        try:
                conn = sqlite3.connect('./itemIndex.db')
        except Error as e:
                print(e)

        recipeJSON = None

        conn.row_factory = lambda cursor, row: row[0]   #prevents fetchall() from return a tuple
        cur = conn.cursor()
        stringtemp = 'select recipeID from recipeIndex where itemID like ' + str(itemID)
        cur.execute(stringtemp)
        id = cur.fetchall()
        if id:
            id = str(id[0])
            url = 'https://api.guildwars2.com/v2/recipes?id=' + id
            try:
                temp = urllib.request.urlopen(url).read().decode('utf-8')
                recipeJSON = json.loads(temp)
            except:
                pass
               
            conn.close()
            return recipeJSON

def updateDatabase():
    try:
        conn = sqlite3.connect('./itemIndex.db')
    except Error as e:
        print(e)

#materials = requests.get('https://api.guildwars2.com/v2/account/materials?access_token=' + API_KEY)

#-------------UPDATES ITEMS--------------------------------------------------------

    conn.row_factory = lambda cursor, row: row[0]   #prevents fetchall() from return a tuple
    cur = conn.cursor()
    cur.execute('select itemID from itemIndex')
    currentItems = cur.fetchall()

    string = 'Database already up to date'


    url = 'https://api.guildwars2.com/v2/items'
    newItems = requests.get(url).json()

    diff = set(currentItems) ^ set(newItems) #XOR to get the values that are different

    print(diff)

    array = list(diff)
    
    length = len(array)    

    modlen = (length % 200)

    if modlen < 200:
        modlen = 0

    id1 = None

    j = 0

    csvfile = open("updateItems.csv", 'w', newline = '')

    f = csv.writer(csvfile)

    print(length)
    while j < (length):
        x = 0
        request_string = 'https://api.guildwars2.com/v2/items?ids='
        #While loop that creates a request_string of 200 items
        while x < 200 and j < (length - modlen):
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


        if j >= (length - modlen):  
            x = 0
            #While loop that creates a request_string with the amount leftover that is under 200
            while x < (modlen) and j < length:
                request_string += str(array[j])
                if x != length:
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
    readfile = open('updateItems.csv')
    csvReader = csv.reader(readfile)

    for row in csvReader:
        try:
            cur.execute('insert into itemIndex (name, itemID, type, level, rarity, vendor_value, chat_link, icon) values (?, ?, ?, ?, ?, ?, ?, ?);', row)
        except Error as e:
            print(e)
        print(cur.fetchall())

    readfile.close()
    
    cursor = conn.execute('select * from itemIndex;')
    conn.commit()
    print("Committed")


#-----------------------------------------------UPDATE RECIPES---------------------------------------------
    cur.execute('select recipeID from recipeIndex')
    currentItems = cur.fetchall()
    
    url = 'https://api.guildwars2.com/v2/recipes'
    newItems = requests.get(url).json()

    diff2 = set(currentItems) ^ set(newItems) #XOR to get the values that are different

    print(diff2)

    array = list(diff2)
    
    length = len(array)    

    modlen = (length % 200)

    if modlen < 200:
        modlen = 0

    id1 = None

    j = 0

    csvfile = open("updateRecipes.csv", 'w', newline = '')

    f = csv.writer(csvfile)

    print(length)
    while j < (length):
        x = 0
        request_string = 'https://api.guildwars2.com/v2/recipes?ids='
        #While loop that creates a request_string of 200 items
        while x < 200 and j < (length - modlen):
            request_string += str(array[j])
            if x != 199:
                request_string += ','
            j += 1
            x += 1
        id1 = requests.get(request_string).json()
        if id1:
            for i in id1:
                f.writerow([i['id'],i['output_item_id']])


        if j >= (length - modlen):  
            x = 0
            #While loop that creates a request_string with the amount leftover that is under 200
            while x < (modlen) and j < length:
                request_string += str(array[j])
                if x != length:
                    request_string += ','
                j += 1
                x += 1
        id1 = requests.get(request_string).json()
        if id1:
            for i in id1:
                f.writerow([i['id'],i['output_item_id']])
        
    csvfile.close()
    readfile = open('updateREcipes.csv')
    csvReader = csv.reader(readfile)

    for row in csvReader:
        try:
            cur.execute('insert into recipeIndex (recipeID, itemID) values (?, ?);', row)
        except Error as e:
            print(e)
        print(cur.fetchall())

    readfile.close()
    
    conn.commit()
    print("Committed")
    if diff or diff2:
        string = 'Database Updated'
    return (string)


#writes to the CSVfile
def writeItemstoItemsCSV(id1, f):
    if id1:
       for i in id1:
            print(i)
            f.writerow([i['name'],i['id'],i['type'],i['level'],i['rarity'],i['vendor_value'],i['chat_link'],i['icon']])


def isCraftable(itemID):
    try:
        conn = sqlite3.connect('./itemIndex.db')
    except Error as e:
        print(e)    

    cur = conn.cursor()

    try:
        cur.execute('select recipeID from recipeIndex where itemID like ' + str(itemID))        
    except Error as e:
        print(e) 
    if cur.fetchall():
        craftable = True
    else:
        craftable = False

    return craftable
