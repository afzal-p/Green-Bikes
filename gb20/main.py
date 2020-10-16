#modules
import sys
from flask import Flask, render_template, request, redirect, g, session, flash, send_from_directory,url_for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os
import sqlite3
from sqlite3 import Error

#secret key
app = Flask(__name__)
app.secret_key = "fruit_music_COFFEE_DRIP__$_5_usa_rope_LAPTOP_Q_drip_9_ROPE_$_LAPTOP_zip_XBOX_yelp_hut_&"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['TESTING'] = False


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def special_requirement(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        try:
            if "Green47" == session['user']:
                return f(*args,**kwargs)
            else:
                return redirect(url_for('homePage'))
    
        except:
            return redirect(url_for('homePage'))
    return wrap

@app.route("/protected/<path:filename>")
@special_requirement
def protected(filename):
    try:
        return send_from_directory('protected', filename)
    except Exception as e:
        #print(session['user'], file=sys.stdout)
        return redirect(url_for('homePage'))

#link to db
DATABASE = '/Users/afzal/Downloads/gb20/user.db'
#currect table attributes
  #(id,first,last,year,school,email,phone,username,hash)
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.route("/",methods=["GET","POST"])
def homePage():
    if request.method == "GET":
        return render_template("homePage.html", user="Guest")
    

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        un = request.form.get("loginID")
        pw = request.form.get("password")

        if not un:
            flash("Please enter your username")
            return render_template("login.html")
        if not pw:
            flash("Please enter your password")
            return render_template("login.html")

        cur.execute("""SELECT EXISTS(SELECT 1 FROM users WHERE username=:un)""",{"un":un})
        checkUser = cur.fetchone()[0]

        if(checkUser):
            cur.execute("""SELECT hash FROM users WHERE username=:un""",{"un":un})
            checkHash=cur.fetchone()[0]
            if(check_password_hash(checkHash, pw)):
                session['logged'] = True 
                session['user'] = un
                return render_template("homePage.html", user=un)
            else:
                flash("invalid credentials. Please try again.")
                return render_template("login.html")
        else:
            flash("invalid credentials. Please try again.")
            return render_template("login.html")
    else:
        flash("invalid credentials. Please try again.")
        return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
  if request.method == "GET":
    return render_template("registration.html")
  else:
    conn = get_db()
    cur = conn.cursor()
    try:
        idNum = int(request.form['idNum'])
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        year = int(request.form["year"])
        school = request.form["school"]
        email = request.form["email"]
        tele = request.form["tele"]
        user = request.form["user"]
        password = str(request.form["password"])
        p2 = str(request.form["p_two"])
        i2 = int(request.form["id_two"])
        hashPSW = generate_password_hash(password)

        #check email
        if('@' not in email):
            flash("invalid email address")
            return render_template("registration.html")
        if(password != p2):
            flash("passwords must match")
            return render_template("registration.html")
        if(idNum != i2):
            flash("id number could not be verified")
            return render_template("registration.html")
        if(type(idNum) != int):
            flash("invalid ID")
            return render_template("registration.html")
        if not idNum:
            flash("Please enter your student id number")
            return render_template("registration.html")
        if not firstName:
            flash("Please enter your first name")
            return render_template("registration.html")
        if not lastName:
            flash("Please enter your last name")
            return render_template("registration.html")
        if not year:
            flash("Please select your year")
            return render_template("registration.html")
        if not school:
            flash("Please select your school")
            return render_template("registration.html")
        if not email:
            flash("Please enter your email")
            return render_template("registration.html")
        if not user:
            flash("Please select a username")
            return render_template("registration.html")
        if not password:
            flash("Please select a password")
            return render_template("registration.html")
        if len(password) > 16:
            flash("Please select a password fewer than sixteen characters")
            return render_template("registration.html")
    
        cur.execute("""SELECT EXISTS(SELECT 1 FROM users WHERE username=:un)""",{"un":user})
        checkUser=cur.fetchone()[0]
        cur.execute("""SELECT EXISTS(SELECT 1 FROM users WHERE email=:em)""",{"em":email})
        checkEmail=cur.fetchone()[0]
        cur.execute("""SELECT EXISTS(SELECT 1 FROM users WHERE id=:in)""",{"in":idNum})
        checkIDnum=cur.fetchone()[0]

        if checkUser:
            flash("username is taken")
            return render_template("registration.html")
        if checkEmail:
            flash("email address is already registered")
            return render_template("registration.html")
        if checkIDnum:
            flash("id number is already registered")
            return render_template("registration.html")

        cur.execute("""INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?)""",(idNum,firstName,lastName,year,school,email,tele,user,hashPSW))
        conn.commit()
        flash("Registration Successful. Please login.")
        return redirect(url_for('login'))
    except:
        render_template("registration.html")
    return redirect(url_for('login'))

@app.route("/passwordHelp", methods=["GET","POST"])
def reset():
    return render_template("passwordHelp.html")


@app.route("/rent")
@login_required
def checkout():
    return render_template("rent.html")


@app.route("/logout")
@login_required
def logout():
    session['logged'] = False 
    session.clear()
    return redirect(url_for('homePage'))

 
  