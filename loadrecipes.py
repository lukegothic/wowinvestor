import requests, re, json, sqlite3

profs = [{"id":171,"name":"Alchemy"},{"id":164,"name":"Blacksmithing"},{"id":202,"name":"Engineering"},{"id":165,"name":"Leatherworking"},{"id":197,"name":"Tailoring"}]

backendurl = "https://vanilla-twinhead.twinstar.cz/?spells=11.{}"
relv = "new Listview\({.*?data:(\[.*\]).*?\)"

dbconn = sqlite3.connect("db/data.sqlite")
c = dbconn.cursor()
c.execute("DELETE FROM luke_item_crafting")
c.execute("DELETE FROM luke_item_crafting_reagents")
dbconn.commit()
dbconn.close()

for p in profs:
    print(p["name"])
    r = requests.get(backendurl.format(p["id"]))
    jsontext = re.search(relv, r.text)
    txt = jsontext.groups(0)[0].replace("name:", "\"name\":").replace("quality:", "\"quality\":").replace("rank:", "\"rank\":").replace("level:", "\"level\":").replace("skill:", "\"skill\":").replace("reagents:", "\"reagents\":").replace("creates:", "\"creates\":").replace("colors:", "\"colors\":").replace("id:", "\"id\":").replace("school:", "\"school\":").replace(":'",":\"").replace("',","\",").replace("\\'","'").replace("[,","[")
    # with open("test.txt", "w") as f:
    #     f.write(txt)
    allrecipes = json.loads(txt)
    recipes = []
    recipes_regs = []
    for r in allrecipes:
        if "creates" in r and "reagents" in r:
            recipes.append((r["id"], r["name"], r["creates"][0], r["creates"][1], p["id"]))
            for reg in r["reagents"]:
                recipes_regs.append((r["id"], reg[0], reg[1]))
        else:
            pass
    dbconn = sqlite3.connect("db/data.sqlite")
    c = dbconn.cursor()
    c.executemany('INSERT OR IGNORE INTO luke_item_crafting VALUES (?,?,?,?,?)', recipes)
    icnt = c.rowcount
    c.executemany('INSERT OR IGNORE INTO luke_item_crafting_reagents VALUES (?,?,?)', recipes_regs)
    dbconn.commit()
    dbconn.close()
    print("Insertadas {} recetas".format(icnt))
