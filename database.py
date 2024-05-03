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
    #userid = "y24s1c9120_unikey"
    myDatabase = "Assignment_2"
    userid = "postgres"
    passwd = "root"
    myHost = "localhost"
    #myHost = "awsprddbs4836.shared.sydney.edu.au"

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
        cur = conn.cursor()
        cur.execute('INSERT INTO MenuItem (Name,Description,CategoryOne,CategoryTwo,CategoryThree,CoffeeType,MilkKind,Price) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)', 
                    (name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price))
        conn.commit()
        if cur.rowcount > 0:
            return True
    except:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
    return False


'''
Update an existing menu item
'''
def updateMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):

    return

'''

'''
if __name__ == '__main__':
    #openConnection()
    #print(addMenuItem(1,1,1,1,1,1,1,1))
    print()

