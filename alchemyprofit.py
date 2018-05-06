import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
dbconn = sqlite3.connect("db/wow_herbalism_profit.db")
dbconn.row_factory = dict_factory
c = dbconn.cursor()
profitlist = c.execute("select c.name,c.price,sum(cxr.total) as componentprice from craftables c left join (select idcraftable, idreagent, name, quantity * price as total from craftablesxreagents cx left join reagents r on cx.idreagent = r.id) cxr on c.id = cxr.idcraftable group by c.name,c.price").fetchall()
dbconn.commit()
dbconn.close()
print(profitlist)
