import sqlite3 as sql
from explorer import find_non_returned

with sql.connect("tmp/explorer.db") as con:
    data = find_non_returned()
    cur = con.cursor()
    for index, value in data:
        date = value[0]
        id = value[1]
        sku = value[2]
        trans = value[3]
        paytype = value[4]
        detail = value[5]
        amount = value[6]
        quantity = value[7]
        title = value[8]
        cur.execute("INSERT INTO refunds (id, date, sku, trans, paytype, detail, amount, quantity, title) VALUES (?,?,?,?,?,?,?,?,?)", (id, date, sku, trans, paytype, detail, amount, quantity, title))
    con.commit()
    msg = "Records successfully added"
    print msg
