import sqlite3

conn = sqlite3.connect('P_data.db')

c = conn.cursor()


def create_table(user_id: str):
    c.execute(f"""CREATE TABLE {user_id}(
            site_name text,
            data text
            )""")


def write_pass(user_id: int, site: str, _pass: int):
    with conn:
        user_id = f"id{str(user_id)}"
        c.execute(
           f"SELECT name FROM sqlite_master WHERE type='table' AND name='{user_id}'"
        )
        if c.fetchone() == None: create_table(user_id)
        c.execute(f"SELECT * From {user_id} WHERE site_name='{site}'")
        if c.fetchone() != None: return 'Error : Site name already exist'
        c.execute(f"INSERT INTO {user_id} VALUES ('{site}', '{str(_pass)}')")
        return 'Done encrypting and storing data.'


def delete_pass(user_id: int, site: str):
    with conn:
        user_id = f"id{str(user_id)}"
        c.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{user_id}'"
        )
        if c.fetchone() == None: return 'There isnt such dir.'
        c.execute(f"SELECT * FROM {user_id} WHERE site_name='{site}'")
        coun = len(c.fetchall())
        if coun > 1: return 'Error : Unknow Error form database. '
        elif coun == 0: return 'Error : No such site name. '
        c.execute(f"DELETE FROM {user_id} WHERE site_name='{site}'")
        return "Done deleting"


def read_pass(user_id: int, site: str):
    user_id = f"id{str(user_id)}"
    with conn:
        c.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{user_id}'"
        )
        if c.fetchone() == None:
            return 'Error : You dont have any pass stored.'
        c.execute(f"SELECT * FROM {user_id} WHERE site_name='{site}'")
        return c.fetchone()[1]
