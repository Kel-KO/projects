import os
import sqlite3
from contextlib import closing
from datetime import datetime

with closing(sqlite3.connect("inv.db")) as connection:
    with closing(connection.cursor()) as cursor:
        rows = cursor.execute("SELECT 1").fetchall()
        

connection = sqlite3.connect("inv.db", check_same_thread=False)
from flask import Flask, flash, redirect, render_template, request, url_for
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

#cnx = MySQLConnection(user='naijaboyz123', database='KKOdb')
#db = cnx.cursor(raw=True, buffered=True)
#print(connection.total_changes)

cursor = connection.cursor()
#------------database test connections


# -------------------------------(empty and recreate inv.db tables)---------------------------------------
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
    if (request.form.get("pass")) == "Typh00n2022":
        x = 1
    elif (request.form.get("pass")) == "Howdy123!":
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
        it = cursor.execute("SELECT * FROM it").fetchall()
        now = datetime. now()
        return render_template("itadmin.html", it = it, now = now)
    else:
        #update database using the user inputs
        now = datetime. now()
        cursor.execute(("CREATE TABLE IF NOT EXISTS it (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

        itnames = cursor.execute("SELECT item FROM it").fetchall()
        itlocation = cursor.execute("SELECT location FROM it").fetchall()
        itnameandplace = cursor.execute("SELECT item, location FROM it").fetchall()

        
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
            cursor.execute("INSERT OR IGNORE INTO it VALUES (?,?,?,?)",(item, quantity, location, note))
            connection.commit()
            # id = id + 1
            it = cursor.execute("SELECT * FROM it").fetchall()
            print (it)
            
        else:
            cursor.execute("UPDATE it SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            it = cursor.execute("SELECT * FROM it").fetchall()
            print(it)
            
        return render_template("itadmin.html", it = it,  now = now)

@app.route("/it",  methods=["GET", "POST"])
def it():
    if request.method == "GET":
        # display IT page
        now = datetime. now()
        it = cursor.execute("SELECT * FROM it").fetchall()
        return render_template("it.html", it = it, now = now)
    else:

        itnames = cursor.execute("SELECT item FROM it").fetchall()
        itlocation = cursor.execute("SELECT location FROM it").fetchall()
        itnameandplace = cursor.execute("SELECT item, location FROM it").fetchall()

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
            cursor.execute("UPDATE it SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            it = cursor.execute("SELECT * FROM it").fetchall()
            print(it)

        return render_template("it.html",it = it, now = now)




@app.route("/retailadmin",  methods=["GET", "POST"])
def retailadmin():
    if request.method == "GET":
        # display retail page
        rt = cursor.execute("SELECT * FROM retail").fetchall()
        now = datetime. now()
        return render_template("rtadmin.html", rt = rt, now = now)
    else:
        #update database using the user inputs
        now = datetime. now()
        cursor.execute(("CREATE TABLE IF NOT EXISTS retail (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

        rtnames = cursor.execute("SELECT item FROM retail").fetchall()
        rtlocation = cursor.execute("SELECT location FROM retail").fetchall()
        rtnameandplace = cursor.execute("SELECT item, location FROM retail").fetchall()

        
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
            cursor.execute("INSERT OR IGNORE INTO retail VALUES (?,?,?,?)",(item, quantity, location, note))
            connection.commit()
            # id = id + 1
            rt = cursor.execute("SELECT * FROM retail").fetchall()
            print (rt)
            
        else:
            cursor.execute("UPDATE retail SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            rt = cursor.execute("SELECT * FROM retail").fetchall()
            print(rt)
            
        return render_template("rtadmin.html", rt = rt,  now = now)


@app.route("/retail",  methods=["GET", "POST"])
def retail():
    if request.method == "GET":
        # display retail page
        now = datetime. now()
        rt = cursor.execute("SELECT * FROM retail").fetchall()
        return render_template("rt.html", rt = rt, now = now)
    else:
        rtnames = cursor.execute("SELECT item FROM retail").fetchall()
        rtlocation = cursor.execute("SELECT location FROM retail").fetchall()
        rtnameandplace = cursor.execute("SELECT item, location FROM retail").fetchall()

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
            cursor.execute("UPDATE retail SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            rt = cursor.execute("SELECT * FROM retail").fetchall()
            print(rt)

        return render_template("rt.html",rt = rt, now = now)




@app.route("/admissionsadmin",  methods=["GET", "POST"])
def admissionsadmin():
    if request.method == "GET":
        # display admissions page
        now = datetime. now()
        ad = cursor.execute("SELECT * FROM admissions").fetchall()
        return render_template("adadmin.html", ad = ad, now = now)

    else:
         #update database using the user inputs
        now = datetime. now()
        cursor.execute(("CREATE TABLE IF NOT EXISTS admissions (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

        adnames = cursor.execute("SELECT item FROM admissions").fetchall()
        adlocation = cursor.execute("SELECT location FROM admissions").fetchall()
        adnameandplace = cursor.execute("SELECT item, location FROM admissions").fetchall()

        
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
            cursor.execute("INSERT OR IGNORE INTO admissions VALUES (?,?,?,?)",(item, quantity, location, note))
            connection.commit()
            # id = id + 1
            ad = cursor.execute("SELECT * FROM admissions").fetchall()
            print (ad)
            
        else:
            cursor.execute("UPDATE admissions SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            ad = cursor.execute("SELECT * FROM admissions").fetchall()
            print(ad)
            
        return render_template("adadmin.html", ad = ad,  now = now)

@app.route("/admissions",  methods=["GET", "POST"])
def admissions():
    if request.method == "GET":
        # display admissions page
        now = datetime. now()
        ad = cursor.execute("SELECT * FROM admissions").fetchall()
        return render_template("ad.html", ad = ad, now = now)

    else:
        adnames = cursor.execute("SELECT item FROM admissions").fetchall()
        adlocation = cursor.execute("SELECT location FROM admissions").fetchall()
        adnameandplace = cursor.execute("SELECT item, location FROM admissions").fetchall()

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
            cursor.execute("UPDATE admissions SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            ad = cursor.execute("SELECT * FROM admissions").fetchall()
            print(ad)

        return render_template("ad.html",ad = ad, now = now)





        

@app.route("/foodandbevadmin",  methods=["GET", "POST"])
def foodandbevadmin():
    if request.method == "GET":
        #display foodandbev page user version
        fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
        now = datetime. now()
        return render_template("fbadmin.html", fb = fb, now = now)
    else:
        #update database using the user inputs
        cursor.execute(("CREATE TABLE IF NOT EXISTS foodandbev (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

        now = datetime. now()

        # fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
        fbnames = cursor.execute("SELECT item FROM foodandbev").fetchall()
        fblocation = cursor.execute("SELECT location FROM foodandbev").fetchall()
        fbnameandplace = cursor.execute("SELECT item, location FROM foodandbev").fetchall()

        
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
            cursor.execute("INSERT OR IGNORE INTO foodandbev VALUES (?,?,?,?)",(item, quantity, location, note))
            connection.commit()
            # id = id + 1
            fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
            print (fb)
            
        else:
            cursor.execute("UPDATE foodandbev SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
            print(fb)
            
 

        return render_template("fbadmin.html", fb = fb, now = now)

@app.route("/foodandbev",  methods=["GET", "POST"])
def foodandbev():
    if request.method == "GET":
        #display foodandbev page user version
        now = datetime. now()
        fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
        return render_template("fb.html", fb = fb, now = now)
    else:

        fbnames = cursor.execute("SELECT item FROM foodandbev").fetchall()
        fblocation = cursor.execute("SELECT location FROM foodandbev").fetchall()
        fbnameandplace = cursor.execute("SELECT item, location FROM foodandbev").fetchall()


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
            cursor.execute("UPDATE foodandbev SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
            print(fb)

        return render_template("fb.html", fb = fb, now = now)





@app.route("/operationsadmin",  methods=["GET", "POST"])
def operationsadmin():
    if request.method == "GET":
        # display operations page
        ops = cursor.execute("SELECT * FROM operations").fetchall()
        now = datetime. now()
        return render_template("opsadmin.html", ops = ops, now = now)
    else:
        #update database using the user inputs
        now = datetime. now()
        cursor.execute(("CREATE TABLE IF NOT EXISTS operations (item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

        opsnames = cursor.execute("SELECT item FROM operations").fetchall()
        opslocation = cursor.execute("SELECT location FROM operations").fetchall()
        opsnameandplace = cursor.execute("SELECT item, location FROM operations").fetchall()

        
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
            cursor.execute("INSERT OR IGNORE INTO operations VALUES (?,?,?,?)",(item, quantity, location, note))
            connection.commit()
            # id = id + 1
            ops = cursor.execute("SELECT * FROM operations").fetchall()
            print (ops)
            
        else:
            cursor.execute("UPDATE operations SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            ops = cursor.execute("SELECT * FROM operations").fetchall()
            print(ops)
            
        return render_template("opsadmin.html", ops = ops,  now = now)


@app.route("/operations",  methods=["GET", "POST"])
def operations():
    if request.method == "GET":
        # display retail page
        now = datetime. now()
        ops = cursor.execute("SELECT * FROM operations").fetchall()
        return render_template("ops.html", ops = ops, now = now)
    else:
        opsnames = cursor.execute("SELECT item FROM operations").fetchall()
        opslocation = cursor.execute("SELECT location FROM operations").fetchall()
        opsnameandplace = cursor.execute("SELECT item, location FROM operations").fetchall()

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
            cursor.execute("UPDATE operations SET quantity = ?, note = ? WHERE item = ? AND location = ?", (quantity, note, item, location))
            connection.commit()
            ops = cursor.execute("SELECT * FROM operations").fetchall()
            print(ops)

        return render_template("ops.html", ops = ops, now = now)
