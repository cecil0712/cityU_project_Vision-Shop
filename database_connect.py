import sqlite3
from sqlite3 import Error
import os

script_dir = os.path.dirname(__file__)

def connect():
    database_path = os.path.join(script_dir, "database", "cityu_project.db")

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        return conn, cursor
    except Error as e:
        print(f'Failed to connect database with error messaged:\n{e}')
        return None, None
    
def close(conn, cursor):
    if conn:
        cursor.close()
        conn.close()

def get_item_coor(item):
    path = os.path.join(script_dir, "database_queries", "get_item_coor.sql")

    conn, cursor = connect()

    if not conn or not cursor:
        return None

    if not item:
        return 'Empty item name is not accepted.'
    
    try:
        with open(path, "r") as f:
            query = f.read()

            cursor.execute(query, (item,))
    except Error as e:
        print(f'Failed to execute with error message:\n{e}')
        return None
    
    item_name = cursor.fetchall()
    close(conn,cursor)
    return item_name[0]

def get_region_coor(region):
    path = os.path.join(script_dir, "database_queries", "get_region_coor.sql")

    conn, cursor = connect()

    if region=='':
        return 'Empty region name is not accepted.'

    try:
        with open(path, "r") as f:
            query = f.read()

            cursor.execute(query, (region,))
    except Error as e:
        print(f'Failed to execute with error message:\n{e}')
        return None
    
    region_name = cursor.fetchall()
    close(conn,cursor)
    return region_name[0]

def check_discount(item):
    path = os.path.join(script_dir, "database_queries", "check_discount.sql")

    conn, cursor = connect()

    try:
        with open(path, "r") as f:
            query = f.read()

            cursor.execute(query, (item,))
    except Error as e:
        print(f'Failed to execute with error message:\n{e}')
        return None
    
    item_name = cursor.fetchall()
    close(conn,cursor)

    if item_name != []: # if there is discounted item
        return item_name[0]
    
    return 0

def get_map():
    path = os.path.join(script_dir, "database_queries", "get_map.sql")

    conn, cursor = connect()

    try:
        with open(path, "r") as f:
            query = f.read()

            cursor.execute(query)
    except Error as e:
        print(f'Failed to execute with error message:\n{e}')
        return None
    
    result = cursor.fetchall()
    map = {}

    for region_name in result:
        map[region_name[0]]=[region_name[1],region_name[2]]

    close(conn,cursor)

    return map

def check_exist(li):
    conn,cursor = connect()

    cursor.execute('SELECT name FROM region;')

    region_list = [i[0] for i in cursor.fetchall()] # to extract the list from [('Name',),...] to ['Name',...]

    close(conn,cursor)

    for name in li:
        if name.lower() in region_list:
            return name
        
    return None

def get_item_list():

    conn, cursor = connect()

    cursor.execute('SELECT name FROM product;')

    item_list=[i[0] for i in cursor.fetchall()] # to extract the list from [('Name',),...] to ['Name',...]
    close(conn,cursor)

    return item_list