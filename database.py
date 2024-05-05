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
    menu_item_tuples = []
    try: 
        conn = openConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM SORTED_KEYWORD_RESULTS('%s');" % searchString)
        conn.commit()
        menu_item_tuples = cur.fetchall()
    except:
        return None
    finally:
        cur.close()
        conn.close()
    if menu_item_tuples.__len__() > 0:
        menuItems = []
        for item in menu_item_tuples:
            print(item)
            menuItems.append(MenuItem(*item))
        return menuItems
    return None


'''
Add a new menu item
'''
def addMenuItem(name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price):
    return


'''
Update an existing menu item
'''
def updateMenuItem(id, name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):
    try: 
        conn = openConnection()
        cur = conn.cursor()
        cur.execute('UPDATE MenuItem SET Name = %s, Description = %s, CategoryOne = %s, CategoryTwo = %s, CategoryThree = %s, CoffeeType = %s, MilkKind = %s, Price = %s, ReviewDate = %s, Reviewer = %s WHERE menuItemId = %s;', 
                    (name, description, get_category(categoryone), get_category(categorytwo), get_category(categorythree), get_coffeeType(coffeetype), get_milkKind(milkkind), price, reviewdate, reviewer, id))
        conn.commit()
        return True
    except:
        return False
    finally:
        cur.close()
        conn.close()

def get_category(category_name):
    try:
        conn = openConnection()
        curs = conn.cursor()
        get_category_id = "SELECT CategoryID FROM Category WHERE lower(CategoryName)='%s'" %(category_name.lower())
        curs.execute(get_category_id)
        conn.commit()
        category_id = curs.fetchone()[0]
        curs.close()
        conn.close()
        return category_id
    except Exception as e:
        print(f"Category: {category_name} is not defined")
        return None

def get_coffeeType(coffee_type):
    try:
        conn = openConnection()
        curs = conn.cursor()
        get_coffee_id = "SELECT CoffeeTypeID FROM CoffeeType WHERE lower(CoffeeTypeName)='%s'" %(coffee_type.lower())
        curs.execute(get_coffee_id)
        conn.commit()
        coffee_id = curs.fetchone()[0]

        curs.close()
        conn.close()
        return coffee_id
    except Exception as e:
        print(f"Coffee Type: {coffee_type} is not defined")
        return None

def get_milkKind(milk_kind):
    try:
        conn = openConnection()
        curs = conn.cursor()
        get_milk_id = "SELECT MilkKindID FROM MilkKind WHERE lower(MilkKindName)='%s'" %(milk_kind.lower())
        curs.execute(get_milk_id)
        conn.commit()
        coffee_id = curs.fetchone()[0]

        curs.close()
        conn.close()
        return coffee_id
    except Exception as e:
        print(f"Milk Type: {milk_kind} is not defined")
        return None
    
class MenuItem:
    def __init__(self, id, name, description, categoryOne, categoryTwo, categoryThree, coffeeType, milkKind, price, reviewDate, reviewer):
        self.menuitem_id = id
        self.name = name
        self.description = description if description != None else ''
        self.category = categoryOne
        self.category += '|'+categoryTwo if categoryTwo != None else ''
        self.category += '|'+categoryThree if categoryThree != None else ''
        if coffeeType == None and milkKind == None:
            self.coffeeoption = ''
        elif coffeeType != None and milkKind == None:
            self.coffeeoption = coffeeType
        elif coffeeType == None and milkKind != None:
            self.coffeeoption = milkKind
        else:
            self.coffeeoption = coffeeType+" - "+milkKind
        self.price = price
        self.reviewdate = reviewDate.strftime('%d-%m-%Y') if reviewDate != None else ''
        self.reviewer = reviewer if reviewer != None else ''
    
'''

'''
if __name__ == '__main__':
    #openConnection()
    #print(updateMenuItem('French Toast', 'A sliced bread soaked in beaten eggs, milk, and cream, then pan-fried with butter', 'Dinner', None, None, None, None, 9.90, '10/01/2024', 'johndoe'))
    #print(getMenuItemByName('Eggs Benedict'))
    #item = getMenuItemById(1)
    #print(item)
    print(findMenuItemsByCriteria('doe').__len__())
    print()

