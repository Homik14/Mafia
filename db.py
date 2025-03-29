import sqlite3
import random

def new_game():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS players')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER,
            username TEXT ,
            role TEXT,
            mafia_vote INTEGER,
            citizen_vote INTEGER,
            voted INTEGER, 
            dead INTEGER)''')
    conn.commit()
    conn.close()

# create_dab()

def insert_player(player_id, username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO players (
            player_id,
            username)
            VALUES (?, ?)''',
            (player_id, username))
    conn.commit()
    conn.close()

def players_amount():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players')
    amount = cursor.fetchall()
    conn.close()
    return len(amount)


def set_roles(players_amount):

    game_roles = ['citizen']* players_amount
    mafias = round(players_amount * 0.3)
    for i in range(mafias):
        game_roles[i] = 'mafia'
    random.shuffle(game_roles)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT player_id, role FROM players')
    players_ids = cursor.fetchall()
    for role , players_id in zip(game_roles, players_ids):
        cursor.execute('''
            UPDATE players
            SET role = ?
            WHERE player_id = ?''',
        (role, players_id[0]))
    conn.commit()
    conn.close()




def get_mafia_usernames():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    sql = f'SELECT username FROM players WHERE role = "mafia"'
    cur.execute(sql)
    data = cur.fetchall()
    names = ''
    for row in data:
        name = row[0]
        names += name + '\n'
    con.close()
    return names



def get_players_roles():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    sql = f'SELECT player_id, role FROM players'
    cur.execute(sql)
    data = cur.fetchall()
    con.close()
    return data


def clear_db(dead=False):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    sql = f'UPDATE players SET mafia_vote = 0, citizen_vote = 0, voted = 0'
    if dead:
        sql += ', dead = 0'
    cur.execute(sql)
    conn.commit()
    conn.close()



def get_alive_players():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT username FROM players WHERE dead = 0')
    data = cur.fetchall()
    data = [data[0] for data in data]
    con.close()
    return data


def vote(type, username, player_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute (f'''
        SELECT username
        FROM players
        WHERE player_id = {player_id}''')
    can_vote = cursor.fetchall()
    if can_vote:
        cursor.execute(f'''
            UPDATE players
            SET {type} = 1
            WHERE username = '{username}' ''')
        cursor.execute(f'''
            UPDATE players
            SET voted = 1
            WHERE player_id = {player_id} ''')    

        conn.commit()
        conn.close()
        return True
    conn.close()
def kill(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    can_vote = cursor.fetchall()
    cursor.execute(f'''
            UPDATE players
            SET dead = 1
            WHERE username = '{username}' 
            ''')    

    conn.commit()
    conn.close()


def chec_winer(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f'''
            Select COUNT(*) FROM players
            WHERE role = 'mafia' and dead = 0 
            ''')    
    mafia = cursor.fetchall()[0]
    cursor.execute(f'''
            Select COUNT(*) FROM players
            WHERE role = 'citizen' and dead = 0 
            ''')
    citizen = cursor.fetchall()[0]
    if mafia[0] == 0 or citizen[0] == 0:
        if mafia[0] == 0:
            return 'citizen'
        else:
            return 'mafia'
        
    else:
        return False

        
        
    