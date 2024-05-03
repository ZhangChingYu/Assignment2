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
    myDatabase = "Assignment_2"
    #userid = "y24s1c9120_unikey"
    userid = "postgres"
    passwd = "root"
    myHost = "localhost"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=myDatabase,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)
        print("Connected to database")
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
        select_id = 'SELECT MenuItemID FROM MenuItem ORDER BY MenuItemID DESC'
        curs.execute(select_id)
        menuItem_id = curs.fetchone()[0]

        # check in list?
        add_item = '''
            INSERT INTO MenuItem (MenuItemID, Name, Description, CategoryOne, CategoryTwo, CategoryThree, CoffeeType, MilkKind, Price)
            VALUES (%s,'%s','%s','%s','%s','%s','%s','%s',%s)
        ''' %(menuItem_id+1, name, description, 
                get_category(categoryone), get_category(categorytwo), get_category(categorythree), 
                get_coffeeType(coffeetype), get_milkKind(milkkind), price)
        curs.execute(add_item)
        curs.close()
        conn.commit()
        print(f"{name} added!")
    except Exception as e:
        print(f"Fail to add {name}!")
    return True


'''
Update an existing menu item
'''
def updateMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):
    try: 
        milkkind = get_milkKind(milkkind)
        conn = openConnection()
        cur = conn.cursor()
        cur.execute('UPDATE MenuItem SET Name = %s, Description = %s, CategoryOne = %s, CategoryTwo = %s, CategoryThree = %s, CoffeeType = %s, MilkKind = %s, Price = %s, ReviewDate = %s, Reviewer = %s WHERE Name = %s', 
                    (name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer, name))
        conn.commit()
        if cur.rowcount > 0:
            return True
    except:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
    return

def get_category(category_name):
    try:
        conn = openConnection()
        curs = conn.cursor()
        get_category_id = "SELECT CategoryID FROM Category WHERE lower(CategoryName)='%s'" %(category_name.lower())
        curs.execute(get_category_id)
        category_id = curs.fetchone()[0]

        curs.close()
        conn.close()
        return category_id
    except Exception as e:
        print(f"{category_name} is not defined")

def get_coffeeType(coffee_type):
    try:
        conn = openConnection()
        curs = conn.cursor()
        get_coffee_id = "SELECT CoffeeTypeID FROM CoffeeType WHERE lower(CoffeeTypeName)='%s'" %(coffee_type.lower())
        curs.execute(get_coffee_id)
        coffee_id = curs.fetchone()[0]

        curs.close()
        conn.close()
        return coffee_id
    except Exception as e:
        print(f"{coffee_type} is not defined")

def get_milkKind(milk_kind):
    try:
        conn = openConnection()
        curs = conn.cursor()
        get_milk_id = "SELECT MilkKindID FROM MilkKind WHERE lower(MilkKindName)='%s'" %(milk_kind.lower())
        curs.execute(get_milk_id)
        coffee_id = curs.fetchone()[0]

        curs.close()
        conn.close()
        return coffee_id
    except Exception as e:
        print(f"{milk_kind} is not defined")


