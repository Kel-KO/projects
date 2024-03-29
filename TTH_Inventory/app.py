from multiprocessing import connection
import os
import sqlite3
from contextlib import closing
from datetime import datetime

#with closing(sqlite3.connect("inv.db")) as connection:
#    with closing(connection.cursor()) as cursor:
#        rows = cursor.execute("SELECT 1").fetchall()
#        
#
#connection = sqlite3.connect("inv.db", check_same_thread=False)
from flask import Flask, flash, redirect, render_template, request, url_for
import psycopg2
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

POSTGRESSQL_URI = "-"
connection = psycopg2.connect(POSTGRESSQL_URI)

try:
    with connection: 
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE foodandbev (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
            cursor.execute("CREATE TABLE it (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
            cursor.execute("CREATE TABLE retail (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
            cursor.execute("CREATE TABLE admissions (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
            cursor.execute("CREATE TABLE operations (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
except psycopg2.errors.DuplicateTable:
    pass



#cnx = MySQLConnection(user='naijaboyz123', database='KKOdb')
#db = cnx.cursor(raw=True, buffered=True)
#print(connection.total_changes)

cursor = connection.cursor()
#------------database test connections


# -------------------------------SQLite(empty and recreate inv.db tables)---------------------------------------
#cursor.execute("DROP TABLE foodandbev")
#cursor.execute("DROP TABLE it")
#cursor.execute("DROP TABLE retail")
#cursor.execute("DROP TABLE admissions")
#cursor.execute("DROP TABLE operations")
#cursor.execute("CREATE TABLE foodandbev (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
#cursor.execute("CREATE TABLE it (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
#cursor.execute("CREATE TABLE retail (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
#cursor.execute("CREATE TABLE admissions (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
#cursor.execute("CREATE TABLE operations (Item TEXT, Quantity INTEGER, Location TEXT, Note TEXT)")
#---------------------------------------------------------------------------------------------------------





#x = 1
#y = "hi"
#cursor.execute("INSERT INTO foodandbev VALUES (?,?,?,?,?)",(x,y,x,y,y))
#r = cursor.execute("SELECT * FROM foodandbev").fetchall()
#print (r)
#cursor.execute("INSERT INTO foodandbev VALUES (2, 'patties', 1, 'RiverGrill', 'null')")
#cursor.execute("INSERT INTO foodandbev VALUES (3, 'silverware', 1, 'RiverGrill', 'null')")
#cursor.execute("UPDATE foodandbev SET quantity = 5 WHERE item = 'patties'")
#cursor.execute("INSERT INTO foodandbev VALUES (4, 'chips', 1, 'RiverGrill', 'null')")
#cursor.execute("UPDATE foodandbev SET quantity = ?, location = ?, note = ? WHERE item = ? ", (1, 'location', 'note', 'patties'))
#cursor.execute("INSERT OR IGNORE INTO foodandbev VALUES (?,?,?,?,?)",(4, 'item', 2, 'location', 'note'))
# fbnames = cursor.execute("SELECT item FROM foodandbev").fetchall()
# r = cursor.execute("SELECT * FROM it").fetchall()
# 
# x = 4
# if x == 4:
    # cursor.execute("INSERT OR IGNORE INTO foodandbev VALUES (?,?,?,?,?)",(0, '0', 0, '0', '0'))
    # connection.commit()
    # 
# print(fbnames)
# item = "pattiez"
# check = False
# for i in fbnames:
    # print(i[0])
    # if item == i[0]:
        # check = True
        # break
# 
# if check:
# cursor.execute("INSERT OR IGNORE INTO it VALUES (?,?,?,?)",('item45', 50, 'location', 'note'))
# connection.commit()
# r = cursor.execute("SELECT * FROM it").fetchall()
# w = cursor.execute("SELECT * FROM foodandbev").fetchall()
# print(r)
# print(w)
# r = cursor.execute("SELECT * FROM foodandbev").fetchall()
# print("hi")
    # connection.commit()
    # print("hi")
# else:
    # cursor.execute("UPDATE foodandbev SET quantity = ?, location = ?, note = ? WHERE item = ? ", (777, 'location', 'note', 'test2'))
    # connection.commit()
    # print("bye")
# cursor.execute("UPDATE foodandbev SET quantity = ?, location = ?, note = ? WHERE item = ? ", (69, 'location', 'note', 'patties'))
# connection.commit()
# print (r)

#
#fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
#fbnames = cursor.execute("SELECT item FROM foodandbev").fetchall()
#r = fbnames[0]
#
#b = 'buns'
#if b in fbnames:
#    print ("hi")
#else:
#    print("bye")

# print(r)


def admin():
    #require passphrase to acces admin or user mode
    x = 0
    if (request.form.get("pass")) == "-":
        x = 1
    elif (request.form.get("pass")) == "-":
        x = 2
    return x

@app.route("/",  methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # display basic index page
        return render_template("index.html")
    else:
        if admin() == 1:
            #display index page admin version
            return render_template("indexadmin.html")
        elif admin() == 2:
            #display index page regular user version
            return render_template("indexuser.html")
        else:
            #if passphrase doesn't match either options redisplay basic index page
            return render_template("index.html") 



        

@app.route("/itadmin",  methods=["GET", "POST"])
def itadmin():
    if request.method == "GET":
        # display IT page
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM it")
                it = cursor.fetchall()
        now = datetime. now()
        return render_template("itadmin.html", it = it, now = now)
    else:
        #update database using the user inputs
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(("CREATE TABLE IF NOT EXISTS it (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

                cursor.execute("SELECT item FROM it")
                itnames = cursor.fetchall()
                cursor.execute("SELECT location FROM it")
                itlocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM it")
                itnameandplace = cursor.fetchall()
        now = datetime. now()

        
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in itnameandplace:
            if item == (i[0]) and location == (i[1]):
                check = True
                break

        #if item is in the db aka "check == true" update that row, else add new item and it's row into db

        if not check:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO it VALUES (%s,%s,%s,%s)",(item, quantity, location, note))
                    connection.commit()
                    # id = id + 1
                    cursor.execute("SELECT * FROM it")
                    it= cursor.fetchall()
            print (it)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE it SET quantity = %s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM it")
                    it = cursor.fetchall()
            print(it)
            
        return render_template("itadmin.html", it = it,  now = now)

@app.route("/it",  methods=["GET", "POST"])
def it():
    if request.method == "GET":
        # display IT page
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM it")
                it = cursor.fetchall()
        return render_template("it.html", it = it, now = now)
    else:

        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT item FROM it")
                itnames = cursor.fetchall()
                cursor.execute("SELECT location FROM it")
                itlocation= cursor.fetchall()
                cursor.execute("SELECT item, location FROM it")
                itnameandplace = cursor.fetchall()

        now = datetime. now()

        #update database using the user inputs
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in itnameandplace:
            if item == i[0] and location == i[1]:
                check = True
                break

        if not check:
            err = "ONLY ADMINS HAVE THIS PERMISSION. SIGN IN AS ADMIN TO ADD ITEMS TO DB"
            return (err)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE it SET quantity = %s, note = %s WHERE item =%s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM it")
                    it = cursor.fetchall()
            print(it)

        return render_template("it.html",it = it, now = now)




@app.route("/retailadmin",  methods=["GET", "POST"])
def retailadmin():
    if request.method == "GET":
        # display retail page
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM retail")
                rt = cursor.fetchall()
        now = datetime. now()
        return render_template("rtadmin.html", rt = rt, now = now)
    else:
        #update database using the user inputs
        now = datetime. now()


        with connection:
            with connection.cursor() as cursor:
                cursor.execute(("CREATE TABLE IF NOT EXISTS retail (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

                cursor.execute("SELECT item FROM retail")
                rtnames = cursor.fetchall()
                cursor.execute("SELECT location FROM retail")
                rtlocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM retail")
                rtnameandplace = cursor.fetchall()

        
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in rtnameandplace:
            if item == (i[0]) and location == (i[1]):
                check = True
                break

        #if item is in the db aka "check == true" update that row, else add new item and it's row into db

        if not check:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO retail VALUES (%s,%s,%s,%s)",(item, quantity, location, note))
                    connection.commit()
                    # id = id + 1
                    cursor.execute("SELECT * FROM retail")
                    rt = cursor.fetchall()
            print (rt)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE retail SET quantity = %s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM retail")
                    rt = cursor.fetchall()
            print(rt)
            
        return render_template("rtadmin.html", rt = rt,  now = now)


@app.route("/retail",  methods=["GET", "POST"])
def retail():
    if request.method == "GET":
        # display retail page
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM retail")
                rt = cursor.fetchall()
        return render_template("rt.html", rt = rt, now = now)
    else:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT item FROM retail")
                rtnames = cursor.fetchall()
                cursor.execute("SELECT location FROM retail")
                rtlocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM retail")
                rtnameandplace = cursor.fetchall()

        now = datetime. now()

        #update database using the user inputs
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in rtnameandplace:
            if item == i[0] and location == i[1]:
                check = True
                break

        if not check:
            err = "ONLY ADMINS HAVE THIS PERMISSION. SIGN IN AS ADMIN TO ADD ITEMS TO DB"
            return (err)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                        cursor.execute("UPDATE retail SET quantity = %s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                        connection.commit()
                        cursor.execute("SELECT * FROM retail")
                        rt = cursor.fetchall()
            print(rt)

        return render_template("rt.html",rt = rt, now = now)




@app.route("/admissionsadmin",  methods=["GET", "POST"])
def admissionsadmin():
    if request.method == "GET":
        # display admissions page
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM admissions")
                ad = cursor.fetchall()
        return render_template("adadmin.html", ad = ad, now = now)

    else:
         #update database using the user inputs
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(("CREATE TABLE IF NOT EXISTS admissions (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

                cursor.execute("SELECT item FROM admissions")
                adnames = cursor.fetchall()
                cursor.execute("SELECT location FROM admissions")
                adlocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM admissions")
                adnameandplace = cursor.fetchall()

        
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in adnameandplace:
            if item == (i[0]) and location == (i[1]):
                check = True
                break

        #if item is in the db aka "check == true" update that row, else add new item and it's row into db

        if not check:
            with connection:
                with connection.cursor() as cursor:        
                    cursor.execute("INSERT INTO admissions VALUES (%s,%s,%s,%s)",(item, quantity, location, note))
                    connection.commit()
                    # id = id + 1
                    cursor.execute("SELECT * FROM admissions")
                    ad = cursor.fetchall()
            print (ad)
            
        else:
            with connection:
                with connection.cursor() as cursor:        
                    cursor.execute("UPDATE admissions SET quantity = %s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM admissions")
                    ad = cursor.fetchall()
            print(ad)
            
        return render_template("adadmin.html", ad = ad,  now = now)

@app.route("/admissions",  methods=["GET", "POST"])
def admissions():
    if request.method == "GET":
        # display admissions page
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM admissions")
                ad = cursor.fetchall()
        return render_template("ad.html", ad = ad, now = now)

    else:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT item FROM admissions")
                adnames = cursor.fetchall()
                cursor.execute("SELECT location FROM admissions")
                adlocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM admissions")
                adnameandplace = cursor.fetchall()

        now = datetime. now()

        #update database using the user inputs
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in adnameandplace:
            if item == i[0] and location == i[1]:
                check = True
                break

        if not check:
            err = "ONLY ADMINS HAVE THIS PERMISSION. SIGN IN AS ADMIN TO ADD ITEMS TO DB"
            return (err)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE admissions SET quantity = %s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM admissions")
                    ad = cursor.fetchall()
            print(ad)

        return render_template("ad.html",ad = ad, now = now)





        

@app.route("/foodandbevadmin",  methods=["GET", "POST"])
def foodandbevadmin():
    if request.method == "GET":
        #display foodandbev page user version
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM foodandbev")
                fb = cursor.fetchall()
        now = datetime. now()
        return render_template("fbadmin.html", fb = fb, now = now)
    else:
        #update database using the user inputs
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(("CREATE TABLE IF NOT EXISTS foodandbev (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

                # fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
                cursor.execute("SELECT item FROM foodandbev")
                fbnames = cursor.fetchall()
                cursor.execute("SELECT location FROM foodandbev")
                fblocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM foodandbev")
                fbnameandplace = cursor.fetchall()

        
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in fbnameandplace:
            if item == i[0] and location == i[1]:
                check = True
                break

        #if item is in the db aka "check == true" update that row, else add new item and it's row into db

        if not check:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO foodandbev VALUES (%s,%s,%s,%s)",(item, quantity, location, note))
                    connection.commit()
                    # id = id + 1
                    cursor.execute("SELECT * FROM foodandbev")
                    fb = cursor.fetchall()
            print (fb)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE foodandbev SET quantity =%s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM foodandbev")
                    fb = cursor.fetchall()
            print(fb)
            
 

        return render_template("fbadmin.html", fb = fb, now = now)

@app.route("/foodandbev",  methods=["GET", "POST"])
def foodandbev():
    if request.method == "GET":
        #display foodandbev page user version
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM foodandbev")
                fb = cursor.fetchall()
        return render_template("fb.html", fb = fb, now = now)
    else:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT item FROM foodandbev")
                fbnames = cursor.fetchall()
                cursor.execute("SELECT location FROM foodandbev")
                fblocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM foodandbev")
                fbnameandplace = cursor.fetchall()


        now = datetime. now()

        #update database using the user inputs
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in fbnameandplace:
            if item == i[0] and location == i[1]:
                check = True
                break

        if not check:
            err = "ONLY ADMINS HAVE THIS PERMISSION. SIGN IN AS ADMIN TO ADD ITEMS TO DB"
            return (err)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE foodandbev SET quantity = %s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM foodandbev")
                    fb = cursor.fetchall()
            print(fb)

        return render_template("fb.html", fb = fb, now = now)





@app.route("/operationsadmin",  methods=["GET", "POST"])
def operationsadmin():
    if request.method == "GET":
        # display operations page
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM operations")
                ops = cursor.fetchall()
        now = datetime. now()
        return render_template("opsadmin.html", ops = ops, now = now)
    else:
        #update database using the user inputs
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(("CREATE TABLE IF NOT EXISTS operations (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

                cursor.execute("SELECT item FROM operations")
                opsnames = cursor.fetchall()
                cursor.execute("SELECT location FROM operations")
                opslocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM operations")
                opsnameandplace = cursor.fetchall()

        
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in opsnameandplace:
            if item == (i[0]) and location == (i[1]):
                check = True
                break

        #if item is in the db aka "check == true" update that row, else add new item and it's row into db

        if not check:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO operations VALUES (%s,%s,%s,%s)",(item, quantity, location, note))
                    connection.commit()
                    # id = id + 1
                    cursor.execute("SELECT * FROM operations")
                    ops = cursor.fetchall()
            print (ops)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE operations SET quantity = %s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM operations")
                    ops = cursor.fetchall()
            print(ops)
            
        return render_template("opsadmin.html", ops = ops,  now = now)


@app.route("/operations",  methods=["GET", "POST"])
def operations():
    if request.method == "GET":
        # display retail page
        now = datetime. now()
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM operations")
                ops = cursor.fetchall()
        return render_template("ops.html", ops = ops, now = now)
    else:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT item FROM operations")
                opsnames = cursor.fetchall()
                cursor.execute("SELECT location FROM operations")
                opslocation = cursor.fetchall()
                cursor.execute("SELECT item, location FROM operations")
                opsnameandplace = cursor.fetchall()

        now = datetime. now()

        #update database using the user inputs
        item = str(request.form.get("item")).upper()
        quantity = str(request.form.get("quantity")).upper()
        location = str(request.form.get("location")).upper()
        note = str(request.form.get("note")).upper()

        #if no item is inputted reuturn an error
        if item == "":
            rspns = "PLEASE INPUT AN ITEM"
            return(rspns)

        if quantity == "":
            rspns = "PLEASE INPUT AN QUANTITY"
            return(rspns)


        #check if that item(with corresponding location) is already in the table
        check = False
        for i in opsnameandplace:
            if item == i[0] and location == i[1]:
                check = True
                break

        if not check:
            err = "ONLY ADMINS HAVE THIS PERMISSION. SIGN IN AS ADMIN TO ADD ITEMS TO DB"
            return (err)
            
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE operations SET quantity = %s, note = %s WHERE item = %s AND location = %s", (quantity, note, item, location))
                    connection.commit()
                    cursor.execute("SELECT * FROM operations")
                    ops = cursor.fetchall()
            print(ops)

        return render_template("ops.html", ops = ops, now = now)
