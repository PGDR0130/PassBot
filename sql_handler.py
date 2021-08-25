#sql read and write

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
        if c.fetchone() != None: return 'Error : 網站名稱已存在'
        c.execute(f"INSERT INTO {user_id} VALUES ('{site}', '{str(_pass)}')")
        return '完成加密並儲存資料'


def delete_pass(user_id: int, site: str):
    with conn:
        user_id = f"id{str(user_id)}"
        c.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{user_id}'"
        )
        if c.fetchone() == None: return 'There isnt such dir.'
        c.execute(f"SELECT * FROM {user_id} WHERE site_name='{site}'")
        coun = len(c.fetchall())
        if coun > 1: return 'Error : 未知的資料庫錯誤 '
        elif coun == 0: return 'Error : 找不到這個網站名稱 '
        c.execute(f"DELETE FROM {user_id} WHERE site_name='{site}'")
        return "完成刪除資料"


def read_pass(user_id: int, site: str):
    user_id = f"id{str(user_id)}"
    with conn:
        if site == "all":
            c.execute(f"SELECT site_name FROM {user_id}")
            all = c.fetchall()
            sites = []
            for i in all:
                sites.append(i[0])
            return sites
        else:
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
            if c.fetchone() == None:
                return 'Error : 你沒有任何儲存的密碼'
            c.execute(f"SELECT * FROM {user_id} WHERE site_name='{site}'")
            d = c.fetchone()
            if d != None :
                return d[1]
            else :
                return None
