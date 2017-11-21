import api_requests

import urllib.request
import base64
from tkinter import *

class recipe_branch:
        
    global state
    state = False
	
    def image_clicked(parent, itemID, craftable):
        global state
	         
			
        if craftable:
            recipeJSON = api_requests.requestRecipe(itemID)
            #Iron Ingot.
        
            id_string = ''
            temp = [None] * 4
            j = 0
            print("Recipe JSON: " + (str(recipeJSON)))
            if recipeJSON:
                for i in recipeJSON['ingredients']:
                    text = i['item_id']
                    count = i['count']
                    print("Text: " + str(text))
                    #temp[j] = api_requests.requestItemByID(text)
                    j += 1
                    print("PLEASE: " + str(text) + " " + str(count))
                print("Temp: " + str(temp))
                info = "Name: " + str(text) + "\n" + "Count: " + str(count)

                itemJSON = api_requests.requestItemByID(text)

                for i in itemJSON:
                    itemIcon = i['icon']

                u = urllib.request.urlopen(itemIcon)
                raw_data = u.read()
                u.close()

                b64_data = base64.encodestring(raw_data)
                image=PhotoImage(data=b64_data)

    
                parent[0].labels[0].image = image
                                
                parent[0].labels[0].config(image = image)
                k = 0
                #while k < len(temp) and temp[k] is not None:
                 #   print(api_requests.requestItemByID(str(temp[k]['output_item_id'])))
                  #  k+=1
        numberInAccount = 0
        x = 0
        while x < 4:
            print("dfkkgjhadf;khgdaf;kjghdfk;jhgdafg;kjh")
            parent[0].labels[x].config(text = str(numberInAccount) + '/' + str(count),
                                       compound=TOP)
            x += 1
                

        parent[0].pack()				
    
        if state is True:
            state = False
            parent[0].pack_forget()
	
        else:
            state = True
            print("Test")
            x = 0
            while x < 4:
                parent[0].labels[x].pack(side = LEFT)
                x += 1
            parent[0].pack()

