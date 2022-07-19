import os
import sqlite3
from contextlib import closing

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
#cursor.execute("CREATE TABLE foodandbev (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, quantity INTEGER, location TEXT, note TEXT)")
#x = 1
#y = "hi"
#cursor.execute("INSERT INTO foodandbev VALUES (?,?,?,?,?)",(x,y,x,y,y))
#r = cursor.execute("SELECT * FROM foodandbev").fetchall()
#print (r)
#cursor.execute("INSERT INTO foodandbev VALUES (2, 'patties', 1, 'RiverGrill', 'null')")
#cursor.execute("INSERT INTO foodandbev VALUES (3, 'silverware', 1, 'RiverGrill', 'null')")
#cursor.execute("UPDATE foodandbev SET quantity = 5 WHERE item = 'patties'")
#cursor.execute("INSERT INTO foodandbev VALUES (4, 'chips', 1, 'RiverGrill', 'null')")
fbnames = cursor.execute("SELECT item FROM foodandbev").fetchall()
r = cursor.execute("SELECT * FROM foodandbev").fetchall()


item = "pattiez"
check = False
for i in fbnames:
    if item == i[0]:
        check = True
        break

if not check:
    cursor.execute("INSERT OR IGNORE INTO foodandbev VALUES (?,?,?,?,?)",(1, item, 2, 'location', 'note'))
else:
    cursor.execute("UPDATE foodandbev SET quantity = ?, location = ?, note = ? WHERE item = ? ", (1, 'location', 'note', item))
print (r)

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
        return render_template("itadmin.html")

@app.route("/it",  methods=["GET", "POST"])
def it():
    if request.method == "GET":
        # display IT page
        return render_template("it.html")




@app.route("/retailadmin",  methods=["GET", "POST"])
def retailadmin():
    if request.method == "GET":
        # display retail page
        return render_template("rtadmin.html")

@app.route("/retail",  methods=["GET", "POST"])
def retail():
    if request.method == "GET":
        # display retail page
        return render_template("rt.html")




@app.route("/admissionsadmin",  methods=["GET", "POST"])
def admissionsadmin():
    if request.method == "GET":
        # display admissions page
        return render_template("adadmin.html")

@app.route("/admissions",  methods=["GET", "POST"])
def admissions():
    if request.method == "GET":
        # display admissions page
        return render_template("ad.html")





        

@app.route("/foodandbevadmin",  methods=["GET", "POST"])
def foodandbevadmin():
    if request.method == "GET":
        #display foodandbev page user version
        fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
        return render_template("fbadmin.html", fb = fb)
    else:
        #update database using the user inputs
        cursor.execute(("CREATE TABLE IF NOT EXISTS foodandbev (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, quantity INTEGER, location TEXT, note TEXT)"))

        fb = cursor.execute("SELECT * FROM foodandbev").fetchall()
        fbnames = cursor.execute("SELECT item FROM foodandbev").fetchall()


        item = str(request.form.get("item"))
        quantity = int(request.form.get("quantity"))
        location = str(request.form.get("location"))
        note = str(request.form.get("note"))
        new_item = str(request.form.get("additem"))

        #if new item is selected set the item variable to the value of "new item" to use in updating the database
        if item == "newitem":
            item = new_item


        #check if that item is already in the table
        check = False
        for i in fbnames:
            if item == fbnames[i]:
                check = True
                break

        #if item is in the db aka "check == true" update that row, else add new item and it's row into db

        if not check:
            cursor.execute("INSERT INTO foodandbev VALUES (?,?,?,?,?)",(quantity, item, quantity, location, note))
            connection.commit()
            #cursor.execute("INSERT INTO foodandbev VALUES (?,?,?,?,?)",(x,y,x,y,y))
            print (fb)
            print (quantity)
            print (item)
            print (quantity)
            print (location)
            print (note)
        else:
            cursor.execute("UPDATE foodandbev SET quantity = ?, location = ?, note = ? WHERE item = ? ", (quantity, location, note, item))
            connection.commit()
 
        #make a check throgh the db table to see if that item already exists. If not, add it to the table along with its other information
        # db.execute("UPDATE fbtable")

        return render_template("fbadmin.html", fb = fb)

@app.route("/foodandbev",  methods=["GET", "POST"])
def foodandbev():
    if request.method == "GET":
        #display foodandbev page user version
        return render_template("fb.html")
    else:
        #update database using the user inputs
        item = (request.form.get("item"))
        quantity = int(request.form.get("quantity"))
        location = (request.form.get("location"))
        note = (request.form.get("note"))
        new_item = (request.form.get("additem"))

        # db.execute("UPDATE fbtable")

        return render_template("fb.html" )
