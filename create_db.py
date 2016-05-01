import sqlite3

conn = sqlite3.connect('tmp/explorer.db')
print "Opened database successfully";

conn.execute('Drop TABLE if exists refunds')
conn.execute('CREATE TABLE refunds (id TEXT, date TEXT, sku TEXT, trans TEXT, detail TEXT, amount INTEGER, quantity INTEGER, title TEXT)')
print "Table created successfully";
conn.close()
