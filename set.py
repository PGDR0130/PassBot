import sqlite3

conn = sqlite3.connect(':memory:')

c = conn.cursor()


c.execute("""CREATE TABLE employees(
            user_id interger,
            site_name text,
            data interger
            )""")

