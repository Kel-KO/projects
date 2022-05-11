import os
from flask import Flask, flash, redirect, render_template, request, url_for
#from flask_session import Session
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)
# Ensure templates are auto-reloaded
#app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
# Configure CS50 Library to use SQLite database
#db = SQL("sqlite:///finance.db")
# Make sure API key is set
#if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")

#@app.after_request
#def after_request(response):
#    #"""Ensure responses aren't cached"""
#    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#    response.headers["Expires"] = 0
#    response.headers["Pragma"] = "no-cache"
#    return response

#export API_KEY=pk_32622fcc31204fa19642a4e5e34cc747

@app.route("/",  methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # display calculator page
        return render_template("calc.html")
    else:
        z=0
        x = int(request.form.get("x"))
        y = int(request.form.get("y"))
        q = request.form.get("q")

        
        if q == "+":
            z = x + y
            print(z)
        elif q == "-":
            z = x - y
            print(z)
        elif q == "/":
            z = x/y
            print(z)
        elif q == "x":
            z = x * y
            print(z)
        elif q == "^":
            z = x
            for i in range(y):
                z = z * x
        return render_template("answer.html", z = z)
            
                
