import sqlite3 as sql
from explorer import damaged_goods

with sql.connect("tmp/explorer.db") as con:
    data = damaged_goods()
    cur = con.cursor()
    for x, y in data:
        for z in y:
            id = x
            date = z['date']
            sku = z['sku']
            details = z['detailed_disposition']
            reason = z['reason']
            cur.execute("INSERT INTO damaged (id, date, sku, details, reason) VALUES (?,?,?,?,?)", (id, date, sku, details, reason))
    con.commit()
    msg = "Records successfully added"
    print msg
