"""
Welcome to search in dictionary utility

Author: Parashar Bhatt
Created: 2 Nov 2020

Revision: 7 Nov 2020
Added Validation and GUI in the application

"""
import os
from tkinter import font
import tkinter as tk
from PIL import Image, ImageTk
import json
import difflib
#from difflib import SequenceMatcher
from difflib import get_close_matches

print(os.getcwd())

dict_file= os.path.join( str( os.getcwd()) ,'data.json')
#dict_file='search_word_in_dict_1\data.json'
print(dict_file)


with open(dict_file , "r") as fp:
    fl_content=fp.read()
fp.close()    

# Below code loads json content into dictionary object using json.loads built-in method of json package
d=json.loads(fl_content)
print(f"Current different words in dictionary are: {len(d)} \n")



#print(os.path)

HEIGHT = 500
WIDTH = 600


root = tk.Tk()
def translate(word):
    word=word.lower()
    if word.lower() in d:
        meanings =  d[word.lower()] 
    elif word.title() in d:
        meanings =  d[word.title()] 
    elif word.upper() in d:
        meanings = d[word.upper()]
    else:
        if len( get_close_matches(word, d.keys(),n=3,cutoff=0.8)) > 0:
            meanings = "Closest match: "+ get_close_matches( word, d.keys(),n=3,cutoff=0.8)[0]
        else:
            meanings=None
    return meanings

def search_click(search_val):
	#print(f"Search button clicked with value {search_val}")
	
	label = tk.Label(lower_frame , font=('Courier',18), anchor='nw', justify='left', bd=4, wraplength=400)
	label.place(relwidth=1, relheight=1)
		
	if len(search_val.strip()) >= 1:
		# Get keys from dictionary
		k=d.keys()
		# store all keys of dictionary in lower case
		n_k=[]
		for x in k:
			n_k.append(x.lower())
			#print(k)
		search_word=search_val.strip()
		result=translate(search_word)
		if (result == None):
			label['text'] = 'No such word exist in our dictionary'
		else:
			label['text']= result
		label_info = label.place_info()
		print(label_info)
		#label.place_forget()
	else:
		label['text']= 'Please enter word to search'
		
		

class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title('Dictionary Search')
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.original = Image.open('education_1.png')
        self.image = ImageTk.PhotoImage(self.original)
        self.display = tk.Canvas(self  , height=HEIGHT, width=WIDTH     , bd=0, highlightthickness=0)
        self.display.create_image(0, 0, image=self.image, anchor='nw', tags="IMG")
        self.display.grid(row=0, sticky="wens")
        self.pack(fill=tk.BOTH, expand=1)
        self.bind("<Configure>", self.resize)

    def resize(self, event):
        size = (event.width, event.height)
        #resized = self.original.resize(size,Image.ANTIALIAS)
        resized = self.original.resize(size,Image.Resampling.LANCZOS)
        self.image = ImageTk.PhotoImage(resized)
        self.display.delete("IMG")
        self.display.create_image(0, 0, image=self.image, anchor='nw', tags="IMG")






app = App(root)

frame =tk.Frame(app, bg='#80c1ff' ,bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')


entry=tk.Entry(frame, font=('Courier',18))
entry.place(relwidth=0.65 , relheight=1)


button = tk.Button(frame, text='Search' , font=('Courier',18) , command= lambda:search_click(entry.get()))
button.place(relx=.7, relwidth=0.3, relheight=1)

lower_frame =tk.Frame(app, bg='#80c1ff' ,bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.45 , anchor='n')

#label = tk.Label(lower_frame , font=('Courier',18), anchor='nw', justify='left', bd=4)
#label.place(relwidth=1,relheight=1)


app.mainloop()
#root.destroy()

