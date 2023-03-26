# To handle csv and panda related operations

# Importing libraries
import database as dbop
import pandas as pd
import csv


def open_csv():
    while True:
        fil = input("Enter csv file name : ")
        fil += ".csv"

        try:
            sample = open(fil)
            return fil
        except FileNotFoundError:
            print("File Not Found")


def fill_t2(cr, db):
    with open("InstalledInfo.csv", "r") as fil:
        records = csv.reader(fil)

        for record in records:
            row = tuple(record)
            sql = "insert into items values( %s, %s, %s, %s )"
            cr.execute(sql, row)
            db.commit()


def csv_to_db(cr, db):
    fname = open_csv()

    with open(fname, "r") as fil:
        records = csv.reader(fil)

        for row in records:
            row = tuple(row)
            try:
                dbop.add_purchase(row, cr, db)
            except:
                print("This value could not be added :")
                print(dbop.printtable([row]))
        print("All csv file records successfully added")
