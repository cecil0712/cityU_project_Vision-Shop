# here we use MySQL as the DBMS
import mysql.connector
from mysql.connector import Error

def connect():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="cecil",
            password="c12182007",
            database="cityu_project"
        )
        cursor = conn.cursor()
        return conn,cursor
    except Error:
        print(f'Failed to connect database with error message:\n{Error}')
    
def close(conn,cursor):
    if conn.is_connected():
        cursor.close()
        conn.close()
        # print("Database closed.")

def get_item_coor(item):
    '''
    return the row num and column num of a specific item from the database
    '''
    conn,cursor=connect()
    if item=='':
        return 'Empty item name is not accepted.'
    try:
        cursor.execute(f"select row_num,col_num from supermarket where productid = (select id from product where name='{item}')")
    except Error:
        print(f'Failed to execute with error message:\n{Error}')
        return None
    item_name = cursor.fetchall()
    close(conn,cursor)
    return item_name[0]
# test : get_item_coor('Lindt Dark Chocolate Bar')

def get_region_coor(region):
    '''
    return the row num and column num of a specific region from the database
    '''
    conn,cursor=connect()
    if region=='':
        return 'Empty region name is not accepted.'
    try:
        cursor.execute(f"select row_num,col_num from supermarket where regionid = (select id from region where name='{region}')")
    except Error:
        print(f'Failed to execute with error message:\n{Error}')
        return None
    region_name = cursor.fetchall()
    close(conn,cursor)
    return region_name[0]

def check_discount(item):
    '''
    check whether the same region has discounted item
    '''
    conn,cursor=connect()
    try:
        cursor.execute(f"select product.name from supermarket,product where supermarket.productid=product.id and product.discount is not null and supermarket.regionid = (select region.id from region,supermarket where region.id=supermarket.regionid and supermarket.productid=(select id from product where name='{item}'));")
    except Error:
        print(f'Failed to execute with error message:\n{Error}')
        return None
    item_name = cursor.fetchall()
    close(conn,cursor)
    if item_name!=[]: # if there is discounted item
        return item_name[0]
    return 0
# test : print(check_discount('Kraft Cheddar Cheese'))

def get_map():
    '''
    return the map of the supermarket with dictionary datatype,ie. {region name:[row num,col num], ...}
    '''
    conn,cursor=connect()
    try:
        cursor.execute('select region.name,row_num,col_num from region,supermarket where regionid=region.id;')
    except Error:
        print(f'Failed to execute with error message:\n{Error}')
        return None
    result=cursor.fetchall()
    map={}
    for region_name in result:
        map[region_name[0]]=[region_name[1],region_name[2]]
        close(conn,cursor)
    return map

def check_exist(li):
    '''
    check if any item in li existed in the region_name list and return the name of region existed
    '''
    conn,cursor=connect()
    cursor.execute('select name from region;')
    region_list=[i[0] for i in cursor.fetchall()] # to extract the list from [('Name',),...] to ['Name',...]
    close(conn,cursor)
    for name in li:
        if name in region_list:
            return name
    return None
# test : print(check_exist(['25', 'Exit']))

def get_item_list():
    conn,cursor=connect()
    cursor.execute('select name from product;')
    item_list=[i[0] for i in cursor.fetchall()] # to extract the list from [('Name',),...] to ['Name',...]
    close(conn,cursor)
    return item_list
# test : print(get_item_list())

# print(get_region_coor('frozen foods'))