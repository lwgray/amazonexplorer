import sqlite3

conn = sqlite3.connect('tmp/explorer.db')
print "Opened database successfully";

conn.execute('Drop TABLE if exists damaged')
conn.execute('CREATE TABLE damaged (id TEXT, date TEXT, sku TEXT, details TEXT, reason TEXT)')
print "Table Damaged created successfully";
conn.close()
