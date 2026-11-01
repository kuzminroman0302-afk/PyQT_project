import sqlite3

con = sqlite3.connect('proect.db')
cur = con.cursor()

cur.execute('DROP TABLE IF EXISTS profile')
cur.execute('DROP TABLE IF EXISTS Clicker')

cur.execute('''
CREATE TABLE IF NOT EXISTS profile (
    login TEXT PRIMARY KEY,
    password TEXT,
    name TEXT,
    surname TEXT,
    age INTEGER,
    country TEXT,
    avatar TEXT,
    level INTEGER,
    ex INTEGER,
    money INTEGER,
    pic TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Clicker (
    login TEXT PRIMARY KEY,
    money INTEGER,
    autoclicker INTEGER,
    mull INTEGER,
    critical INTEGER,
    click INTEGER,
    one INTEGER,
    two INTEGER,
    three INTEGER,
    four INTEGER,
    five INTEGER
)
''')

con.commit()
con.close()