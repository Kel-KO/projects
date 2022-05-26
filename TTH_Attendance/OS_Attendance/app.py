import os
import mysql.connector
from flask import Flask, flash, redirect, render_template, request, url_for
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)

#cnx = MySQLConnection(user='naijaboyz123', database='KKOdb')
#db = cnx.cursor(raw=True, buffered=True)

@app.route("/",  methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # display attendance page
        i = 0
        x = ['mark', 'kel', 'ryan', 'ty', 'aly', 'brannan']
        for person in x:
            i += 1
        return render_template("attendance.html",i = i, x = x)
