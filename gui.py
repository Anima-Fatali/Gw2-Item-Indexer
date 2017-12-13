from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

import api_requests
import treeview

import urllib.request
import base64

import sqlite3
from sqlite3 import *

global API_KEY

root = Tk()
root.title('Gw2 Indexer')

#Causes the application to be launched in a maximized window
root.state('zoomed')

#Sets the favicon of the application
root.iconbitmap('./Images/favicon.ico')

#Calls pack_forget() on all items in the InfoFrame
def collapseInfoFrame():
    if itemInfoLabel:
        itemInfoLabel.pack_forget()
        
    if imgLabel:
        imgLabel.pack_forget()
    
    if treeview.getTree():
        treeview.getTree().pack_forget()
        treeview.vsb.pack_forget()
    displayRecipeButton.pack_forget()

#Displays the trademark information and collapses all item information when clicked.
def aboutClicked():

    collapseInfoFrame()
    
    trademark = '© 2015 ArenaNet, LLC. All rights reserved. NCSOFT, the interlocking NC logo, ArenaNet, Guild Wars, Guild Wars Factions, Guild Wars Nightfall, Guild Wars: Eye of the North, Guild Wars 2, Heart of Thorns, and all associated logos and designs are trademarks or registered trademarks of NCSOFT Corporation. All other trademarks are the property of their respective owners.'
    itemInfoLabel.config(text = trademark)
    itemInfoLabel.pack()


    
#Pulls data from the API and displays it in the infoFrame
def itemCallBack():
    global API_KEY
    
    api_requests.setApiKey(apiKeyEntry.get())

    collapseInfoFrame()

    try:
        conn = sqlite3.connect('./itemIndex.db')
    except Error as e:
        print(e)
        return
    
    itemInfo = "Placeholder text"
    itemName = "Error"
    itemID = "Error"
    itemType = "Placeholder"
    itemLevel = "Placeholder"
    itemRarity = "Placeholder"
    itemVendorValue = "Placeholder"
    itemChatLink = "Placeholder"
    itemIcon = "Placeholder"
    craftable = False

    
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()

    cur.execute('select name from itemIndex where name like "' + search.get() + '" limit 1')
    itemName = cur.fetchone()

    if itemName:
        cur.execute('select itemID from itemIndex where name like "' + search.get() + '" limit 1')
        itemID = cur.fetchone()

        cur.execute('select type from itemIndex where name like "' + search.get() + '" limit 1')
        itemType = cur.fetchone()

        cur.execute('select level from itemIndex where name like "' + search.get() + '" limit 1')
        itemLevel = cur.fetchone()

        cur.execute('select rarity from itemIndex where name like "' + search.get() + '" limit 1')
        itemRarity = cur.fetchone()

        cur.execute('select vendor_value from itemIndex where name like "' + search.get() + '" limit 1')
        itemVendorValue = cur.fetchone()

        cur.execute('select chat_link from itemIndex where name like "' + search.get() + '" limit 1')
        itemChatLink = cur.fetchone()

        cur.execute('select icon from itemIndex where name like "' + search.get() + '" limit 1')
        itemIcon = cur.fetchone()


        itemInfo = 'Item Name: ' + str(itemName) + '\n' + 'Type: ' + str(itemType) + '\n' + 'Level: ' + str(itemLevel) + '\n' + 'Rarity: ' + str(itemRarity) + '\n' + 'Vender Value: ' + str(itemVendorValue) + '\n' + 'Chat Link: ' + str(itemChatLink) + '\n' + 'ID: ' + str(itemID)

        if api_requests.isCraftable(itemID):
            itemInfo += '\n' + 'Craftable: ' + 'Yes'
            craftable = True
        else:
            itemInfo += '\n' + 'Craftable: ' + 'No'
            craftable = False



        itemInfoLabel.config(text = itemInfo)
        itemInfoLabel.pack()

        if imgLabel:
            imgLabel.pack_forget()

        if itemInfo is 'Item does not exist':
            itemInfoLabel.config(text = itemInfo)
            imgLabel.pack_forget()
            return

        u = urllib.request.urlopen(itemIcon)
        raw_data = u.read()
        u.close()

        b64_data = base64.encodestring(raw_data)
        image=PhotoImage(data=b64_data)

        itemInfoLabel.config(text = itemInfo)
        itemInfoLabel.pack()
        
        imgLabel.config(image=image)
        imgLabel.image = image
        imgLabel.pack()

        if(craftable):
            displayRecipeButton.config(command = lambda: treeview.createTree(infoFrame, itemID, craftable))  
            displayRecipeButton.pack()
            
    else:
        messagebox.showinfo(search.get(), 'Item does not exist')
    
    #I need to check for Item does not exist still
    
#Method that will clear the text box when called with the event and the entry box
def clear_entry(event, entry):
        entry.delete(0,END)

def updateDatabase():
    string = api_requests.updateDatabase()

    messagebox.showinfo('Update Script', string)



def removeItems():
    try:
        conn = sqlite3.connect('./itemIndex.db')
    except Error as e:
        print(e)

    conn.row_factory = lambda cursor, row: row[0]   #prevents fetchall() from return a tuple
    cur = conn.cursor()

    cur.execute('delete from itemIndex where itemID = 30698')
    cur.execute('delete from itemIndex where itemID = 49200')
    cur.execute('delete from recipeIndex where recipeID = 1')
    cur.execute('delete from recipeIndex where recipeID = 2')
    conn.commit()

    messagebox.showinfo("Remove Items", "The Bifrost and recipes 1 and 2 Removed from Database")




#Sets with and height to the size of the screen running the application
width = root.winfo_screenwidth()
height = root.winfo_screenheight()

#Sets the min and max width/height relative to the screen running the application
root.minsize(width=width, height=height-80)
root.maxsize(width=width, height=height-80)

#Frame that contains the searchFrame, itemInfoLabel, imgLabel, and displayRecipeButton
infoFrame = Frame(root)
infoFrame.grid(row = 0, column = 1, columnspan = 1, padx = (width/6, width/8))

#Frame that contains the search bar and button
searchFrame = Frame(infoFrame)
searchFrame.pack()

#Frame that contains the APIlabel and apiKeyEntry
apiFrame = Frame(root)
apiFrame.grid(row = 0, column = 0, sticky = NW)

#Frame that contains the about button
aboutFrame = Frame(root)
aboutFrame.grid(row = 0, column = 2, sticky = NE)

#Button with the text 'about' that will display necasarry information for the application
aboutButton = Button(aboutFrame, text = 'About', command = aboutClicked)
aboutButton.pack(side = LEFT)

#button that runs the update script
updateButton = Button(aboutFrame, text = "Update Database", command = updateDatabase)
updateButton.pack(side = RIGHT)

#Label in the apiFrame that contains the text 'Api Key'
APIlabel = Label(apiFrame, text = 'API Key: ')
APIlabel.pack(side = LEFT)

#Entry field for the API key
apiKeyEntry = Entry(apiFrame)
apiKeyEntry.insert(0, 'Enter API key')
apiKeyEntry.bind("<Button-1>", lambda event: clear_entry(event, apiKeyEntry))
apiKeyEntry.pack(side=RIGHT)


#Entry field for searching items
search = Entry(searchFrame)
search.pack(side = LEFT, padx = (200, 0))

#Button to click when you want to search
searchButton = Button(searchFrame, text = "Search", command = itemCallBack)
searchButton.pack(side = RIGHT, padx = (0,200))

#Button that displays a treeview of the recipe when clicked
displayRecipeButton = Button(infoFrame, text = 'Toggle Recipe', command = treeview.createTree)

#image Label, for the icon image
imgLabel = Label(infoFrame)

#label that contains all information about the item.  
itemInfoLabel = Label(infoFrame, text = '', wraplength = 200)
itemInfoLabel.pack()







