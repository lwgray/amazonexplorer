import sqlite3 as sql
from explorer import find_non_returned

with sql.connect("tmp/explorer.db") as con:
    data = find_non_returned()
    cur = con.cursor()
    for index, value in data:
        id = value[1]
        date = value[0]
        sku = value[2]
        trans = value[3]
        detail = value[4]
        amount = value[5]
        quantity = value[6]
        title = value[7]
        cur.execute("INSERT INTO refunds (id, date, sku, trans, detail, amount, quantity, title) VALUES (?,?,?,?,?,?,?,?)", (id, date, sku, trans, detail, amount, quantity, title))
    con.commit()
    msg = "Records successfully added"
    print msg
