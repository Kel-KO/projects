import os
from flask import Flask, flash, redirect, render_template, request, url_for
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)


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
            
                
