
from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import *

import api_requests
import treeview

import difflib

import urllib.request
import base64

global API_KEY

try:
	import json
except ImportError:
	import simplejson as json

#Global variable to track the state of the item image and if the recipe tree is expanded or not.
global topstate
topstate = False


def itemCallBack():
    global API_KEY
    itemJSON = api_requests.requestItem(search.get())
    api_requests.setApiKey(apiKeyEntry.get())
    
    itemInfo = "Placeholder text"
    itemName = "Error"
    itemType = "Placeholder"
    itemLevel = "Placeholder"
    itemRarity = "Placeholder"
    itemVendorValue = "Placeholder"
    itemChatLink = "Placeholder"
    itemIcon = "Placeholder"
    craftable = False

    if itemJSON is False:
        itemInfo = 'API is down.'
    elif itemJSON:
        for i in itemJSON:
            itemName = i['name']
            if itemName is '':
                itemName = '{Missing Name}'
            itemID = i['id']
            itemType = i['type']
            itemLevel = i['level']
            itemRarity = i['rarity']
            itemVendorValue = i['vendor_value']
            itemChatLink = i['chat_link']
            itemIcon = i['icon']
            itemInfo = 'Item Name: ' + itemName + '\n' + 'Type: ' + itemType + '\n' + 'Level: ' + str(itemLevel) + '\n' + 'Rarity: ' + itemRarity + '\n' + 'Vender Value: ' + str(itemVendorValue) + '\n' + 'Chat Link: ' + itemChatLink + '\n' + 'ID: ' + str(itemID)


            #check if craftable
        if api_requests.isCraftable(itemID):
            itemInfo += '\n' + 'Craftable: ' + 'Yes'
            craftable = True
        else:
            itemInfo += '\n' + 'Craftable: ' + 'No'
            craftable = False
    else:
        itemInfo = 'Item does not exist'

    if itemInfo == 'API is down.' or itemInfo == 'Item does not exist':
        print(itemInfo)
        messagebox.showinfo(itemName, itemInfo)
        return

    if imgButton:
        imgButton.pack_forget()
    imgButton.config(command = lambda: treeview.createTree(separator2, itemID, craftable))  
    imgButton.pack()
    if itemInfo is 'Item does not exist':
        label.config(text = itemInfo)
        imgButton.pack_forget()
        return



    
            
    u = urllib.request.urlopen(itemIcon)
    raw_data = u.read()
    u.close()

    b64_data = base64.encodestring(raw_data)
    image=PhotoImage(data=b64_data)

    label.config(text = itemInfo)
    
    imgButton.config(image=image)
    imgButton.image = image

root = Tk()
root.title("Gw2 Indexer")

#Causes the application to be launched in a maximized window
root.state('zoomed')

#Causes the default size of unmaxized window to be 500px by 500px
#root.geometry('500x500')
root.iconbitmap('./Images/favicon.ico')

separator = Frame(height=2, bd=1, relief=SUNKEN)
separator.pack(padx=5, pady=5)

separator2= Frame(height=400, width=500)
separator2.pack()

label = Label(separator2, text = '')
label.pack()





def clear_entry(event, entry):
        entry.delete(0,END)

apiKeyEntry = Entry(separator, bd = 5)
apiKeyEntry.insert(0, 'Enter API key')
apiKeyEntry.bind("<Button-1>", lambda event: clear_entry(event, apiKeyEntry))

apiKeyEntry.pack(side=LEFT) 

search = Entry(separator, bd = 5)
search.pack(side=LEFT)

   

searchButton = Button(separator, text = "Search", command = itemCallBack)
searchButton.pack(side=RIGHT)


def updateDatabase():
    string = api_requests.updateDatabase()

    messagebox.showinfo("Update Script",string)
    

updateButton = Button(root, text = "Update Database", command = updateDatabase)
updateButton.pack()

def removeItems():
    try:
        conn = sqlite3.connect('./itemIndex.db')
    except Error as e:
        print(e)

    conn.row_factory = lambda cursor, row: row[0]   #prevents fetchall() from return a tuple
    cur = conn.cursor()

    cur.execute('delete from itemIndex where itemID = 30698')
    cur.execute('delete from itemIndex where itemID = 49200')
    conn.commit()

    messagebox.showinfo("Remove Bifrost", "The Bifrost Removed from Database")

removeButton = Button(root, text = "Remove the Bifrost", command = removeItems)
removeButton.pack()


imgButton = Button(separator2, command = treeview.createTree, borderwidth = 0)





root.mainloop()
