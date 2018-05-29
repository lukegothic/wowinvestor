import re
import tkinter as tk
from tkinter import filedialog
import sqlite3
import utils

root = tk.Tk()
root.withdraw()
filepath = filedialog.askopenfilename()
with open(filepath) as f:
    data = f.read()

reHro = '\[\"history\"\] = {(.*?)}'
m = re.findall(reHro, data, re.DOTALL)
content = m[1].replace("\n", "").replace("\t", "")
content = content.split(",")
reKey = '\[\"(\d*):(\d*)\"\]'
reValue = '\"(.*)\"'
prices = []
for c in content:
    if (c != ""):
        keyvalue = c.split(" = ")
        key = re.search(reKey, keyvalue[0])
        value = re.search(reValue, keyvalue[1]).groups(0)[0]
        value = value.split("#")
        if value[1] != "":
            price = value[1]
        else:
            price = value[2].split(";")[0].split("@")[0]
        prices.append((key.groups(0)[0], key.groups(0)[1], price))

dbconn = sqlite3.connect("db/data.sqlite")
dbconn.row_factory = utils.dict_factory
c = dbconn.cursor()
c.execute("DELETE FROM luke_item_ahprices")
c.executemany('INSERT INTO luke_item_ahprices VALUES (?,?,?)', prices)
dbconn.commit()
dbconn.close()
