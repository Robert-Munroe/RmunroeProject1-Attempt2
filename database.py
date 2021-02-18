import sqlite3

conn = sqlite3.connect('Schools_Database.db')

c = conn.cursor()

c.execute("""CREATE TABLE school (
            Name text,
            City text,
            Size_2018 integer,
            Size_2017 integer,
            Earnings_2017 integer,
            Repayments_2016 integer
            )""")


conn.commit()

conn.close()
