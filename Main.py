import requests
import json
import tkinter as tk
from tkinter import *
from tkinter import END, messagebox
from PIL import Image, ImageTk
from enum import Enum
from io import BytesIO
from contextlib import nullcontext
from distutils.command.config import config

print("Running")

#URL and Window Creation

pokemonURL = "https://pokeapi.co/api/v2/pokemon/"

window = tk.Tk()
#Window initilization
window.title("Pokedex++ (Powered by PokeAPI)")
window.configure(bg='lightgray')

frame = Frame(window)
scroll = Scrollbar(frame)
scroll.pack(side = RIGHT, expand=True)

#init fields
#global variables cause Im to lazy to be bothered

pokemon = nullcontext
pokemonData = nullcontext
pokemonURL = nullcontext
pkmBack = nullcontext
pkmFront = nullcontext
ability = ""

input= tk.Text(window, height = 1, width = 10)
moveList= tk.Text(window, height = 6, width = 15)

idLbl = tk.Label(window, text="National Dex #: ")
nameLbl = tk.Label(window, text="Name: ")
type1Lbl = tk.Label(window, text="Type 1: ")
type2Lbl = tk.Label(window, text="Type 2: ")
entryLbl = tk.Label(window, text="Enter Pokemon Name or National Dex Number")
HPLbl = tk.Label(window, text="HP: ") 
atkLbl = tk.Label(window, text="ATK: ") 
defLbl = tk.Label(window, text="DEF: ") 
spAtkLbl = tk.Label(window, text="SpATK: ") 
spDefLbl = tk.Label(window, text="SpDEF: ") 
speedLbl = tk.Label(window, text="SPEED: ") 
abilityLbl = tk.Label(window, text="Abilities: ") 
bstLbl = tk.Label(window, text="Base Stats ") 

##########################Function Declarations###############################################

#confirm window close
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
        print("Closing")

#appends the user's to the requestURL and requests the api
def getPokemon():
    global pokemonData
    global pokemon
    global ability
    global pokemonURL
    ability = ""
    inp = input.get(1.0, "end-1c")
    inp = inp.lower()
    pokemonURL = "https://pokeapi.co/api/v2/pokemon/" + inp
    pokemonData = requests.get(pokemonURL)
    pokemon = json.dumps(pokemonData.json(), sort_keys = True, indent = 1)
    
    fillData(pokemon)
    

#fills in the Labels
def fillData( pkm ):
    global idLbl
    global nameLbl
    
    pokeObj = json.loads(pkm)
    strId = str(pokeObj['id'])
    idLbl.config(text="National Dex #: " + strId)
    nameLbl.config(text="NAME: " + pokeObj['name'])
    
    getTypes(pkm)
    getStats(pkm)
    getAbilities(pkm)
    getSprites(pkm)
    getMoves(pkm)

    
    
#gets the type of requested pokemon
def getTypes( pkm ):
    global type1Lbl
    global type2Lbl
    
    counter = 0
    pokeObj = json.loads(pkm)
    for type in pokeObj['types']:
        if counter == 0:
            type1Lbl.config(text ="Type 1: " + pokeObj['types'][counter]['type']['name'])
            type2Lbl.config(text ="Type 2: none")
        else:
            type2Lbl.config(text ="Type 2: " + pokeObj['types'][counter]['type']['name'])
        counter += 1
    

#pokeAPI STAT ORDER
# 0 = HP; 1 = ATK; 2 = DEF; 3 = SpATK
# 4 = SpDEF; 5 = SPEED
#gets the base stats of a pokemon
def getStats( pkm ):
    global atkLbl
    global defLbl
    global spAtkLbl
    global spDefLbl
    global speedLbl
    global HPLbl
    
    pokeObj = json.loads(pkm)
    
    HPLbl.config(text = "HP: " + str(pokeObj['stats'][0]['base_stat']))
    atkLbl.config(text = "ATK: " + str(pokeObj['stats'][1]['base_stat']))
    defLbl.config(text = "DEF: " + str(pokeObj['stats'][2]['base_stat']))
    spAtkLbl.config(text = "SpATK: " + str(pokeObj['stats'][3]['base_stat']))
    spDefLbl.config(text = "SpDEF: " + str(pokeObj['stats'][4]['base_stat']))
    speedLbl.config(text = "SPEED: " + str(pokeObj['stats'][5]['base_stat']))
    
#get abilities for pokemon
def getAbilities( pkm ):
    global ability
    
    pokeObj = json.loads(pkm)
    
    counter = 0
    for a in pokeObj['abilities']:
        ability += (pokeObj['abilities'][counter]['ability']['name']) + ", "
        counter += 1
    
    abilityLbl.config(text = 'Abilities: ' + ability)

#gets move list
def getMoves( pkm ):
    global moveList
    global scroll
    global frame
    
    counter = 0
    moves = ""
    moveList.config(state='normal')
    moveList.delete("1.0", 'end')
    moveList.insert('end', "")
    pokeObj = json.loads(pkm)
    
    for move in pokeObj['moves']:
        moves += str(pokeObj['moves'][counter]['move']['name']) + "\n"
        counter += 1
    #print(moves)
    moveList.delete("1.0", 'end')
    moveList.insert('end', moves)
    moveList.config(state='disabled')
    moveList.config(yscrollcommand=scroll.set)
    scroll.config(command=moveList.yview)
    
#gets sprites and adds them to grid
def getSprites( pkm ):
    global pkmBack
    global pkmFront
    global window
    
    pokeObj = json.loads(pkm)
    response1 = requests.get(pokeObj['sprites']['back_default'])
    
    pkmBack = Image.open(BytesIO(response1.content))
    pkmBack = ImageTk.PhotoImage(pkmBack)
    
    response2 = requests.get(pokeObj['sprites']['front_default'])
    
    pkmFront = Image.open(BytesIO(response2.content))
    pkmFront = ImageTk.PhotoImage(pkmFront)
    
    bckSprt = tk.Label(window, image = pkmBack)
    bckSprt.grid(row = 0, column = 1, sticky = 'W', pady = 5)
    frntSprt = tk.Label(window, image = pkmFront)
    frntSprt.grid(row = 0, column = 0, sticky = 'W', pady = 5)
    
    
    
#Pack info into a grid
#please find a better way to do this part for the love of god
def gridLabels():
    global atkLbl
    global defLbl
    global spAtkLbl
    global spDefLbl
    global speedLbl
    global HPLbl
    global type1Lbl
    global type2Lbl
    global nameLbl
    global idLbl
    global entryLbl
    global input
    global submitBtn
    global abilityLbl
    global bstLbl
    global moveList
    
    entryLbl.grid(row = 1, column = 0, sticky = 'W', pady = 5)
    input.grid(row = 2, column = 0, sticky = 'W', pady = 5)
    submitBtn.grid(row = 2, column = 1, sticky = 'W', pady = 5)
    nameLbl.grid(row = 3, column = 0, sticky = 'W', pady = 5)
    idLbl.grid(row = 3, column = 1, sticky = 'W', pady = 5)
    type1Lbl.grid(row = 4, column = 0, sticky = 'W', pady = 5)
    type2Lbl.grid(row = 4, column = 1, sticky = 'W', pady = 5)
    bstLbl.grid(row = 5, column = 0, sticky = 'W', pady = 5)
    HPLbl.grid(row = 6, column = 0, sticky = 'W', pady = 5)
    atkLbl.grid(row = 7, column = 0, sticky = 'W', pady = 5)
    defLbl.grid(row = 8, column = 0, sticky = 'W', pady = 5)
    spAtkLbl.grid(row = 7, column = 1, sticky = 'W', pady = 5)
    spDefLbl.grid(row = 8, column = 1, sticky = 'W', pady = 5)
    speedLbl.grid(row = 6, column = 1, sticky = 'W', pady = 5)
    abilityLbl.grid(row = 5, column = 1, sticky = 'W', pady = 5)
    moveList.grid(row = 9, column = 0, sticky = 'W', pady = 5)
###############################################################################################

window.protocol("WM_DELETE_WINDOW", on_closing)

window.protocol("<Return>", getPokemon)

#labels and submit button
submitBtn = tk.Button(window, text = "Search", command = getPokemon)

gridLabels()

#shiny pachu icon cause fav
window.iconbitmap('res/icon_smol.ico')

#open window
window.mainloop()