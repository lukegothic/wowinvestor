import sqlite3, utils, json

dbconn = sqlite3.connect("db/data.sqlite")
dbconn.row_factory = utils.dict_factory
c = dbconn.cursor()
npcs = c.execute("select c.entry as id, c.name from creature_template c").fetchall()
spawns = c.execute("select s.id, s.map, s.position_x, s.position_y, s.spawntimesecsmin, s.spawntimesecsmax, s.spawndist from creature s").fetchall()
dbconn.commit()
dbconn.close()
for npc in npcs:
    npc["spawns"] = list(s for s in spawns if s["id"] == npc["id"])

with open('data.json', 'w') as fp:
    json.dump(npcs, fp)
