import os
#import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

#cnx = MySQLConnection(user='naijaboyz123', database='KKOdb')
#db = cnx.cursor(raw=True, buffered=True)

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
        return render_template("fbadmin.html")
    else:
        #update database using the user inputs
        item = (request.form.get("item"))
        quantity = int(request.form.get("quantity"))
        location = (request.form.get("location"))
        note = (request.form.get("note"))
        new_item = (request.form.get("additem"))

        #if new item is selected set the item variable to the value of "new item" to use in updating the database
        if item == "new item":
            item = new_item
 
        #make a check throgh the db table to see if that item already exists. If not, add it to the table along with its other information
        # db.execute("UPDATE fbtable")

        return render_template("fbadmin.html" )

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
