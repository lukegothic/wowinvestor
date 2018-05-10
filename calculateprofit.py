import sqlite3, utils
from subprocess import Popen
dbconn = sqlite3.connect("db/data.sqlite")
dbconn.row_factory = utils.dict_factory
c = dbconn.cursor()
data = c.execute("""select
	c.profession,
	c.name,
	--c.quantity,
	ah_creates.price,
	--i_regs.name,
	--r.quantity,
	--ah_regs.price,
	--i_regs.BuyPrice / i_regs.BuyCount,
	sum(case when ah_regs.price is not null then ah_regs.price else (i_regs.BuyPrice / i_regs.BuyCount) end * r.quantity / c.quantity)  as cprice
from
	luke_item_crafting c left join luke_item_crafting_reagents r on c.entry = r.entry
	left join luke_item_ahprices ah_creates on c.creates = ah_creates.entry
	left join luke_item_ahprices ah_regs on r.reagent = ah_regs.entry
	left join item_template i_regs on r.reagent = i_regs.entry
group by
	c.name
order by
	c.profession,
	c.name""").fetchall()
dbconn.commit()
dbconn.close()

with open("p_crafting.csv", "w") as f:
    f.write("Prof.;Item;AHPrice;Comp.Price\n")
    for d in data:
        f.write("{};{};{};{}\n".format(d["profession"],d["name"],d["price"],d["cprice"]))
#p = Popen('result.csv', shell=True)

dbconn = sqlite3.connect("db/data.sqlite")
dbconn.row_factory = utils.dict_factory
c = dbconn.cursor()
data = c.execute("""select
	i.entry,
	i.name,
    ah.price,
    i.BuyPrice,
    n.incrtime / 60 as rtime,
	n.maxcount,
	c.name as seller
from
	npc_vendor n
	left join item_template i on n.item = i.entry
	left join creature_template c on n.entry = c.entry
	left join luke_item_ahprices ah on n.item = ah.entry
--where
--	n.maxcount <> '0'
order by
	rtime desc""").fetchall()
dbconn.commit()
dbconn.close()

with open("p_vendoring.csv", "w") as f:
    f.write("id;Item;AHPrice;BuyPrice;Respawn;Qty;Seller\n")
    for d in data:
        f.write("{};{};{};{};{};{};{}\n".format(d["entry"],d["name"].replace("\"", "'"),d["price"],d["BuyPrice"],d["rtime"],d["maxcount"],d["seller"]))
