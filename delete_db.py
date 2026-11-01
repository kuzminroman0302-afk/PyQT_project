import sqlite3

con = sqlite3.connect('proect.db')
cur = con.cursor()
s = cur.execute("Select * from profile").fetchall()
print(s)
cur.execute("Delete from profile")
s = cur.execute("Select * from profile").fetchall()
print(s)
con.commit()
con.close()
