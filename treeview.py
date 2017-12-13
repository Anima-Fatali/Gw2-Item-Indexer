import api_requests

import urllib.request
import base64

import time

import os

from tkinter import *
from tkinter.ttk import *

global state
state = False

global g
g = 0

global tree
tree = None
global vsb

#name is the parent, itemID is the item to be added.
def addChild(parentName, itemID, tree):
    

    global g
    recipeJSON = api_requests.requestRecipe(itemID)
    itemJSON = api_requests.requestItemByID(itemID)

                
    if recipeJSON:
        for i in recipeJSON['ingredients']:
            itemID = i['item_id']
            count = i['count']
            itemJSON = api_requests.requestItemByID(itemID)

            if itemJSON:
                for i in itemJSON:
                    name = i['name']
                    item_ID = i['id']
                #Need to add method that pulls from api the ammount of item owned
                    #print(parentName + "     " + name)

                #print("ParentName = " + parentName + '\nName = ' + name)
                try:
                    amountOwned = api_requests.searchAccount(item_ID)
                    buy_price = api_requests.requestBuyPrice(item_ID)
                    sell_price = api_requests.requestSellPrice(item_ID)
                    tree.insert(parentName, 1, name, text=name, values=(amountOwned, count, buy_price, sell_price))
                    if api_requests.isCraftable(item_ID):
                        addChild(name, item_ID, tree)
                except:
                    g += 1
                    tree.insert(parentName, 1, name + str(g), text=name, values=('0', count, '0', '0'))
                    if api_requests.isCraftable(item_ID):
                        addChild(name + str(g), item_ID, tree)
    

def getTree():
    global tree
    return tree

def createTree(parent, itemID, craftable):
    start = time.time()
    
    global state
    global tree
    global vsb

    if craftable:  
        if state is True:
            state = False
            tree.pack_forget()
            vsb.pack_forget()
            return

        tree = Treeview(parent)
        
        vsb = Scrollbar(parent, orient="vertical", command=tree.yview)
        vsb.pack(side='right', fill='y')
        tree.configure(yscrollcommand=vsb.set)
        
        tree['columns']=('one','two','three', 'four')
        tree.column('one', width=75)
        tree.column('two', width=75)
        tree.column('three', width=100)
        tree.column('four', width=100)
        tree.heading('one', text='Owned')
        tree.heading('two', text='Required')
        tree.heading('three', text='Sell Listing')
        tree.heading('four', text='Buy Listing')

           

        
        recipeJSON = api_requests.requestRecipe(itemID)
        itemJSON = api_requests.requestItemByID(itemID)

        if itemJSON:
            for i in itemJSON:
                name = i['name']
                    
            tree.insert('', 1, 'itemHead', text = name)
                    
        if recipeJSON:
            for i in recipeJSON['ingredients']:
                itemID = i['item_id']
                count = i['count']
                itemJSON = api_requests.requestItemByID(itemID)

                if itemJSON:
                    for i in itemJSON:
                        name = i['name']
                #Need to add method that pulls from api the ammount of item owned
                tree.insert('itemHead', 1, name, text=name, values=('0', count))
                #print("itemHead child = " + name)
                        
        for each in tree.get_children():
            temp = tree.get_children(each)
            y = 0
            tempArr = [0] * len(temp)
            while y < len(temp):
            #for y in range (0,4):
                itemJSONtemp = api_requests.requestItem(tree.item(temp[y], 'text'))
                tempArr[y] = itemJSONtemp
                y += 1

        z = 0
        while z < len(tempArr):
            for i in tempArr[z]:
                itemID = i['id']
                name = i['name']
                if api_requests.isCraftable(itemID):
                    #print('Name : ' + name)
                    addChild(name, itemID, tree)
         
            z += 1

            
        state = True
        tree.pack()

    if(os.path.isfile('./temp.csv') is True):
        os.remove('./temp.csv')
    if(os.path.isfile('./temp.db') is True):
        os.remove('./temp.db')

    end = time.time()
    print(end-start)
        


