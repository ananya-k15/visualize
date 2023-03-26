# Project Title : Marketing Sales Analyser
# Version : 1.0 2020-2021
# Developed By : Ananya Kumar
# Guide : Sarika Kaushal
# Last Updated On: 2021-03-22

# To run the entire project

# t1 - User table with the following attributes :
# CID, Name, Age, Gender, ItemID, Quantity, Date, Location
# t2 - Item table with price and item category
# t3 - Locality table with locality name, pincode and ID

# Importing libraries
import pymysql
import datetime
import pandas
import database as dbop
import csvfiles as cvf
import graphs as gr
from pyfiglet import figlet_format

result = figlet_format(" Sales", font="bulbhead")
result2 = figlet_format(" Analysis", font="bulbhead")
print(result, result2, sep="\n")


def printmenu():
    print()
    print("A. Add purchase detail")
    print("B. Display all purchases")
    print("C. Add a new item")
    print("D. Import purchase history from csv file")
    print("E. Graphical Analysis")
    print("Q. Quit")
    print()


def set_up():
    if not dbop.check("tables", "user_info", cr):
        dbop.create_t1(cr)
    if not dbop.check("tables", "items", cr):
        dbop.create_t2(cr)
        cvf.fill_t2(cr, db)
    if not dbop.check("tables", "locality", cr):
        dbop.create_t3(cr)
        cvf.fill_t2(cr, db)


# Connecting to MySQL
print("Connecting to MySQL... ", "", sep="\n")
db = pymysql.connect(host="localhost", user="root", passwd="@Ananya5492")
print("Database connected... ", "", sep="\n")
cr = db.cursor()
print("Cursor created... ", "", sep="\n")

# Creating database
dbop.create_db(cr)
set_up()

while True:
    printmenu()
    ch = input("Enter choice : ").upper()
    if ch == "A":
        dbop.fill_t1(cr, db)
    elif ch == "B":
        dbop.display_all(cr, db)
    elif ch == "C":
        dbop.add_item_data(cr, db)
    elif ch == "D":
        cvf.csv_to_db(cr, db)
    elif ch == "E":
        gr.main(cr, db)
    elif ch == "Q":
        print("Thank you ...")
        break
    else:
        print("Invalid input, please try again")
