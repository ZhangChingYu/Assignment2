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
    return


'''
Update an existing menu item
'''
def updateMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):
    try: 
        milkkind = getMilkKindByName(milkkind)
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

def getMenuItemByName(name):
    try: 
        conn = openConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM MenuItem WHERE Name = '%s';" % name)
        conn.commit()
        MenuItem = cur.fetchone()
        return MenuItem
    except:
        return None
    finally:
        cur.close()
        conn.close()

def getMilkKindByName(name):
    try: 
        conn = openConnection()
        cur = conn.cursor()
        cur.execute("SELECT MilkKindID FROM MilkKind WHERE MilkKindName = '%s';" % name )
        conn.commit()
        MilkKind = cur.fetchone()[0]
        return MilkKind
    except:
        return None
    finally:
        cur.close()
        conn.close()
'''

'''
if __name__ == '__main__':
    #openConnection()
    #print(updateMenuItem('French Toast', 'A sliced bread soaked in beaten eggs, milk, and cream, then pan-fried with butter', 1, None, None, None, None, 9.90, '11/01/2024', 'johndoe'))
    #print(getMenuItemByName('French Toast'))
    print(getMilkKindByName('Whole'))

