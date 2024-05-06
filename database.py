#!/usr/bin/env python3
import psycopg2

#####################################################
##  Database Connection
#####################################################

'''
Connect to the database using the connection string
'''
def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    database = 'comp9120'
    userid = "postgres"
    passwd = "1231"
    myHost = "localhost"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=database,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn

'''
Validate staff based on username and password
'''
def checkStaffLogin(staffID, password):
    
    return ['johndoe', '654', 'John', 'Doe', 22, 38000]


'''
List all the associated menu items in the database by staff
'''
def findMenuItemsByStaff(staffID):

    return


'''
Find a list of menu items based on the searchString provided as parameter
See assignment description for search specification
'''
def findMenuItemsByCriteria(searchString):

    return


'''
Add a new menu item
'''
def addMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price):
    try:
        conn = openConnection()
        curs = conn.cursor()
        curs.callproc("add_menu_item",[name, description, get_category(categoryone), get_category(categorytwo), 
                                       get_category(categorythree), get_coffeeType(coffeetype), get_milkKind(milkkind), price])
        curs.close()
        conn.commit()
        print(f"{name} added!")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


'''
Update an existing menu item
'''
def updateMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):

    return

def get_category(category_name):
    try:
        conn = openConnection()
        curs = conn.cursor()
        curs.callproc("get_category_id", [category_name])
        category_id = curs.fetchone()[0]

        curs.close()
        conn.close()
        return category_id
    except Exception as e:
        print(f"Error: {e}")

def get_coffeeType(coffee_type):
    try:
        conn = openConnection()
        curs = conn.cursor()
        curs.callproc("get_coffee_type_id", [coffee_type])
        coffee_id = curs.fetchone()[0]

        curs.close()
        conn.close()
        return coffee_id
    except Exception as e:
        print(f"Error: {e}")

def get_milkKind(milk_kind):
    try:
        conn = openConnection()
        curs = conn.cursor()
        curs.callproc("get_milk_kind_id", [milk_kind])
        milk_id = curs.fetchone()[0]

        curs.close()
        conn.close()
        return milk_id
    except Exception as e:
        print(f"Error: {e}")




