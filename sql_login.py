import sqlite3

conn = sqlite3.connect('app_data.db')
c = conn.cursor()

def new_data():
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='login' ''')
    # if the count is 1, then table exists
    if (c.fetchone()[0] == 1):
        print("Table exists.")
    else:
        c.execute('''CREATE TABLE login (username text, pwd text)''')
        conn.commit()

def validify_name(name):
    c.execute("SELECT rowid FROM login WHERE username = ?;", [name])
    data = c.fetchall()
    if (len(data) == 0):
        print("Username does not exist")
        return False
    else:
        print("Username do exist")
        return True


def validify_password(name, pwd):
    c.execute("SELECT pwd FROM login WHERE username = ?;", [name])
    if (c.fetchone()[0] == pwd):
        print("Match!")
        return True
    else:
        print("Username and password do not match!")
        return False


def registration(name, pwd):
    c.execute("SELECT rowid FROM login WHERE username = ?;", [name])
    data = c.fetchall()

    if (len(data) == 0):
        print("Username does not exist")
        print("Creating new account...")

        c.execute("INSERT INTO login VALUES (?,?)", [name, pwd])

        for row in c.execute('SELECT * FROM login'):
            print(row)

        conn.commit()
        return True
    else:
        print("Username do exist")
        return False