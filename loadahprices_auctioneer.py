import re
import tkinter as tk
from tkinter import filedialog
import sqlite3
import utils

# Abrir archivo aux-addon.lua del directorio del wow--- ahora se llama Auctioneer.lua
# D:\Juegos\RetroWoW 1.12.1\WTF\Account\luke\SavedVariables (o similar)
root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("lua files","*.lua"),("all files","*.*")))
with open(filepath) as f:
    data = f.read()

reHro = '\[\"buyoutPrices\"\] = {(.*?)}'
m = re.findall(reHro, data, re.DOTALL)
content = m[0].replace("\n", "").replace("\t", "")
content = content.split(",")
reKey = '\[\"(\d*):(\d*):(\d*)\"\]'
reValue = '\"(.*)\"'
prices = []
# HECHO PARA HISTORY VALUES... PROBAR A HACERLO PARA ACTUAL y compras compulsivas
for c in content:
    if (c != ""):
        keyvalue = c.split(" = ")
        key = re.search(reKey, keyvalue[0])
        value = re.search(reValue, keyvalue[1]).groups(0)[0]
        value = value.split(":")[0]
        price = value.split("x")[0] if value.find("x") != -1 else value
        prices.append((key.groups(0)[0], key.groups(0)[1], price))


dbconn = sqlite3.connect("db/data.sqlite")
dbconn.row_factory = utils.dict_factory
c = dbconn.cursor()
c.execute("DELETE FROM luke_item_ahprices")
c.executemany('INSERT INTO luke_item_ahprices VALUES (?,?,?)', prices)
dbconn.commit()
dbconn.close()
