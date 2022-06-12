import os
#import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

#cnx = MySQLConnection(user='naijaboyz123', database='KKOdb')
#db = cnx.cursor(raw=True, buffered=True)

@app.route("/",  methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # display index page
        return render_template("index.html")

@app.route("/it",  methods=["GET", "POST"])
def it():
    if request.method == "GET":
        # display IT page
        return render_template("it.html")

@app.route("/retail",  methods=["GET", "POST"])
def retail():
    if request.method == "GET":
        # display retail page
        return render_template("rt.html")

@app.route("/admissionsadmin",  methods=["GET", "POST"])
def admissions():
    if request.method == "GET":
        # display admissions page
        return render_template("ad.html")
        

@app.route("/foodandbev",  methods=["GET", "POST"])
def foodandbev():
    if request.method == "GET":
        # display food and bev page
        x = True
        # if (request.form.get("pass")) == "Typh00n2022":
            # x = True
        if x == True:
            return render_template("fbadmin.html")
        else:
            return render_template("fb.html")
    else:
        item = (request.form.get("item"))
        quantity = int(request.form.get("quantity"))
        location = (request.form.get("location"))
        note = (request.form.get("note"))

        # db.execute("UPDATE fbtable")

        return render_template("fbadmin.html" )
