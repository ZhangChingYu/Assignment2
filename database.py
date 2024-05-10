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
    query = f'SELECT * FROM Staff WHERE StaffID = \'{staffID.lower()}\' and Password = \'{password}\''
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
    cleanse_data = ' - '.join(curr_data)
    return cleanse_data

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
        cur.execute('UPDATE MenuItem SET Name = %s, Description = %s, CategoryOne = %s, CategoryTwo = %s, CategoryThree = %s, CoffeeType = %s, MilkKind = %s, Price = %s, ReviewDate = %s, Reviewer = %s WHERE menuItemId = %s;', 
                    (name, description, get_category(categoryone), get_category(categorytwo), get_category(categorythree), get_coffeeType(coffeetype), get_milkKind(milkkind), price, reviewdate, reviewer.lower(), id))
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


if __name__ == '__main__':
    # print(findMenuItemsByCriteria("fee"))
    get_staffID("John Doe")
    findMenuItemsByCriteria("fee")