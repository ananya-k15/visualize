# To run the database part of program

# Importing libraries
import pymysql
import datetime


def add_item_data(cr, db):
    # Taking item name
    while True:
        name = input("Enter item name : ")
        if name.isalpha():
            break
        print("Invalid item name")

    # Taking item price
    while True:
        price = input("Enter item price : ")
        if price.isnumeric():
            break
        print("Invalid price")

    # Taking item category
    while True:
        # Printing accepted categories -
        acats = ["Electronic", "Grocery", "Stationary", "Medicines", "Clothing"]
        print("Accepted categories are : ")
        printtable([acats])

        # Inputing category
        cat = input("Enter item category : ")
        if cat.isalpha() and cat in acats:
            break
        print("Invalid category")

    # Taking item id
    while True:
        itemID = input("Enter new item id : ")
        cr.execute("select ItemID from items")
        re = cr.fetchall()
        if itemID in re:
            print("Item ID already exists.")
            pass
        else:
            print("Adding new item ... ")
            break

    # Adding item to items table
    T = (itemID, name, cat, price)
    sql = "insert into items(ItemID, Name, Category, Price) values(%s,%s,%s,%s)"
    cr.execute(sql, T)
    db.commit()

    # Printing added item
    print("Item added to items table :")
    cr.execute("select * from items")
    re = cr.fetchall()
    printtable(re)

    # Asking if another item is to be added
    ch = input("Do you wish to add another item ? (Y/N) :")
    if ch.upper() == "Y":
        add_item_data(cr, db)


def create_db(cr):
    # Creating database
    if check("databases", "sales_analysis", cr):
        cr.execute("use sales_analysis")
    else:
        cr.execute("create database sales_analysis")
        cr.execute("use sales_analysis")


def check(category, name, cr):  # to check for a table/database
    sql = "show " + category
    cr.execute(sql)
    re = cr.fetchall()
    for i in re:
        if i[0].lower() == name:
            return True
    return False


def create_t1(
    cr,
):  # user_info -> [CID, Name, Age, Gender, ItemID, Quantity, Date, Location]
    sql = "create table user_info(CID decimal(10) primary key, Name varchar(20), Age decimal(2,0),\
    Gender char(1), ItemID varchar(6), Quantity decimal(5,2), Date date, AreaID varchar(6))"
    cr.execute(sql)


def create_t2(cr):  # items -> [ItemID, Name, Category, Price]
    sql = "create table items(ItemID varchar(6) primary key, Name varchar(20), Category varchar(15),\
    Price decimal(6,2))"
    cr.execute(sql)


def create_t3(cr):  # locality -> [AreaID, Name]
    sql = "create table locality(AreaID varchar(3) primary key, Name varchar(20))"
    cr.execute(sql)


def fill_t3(cr, db):
    # Accepted localities -
    loc = [
        ["North West Delhi", "NWS"],
        ["North Delhi", "NTH"],
        ["North East Delhi", "NES"],
        ["Central Delhi", "CEN"],
        ["New Delhi", "NEW"],
        ["East Delhi", "EAS"],
        ["South Delhi", "STH"],
        ["South West Delhi", "SWD"],
        ["West Delhi", "WES"],
    ]

    # Adding each locality
    for area in loc:
        sql = (
            'insert into locality(AreaID, Name) values("'
            + area[1]
            + '","'
            + area[0]
            + '")'
        )
    cr.execute(sql)
    db.commit()


def fill_t1(cr, db):
    # Taking user input [CID, Name, Age, Gender, ItemID, Quantity, Date, Location]
    inputs = take_user_data(cr)

    # Adding user data
    add_purchase(inputs, cr, db)

    # Asking if user wants to add again
    ch = input("Do you wish to add another purchase ? (Y/N) :")
    if ch.upper() == "Y":
        fill_t1(cr, db)


def add_purchase(details, cr, db):  # For adding data to user_info table
    sql = "insert into user_info values( %s, %s, %s, %s, %s, %s, %s, %s )"
    cr.execute(sql, details)
    db.commit()


def take_user_data(cr):
    # Taking customer name
    while True:
        name = input("Enter customer name : ")
        for i in name:
            if i.isnumeric():
                print("Invalid name")
                break
        else:
            break

    # Taking customer ID
    while True:
        cusID = input("Enter phone number (without extention): ")
        if cusID.isnumeric() and len(cusID) == 10:
            cr.execute("select Name, CID from user_info")
            re = cr.fetchall()
            if re == ():
                break
            for j in re:
                if j[1] == cusID and name == j[0].lower():
                    print("User identified")
                    break
                elif j[1] != cusID and name != j[0].lower():
                    print("New user added")
                    k = 0
                    break
            if k == 0:
                break
            print("Invalid number")

    # Taking customer age
    while True:
        age = input("Enter customer age : ")
        if age.isnumeric() and len(age) < 3:
            break
        print("Invalid age")

    # Taking customer gender
    while True:
        gen = input("Enter customer gender (M/F): ")
        if gen.upper() in ["M", "F"]:
            break
        print("Invalid gender")

    # Taking item ID
    while True:
        # Printing accepted ItemID values
        print("Accepted ItemID values :")
        cr.execute("select * from items")
        re = cr.fetchall()
        printtable(re)

        # Asking is user wants to add item
        ch = input("Do you wish to add a new item ? (Y/N) :")
        if ch.upper() == "Y":
            add_item_data(cr, db)

        t = True

        # Inputing item ID
        itemID = input("Enter item ID : ")
        cr.execute("select ItemID from items")
        re = cr.fetchall()
        for j in re:
            if itemID == j[0]:
                print("Item matched")
                t = False
        if not t:
            break
        print("Invalid item ID")

    # Taking purchase quantity
    while True:
        quan = input("Enter purchase quantity : ")
        if quan.isnumeric() and int(quan) > 0:
            break
        print("Invalid quantity")

    # Taking purchase date
    while True:
        yr = input("Enter purchase year (YYYY): ")
        mon = input("Enter purchase month (MM): ")
        dd = input("Enter purchase date (DD): ")

        try:
            newDate = datetime.datetime(int(yr), int(mon), int(dd))
            date = "%s/%s/%s" % (yr, mon, dd)
            break
        except ValueError:
            print("Invalid date")

    # Taking locality
    while True:
        # Printing accepted Area ID values
        print("Accepted area ID values :")
        cr.execute("select * from locality")
        re = cr.fetchall()
        biglist = []
        for tup in re:
            biglist.append(list(tup))
        printtable(biglist)

        # Inputing item ID
        t = True
        loc = input("Enter area ID : ")
        cr.execute("select AreaID from locality")
        re = cr.fetchall()
        for j in re:
            if loc == j[0].upper():
                t = False
        if not t:
            break
        print("Invalid area ID")

    details = (cusID, name, age, gen, itemID, quan, date, loc)
    return details


def display_all(cr, db):
    sql = "select * from user_info"
    cr.execute(sql)
    table = cr.fetchall()
    printtable(table)


def printtable(biglist):  # to print tablular stuctures using nested lists/tuples
    col = len(biglist[0])
    row = len(biglist)
    larg = [0 for i in range(col)]

    for row in biglist:
        for i in range(col):  # column
            if len(str(row[i])) > larg[i]:
                larg[i] = len(str(row[i])) + 1

    print()
    ch = sum(larg)
    print("|", "-" * (ch + col - 1), "|", sep="")
    for row in biglist:
        print("|", end="")
        for ind in range(len(row)):
            remaining = larg[ind] - len(str(row[ind]))
            print(row[ind], end=" " * remaining + "|")
        print()
        print("|", "-" * (ch + col - 1), "|", sep="")
    print()
