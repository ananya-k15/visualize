# To plot graphs

# Importing libraries
import matplotlib.pyplot as plt
import pymysql
import datetime
import pandas as pd
import database as dbop
import csvfiles as cvf
import numpy as np

# Graphical Menu
def graphmenu():
    print()
    print("Select a graph : ")
    print("A. Product wise comparison using bar graph")
    print("B. Gender wise product comparison using bar graph")
    print("C. Area wise sales using bar graph")
    print("D. Area wise sales using pie chart")
    print("E. Product wise sales using pie chart")
    print("F. Go back to main menu")
    print()


# Running all graphical operations
def main(cr, db):

    while True:

        # Printing menu and asking choice
        graphmenu()
        ch = input("Enter choice : ").upper()

        if ch == "A":
            barplot0(cr, db)
        elif ch == "B":
            barplot1(cr, db)
        elif ch == "C":
            barplot2(cr, db)
        elif ch == "D":
            piechart0(cr, db)
        elif ch == "E":
            piechart1(cr, db)
        elif ch == "F":
            break
        else:
            print("Invalid input")


# Creating bar graph to compare product wise sale
def barplot0(cr, db):
    # Declaring variables
    pronames = []
    ref = []
    PRICE = []
    FPRO = []

    # Extracting details from item table
    sql = "select * from items"
    cr.execute(sql)
    re = cr.fetchall()
    for row in re:
        pronames.append(row[1])
        ref.append([row[0], row[1], int(row[3])])

    # Setting width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize=(6, 4))

    # Setting height of bar
    for pro in ref:
        sql = "select Quantity from user_info where ItemID = '" + pro[0] + "'"
        cr.execute(sql)
        price = 0
        while True:
            res = cr.fetchone()
            if res == None:
                break
            else:
                price += int(res[0]) * pro[2]
        if price != 0:
            PRICE.append(price)
            FPRO.append(pro[1])

    # Adding colors
    n = len(PRICE)
    c = ["pink", "red", "orange", "yellow", "green", "cyan", "blue", "purple"]
    COLOR = []
    if n > len(c):
        j = n - len(c)
        COLOR += c
        COLOR += c[: j + 1]
    else:
        COLOR += c[: n + 1]

    # Setting position of bar on X axis
    br1 = np.arange(n)

    # Make the plot
    plt.bar(br1, PRICE, width=barWidth, edgecolor="grey", color=COLOR)

    # Adding Xticks
    plt.xlabel("Product", fontweight="bold")
    plt.ylabel("Sales", fontweight="bold")
    plt.xticks([r for r in range(n)], FPRO)
    plt.title("Product wise comparison using bar graph")

    plt.show()


# Creating bar graph to compare gender wise product sale
def barplot1(cr, db):
    # Declaring variables
    pronames = []
    ref = []
    MALE = []
    FEMALE = []
    FPRO = []

    # Extracting details from item table
    sql = "select * from items"
    cr.execute(sql)
    re = cr.fetchall()
    for row in re:
        pronames.append(row[1])
        ef.append([row[0], row[1], int(row[3])])

    # Setting width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize=(6, 4))

    # Setting height of bar
    for pro in ref:
        sql = "select Gender, Quantity from user_info where ItemID = '" + pro[0] + "'"
        cr.execute(sql)
        mprice = 0
        fprice = 0
        while True:
            res = cr.fetchone()
            if res == None:
                break
            else:
                if res[0].upper() == "M":
                    mprice += int(res[1]) * pro[2]
                elif res[0].upper() == "F":
                    fprice += int(res[1]) * pro[2]
        if mprice != 0 or fprice != 0:
            MALE.append(mprice)
            FEMALE.append(fprice)
            FPRO.append(pro[1])

    # Setting position of bar on X axis
    br1 = np.arange(len(MALE))
    br2 = [x + barWidth for x in br1]

    # Make the plot
    plt.bar(br1, MALE, color="cyan", width=barWidth, edgecolor="grey", label="Male")
    plt.bar(br2, FEMALE, color="pink", width=barWidth, edgecolor="grey", label="Female")

    # Adding Xticks
    plt.xlabel("Product", fontweight="bold")
    plt.ylabel("Sales", fontweight="bold")
    plt.xticks([r + barWidth for r in range(len(MALE))], FPRO)
    plt.title("Gender wise product comparison using bar graph")

    plt.show()


# Creating bar graph to compare area wise product sales
def barplot2(cr, db):
    # Declaring variables
    pronames = []
    SALE = {
        "NTH": 0,
        "NES": 0,
        "CEN": 0,
        "NEW": 0,
        "EAS": 0,
        "STH": 0,
        "SWD": 0,
        "WES": 0,
    }

    # Extracting details from item table
    sql = "select AreaID, Quantity, Price from user_info, items where user_info.ItemID = items.ItemID"
    cr.execute(sql)
    re = cr.fetchall()
    for row in re:
        price = int(row[1]) * int(row[2])
        if price != 0:
            pronames.append(row[0])
            SALE[row[0].strip()] += price

    # Setting width of bar
    barWidth = 0.5
    fig = plt.subplots(figsize=(6, 4))

    # Setting position of bar on X axis
    br1 = np.arange(len(SALE))

    # Make the plot
    plt.bar(
        br1,
        SALE.values(),
        width=barWidth,
        edgecolor="grey",
        color=["pink", "red", "orange", "yellow", "green", "cyan", "blue", "purple"],
    )

    # Adding Xticks
    plt.xlabel("Area", fontweight="bold")
    plt.ylabel("Sales", fontweight="bold")
    plt.xticks([r for r in range(len(SALE.values()))], pronames)
    plt.title("Area wise sales using bar graph")

    plt.show()


# Creating pie chart to compare area wise sale
def piechart0(cr, db):
    # Declaring variables
    SALE = {
        "NTH": 0,
        "NES": 0,
        "CEN": 0,
        "NEW": 0,
        "EAS": 0,
        "STH": 0,
        "SWD": 0,
        "WES": 0,
    }

    # Extracting details from item table
    sql = "select AreaID, Quantity, Price from user_info, items where user_info.ItemID = items.ItemID"
    cr.execute(sql)
    re = cr.fetchall()
    for row in re:
        SALE[row[0].strip()] += int(row[1]) * int(row[2])

    # Removing values with no sales
    L = []
    for i in range(len(SALE.keys())):
        if SALE[list(SALE.keys())[i]] == 0:
            L.append(list(SALE.keys())[i])
    for i in L:
        del SALE[i]

    # Creating plot
    fig = plt.figure(figsize=(10, 7))
    plt.pie(SALE.values(), labels=SALE.keys())
    plt.title("Area wise sales using pie chart")

    # Show plot
    plt.show()


# Creating pie chart to compare product wise sale
def piechart1(cr, db):
    # Declaring variables
    pronames = []
    ref = []
    PRICE = []
    FPRO = []

    # Extracting details from item table
    sql = "select * from items"
    cr.execute(sql)
    re = cr.fetchall()
    for row in re:
        pronames.append(row[1])
        ref.append([row[0], row[1], int(row[3])])

    # Setting height of bar
    for pro in ref:
        sql = "select Quantity from user_info where ItemID = '" + pro[0] + "'"
        cr.execute(sql)
        price = 0
        while True:
            res = cr.fetchone()
            if res == None:
                break
            else:
                price += int(res[0]) * pro[2]
        if price != 0:
            PRICE.append(price)
            FPRO.append(pro[1])

    # Creating plot
    fig = plt.figure(figsize=(10, 7))
    plt.pie(PRICE, labels=FPRO)
    plt.title("Product wise sales using pie chart")

    # Show plot
    plt.show()
