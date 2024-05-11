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
    userid = "y24s1c9120_ccha0039"
    passwd = "VJqh47sW"
    myHost = "awsprddbs4836.shared.sydney.edu.au"
    #userid = "postgres"
    #passwd = "root"
    #myHost = "localhost"
    #database = "Assignment_2"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
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
    conn = openConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Staff WHERE StaffID = LOWER(%s) and Password = %s', (staffID, password))
    result = cursor.fetchall()
    if len(result) ==0:
        return None
    else:
        return list(result[0])


'''
List all the associated menu items in the database by staff
'''
def findMenuItemsByStaff(staffID):
    conn = openConnection()
    cursor = conn.cursor()
    cursor.execute('''
    select 
        menuitemid, 
        name, 
        COALESCE(description,''), 
        concat(c1.categoryName,
            CASE
                WHEN c2.categoryName IS NOT NULL THEN '|' || c2.categoryName
                ELSE ''
            END,
            CASE
                WHEN c3.categoryName IS NOT NULL THEN '|' || c3.categoryName
                ELSE ''
            END) as category, 
        concat(
            CASE
                WHEN coffeetypename IS NOT NULL THEN coffeetypename
                ELSE ''
            END,
            CASE
                WHEN milkkindname IS NOT NULL THEN ' - ' || milkkindname
                ELSE ''
            END) as options, 
        price, 
        COALESCE(TO_CHAR(reviewdate, 'DD-MM-YYYY'), ''),
        concat(firstname,' ',lastname) as reviewname 
    from menuitem 
    left join category c1 on menuitem.categoryOne = c1.categoryId
    left join category c2 on menuitem.categoryTwo = c2.categoryId
    left join category c3 on menuitem.categoryThree = c3.categoryId
    left join coffeetype on menuitem.coffeetype = coffeetype.coffeetypeid 
    left join milkkind on menuitem.milkkind = milkkind.milkkindid
    left join staff on menuitem.reviewer = staff.staffid
    where reviewer = '%s'
    order by description asc,price desc;
    ''' % staffID)
    results = cursor.fetchall()
    menu_items = list()

    for result in results:
        row = dict()
        row['menuitem_id'] = result[0]
        row['name'] = result[1]
        row['description'] = result[2]
        row['category'] = result[3]
        row['coffeeoption'] = result[4]
        row['price'] = result[5]
        row['reviewdate'] = result[6]
        row['reviewer'] = result[7]
        menu_items.append(row)
    return menu_items


'''
Find a list of menu items based on the searchString provided as parameter
See assignment description for search specification
'''
def findMenuItemsByCriteria(searchString):
    print(searchString)
    menu_item_tuples = []
    try: 
        conn = openConnection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM SEARCH_BY_KEYWORD('%s');" % searchString)
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
def updateMenuItem(id, name, description, categoryone, categorytwo, categorythree, coffeetype, milkkind, price, reviewdate, reviewer):
    try: 
        conn = openConnection()
        cur = conn.cursor()
        cur.execute('UPDATE MenuItem SET Name = %s, Description = %s, CategoryOne = %s, CategoryTwo = %s, CategoryThree = %s, CoffeeType = %s, MilkKind = %s, Price = %s, ReviewDate = %s, Reviewer = LOWER(%s) WHERE menuItemId = %s;', 
                    (name, description, get_category(categoryone), get_category(categorytwo), get_category(categorythree), get_coffeeType(coffeetype), get_milkKind(milkkind), price, reviewdate, reviewer, id))
        conn.commit()
        return True
    except Exception as e: 
        print(e)
        return False
    finally:
        cur.close()
        conn.close()



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

def get_staffID(staffName):
    firstname = staffName.split(" ")[0]
    lastname = staffName.split(" ")[1]
    try:
        conn = openConnection()
        curs = conn.cursor()
        curs.execute("SELECT * FROM Staff WHERE FirstName = %s AND LastName = %s;" ,(firstname, lastname))
        conn.commit()
        staffId =curs.fetchone()[0]
        print(staffId)
        return staffId
    except Exception as e:
        print(e)
        return None
    finally:
        curs.close()
        conn.close()

class MenuItem:
    def __init__(self, id, name, description, categories, coffeeOptions, price, reviewDate, reviewer):
        self.menuitem_id = id
        self.name = name
        self.description = description
        self.category = categories
        self.coffeeoption = coffeeOptions
        self.price = price
        self.reviewdate = reviewDate
        self.reviewer = reviewer


if __name__ == '__main__':
    # print(findMenuItemsByCriteria("fee"))
    get_staffID("John Doe")
    findMenuItemsByCriteria("fee")