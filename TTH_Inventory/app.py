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

@app.route("/admissions",  methods=["GET", "POST"])
def admissions():
    if request.method == "GET":
        # display admissions page
        return render_template("ad.html")

@app.route("/foodandbev",  methods=["GET", "POST"])
def foodandbev():
    if request.method == "GET":
        # display food and bev page
        return render_template("fb.html")
