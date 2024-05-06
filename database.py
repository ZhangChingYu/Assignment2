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
    myDatabase = "comp9120"
    userid = "postgres"
    passwd = "1231"
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

    conn = openConnection()
    cursor = conn.cursor()
    query = f'SELECT * FROM Staff WHERE StaffID = \'{staffID}\' and Password = \'{password}\''
    cursor.execute(query)
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
    query = f'''
    select menuitemid, name, description, concat(categoryone,categorytwo,categorythree) as category, concat(coffeetypename,' ',milkkindname) as options, price	, reviewdate,concat(firstname,' ',lastname) as reviewname from menuitem 
    left join coffeetype on menuitem.coffeetype = coffeetype.coffeetypeid 
    left join milkkind on menuitem.milkkind = milkkind.milkkindid
    left join staff on menuitem.reviewer = staff.staffid
    where reviewer = \'{staffID}\'
    order by description asc,price desc;
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    menu_items = list()

    for result in results:
        row = dict()
        row['menuitem_id'] = result[0]
        row['name'] = handle_display_empty(result[1])
        row['description'] = handle_display_empty(result[2])
        row['category'] = displaying_category(str(result[3]))
        row['coffeeoption'] = format_options(str(result[4]))
        row['price'] = str(result[5])
        row['reviewdate'] = str(format_date(result[6]))
        row['reviewer'] = handle_display_empty(result[7])
        menu_items.append(row)
    return menu_items

def displaying_category(categories: str):
    if categories == '' or categories is None:
        return ''
    i =0
    result = ''
    while i < len(categories):
        if categories[i] == '1':
            result+= 'Breakfast' + '|'
        elif categories[i] == '2':
            result+= 'Lunch' + '|'
        elif categories[i] == '3':
            result+='Dinner' + '|'
        i+=1
    return result.strip('|')

def format_date(date):
    if date is None:
        return ''
    curr_date = str(date).split('-')
    reverse_order = curr_date[::-1]
    cleanse_date = '-'.join(reverse_order)
    return cleanse_date
def handle_display_empty(data):
    return '' if data == None else data

def format_options(coffee_option):
    
    curr_data = coffee_option.split()
    cleanse_data = '-'.join(curr_data)
    return cleanse_data


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
        conn = openConnection()
        cur = conn.cursor()
        cur.execute('UPDATE MenuItem SET Name = %s, Description = %s, CategoryOne = %s, CategoryTwo = %s, CategoryThree = %s, CoffeeType = %s, MilkKind = %s, Price = %s, ReviewDate = %s, Reviewer = %s WHERE Name = %s AND MilkKind = %s AND CoffeeType = %s', 
                    (name, description, get_category(categoryone), get_category(categorytwo), get_category(categorythree), get_coffeeType(coffeetype), get_milkKind(milkkind), price, reviewdate, reviewer, name, get_milkKind(milkkind), get_coffeeType(coffeetype)))
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
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()

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
        return None

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
        return None

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
        return None
'''

'''
if __name__ == '__main__':
    #openConnection()
    print(updateMenuItem('French Toast', 'A sliced bread soaked in beaten eggs, milk, and cream, then pan-fried with butter', 'Breakfast', None, None, None, None, 9.90, '10/01/2024', 'johndoe'))
    print(getMenuItemByName('French Toast'))

