#modules
import sys
from flask import Flask, render_template, request, redirect, g, session, flash, send_from_directory,url_for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import os
import sqlite3
from sqlite3 import Error
import random

#secret key
app = Flask(__name__)
app.secret_key = "fruit_music_COFFEE_DRIP__$_5_usa_rope_LAPTOP_Q_drip_9_ROPE_$_LAPTOP_zip_XBOX_yelp_hut_&"
app.config["TEMPLATES_AUTO_RELOAD"] = True
#app.config['TESTING'] = True
#app.config['ENV'] = 'development'
#app.config['DEBUG'] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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


def special_requirement(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        try:
            if "green47" == session['user']:
                return f(*args,**kwargs)
            else:
                return redirect(url_for('homePage'))
    
        except:
            return redirect(url_for('homePage'))
    return wrap

@app.route("/mainTool",methods=["GET"])
@login_required
@special_requirement
def staff():
    try:
        user = session['user']
        con = get_db()
        cur = con.cursor()
        cur.execute("SELECT * from Staff")
        staff_data = cur.fetchall()
        cur.execute("SELECT * from Students")
        student_data = cur.fetchall()
        cur.execute("SELECT * from Community")
        community_data = cur.fetchall()
        return render_template("mainTool.html", data1=staff_data,data2=student_data,data3=community_data,user=user)
    except Exception as e:
        print(e, file=sys.stdout)
        return redirect(url_for('homePage'))


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

        #userID must be registered
        cur.execute("""SELECT EXISTS(SELECT 1 FROM Staff WHERE userID=:un)""",{"un":un})
        checkUser1 = cur.fetchone()[0]
        cur.execute("""SELECT EXISTS(SELECT 1 FROM Students WHERE userID=:un)""",{"un":un})
        checkUser2 = cur.fetchone()[0]
        cur.execute("""SELECT EXISTS(SELECT 1 FROM Community WHERE userID=:un)""",{"un":un})
        checkUser3 = cur.fetchone()[0]

        if(checkUser1 or checkUser2 or checkUser3):
            #entered password must = hashed password for entered userID
            cur.execute("""SELECT S1.hash,S2.hash,C.hash FROM Staff AS S1, Students AS S2, Community AS C WHERE S1.userID=:un OR S2.userID=:un OR C.userID=:un""",{"un":un})
            checkHash1=cur.fetchone()[0]
            if(check_password_hash(checkHash1, pw)):
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


#registration logic
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("registration.html")
    else:
        conn = get_db()
        cur = conn.cursor()
        try:
        #accType: 1 = staff ; 2 = student ; 3 = community
        
        #default accType set to user
            accType = 2

        #optional values that will set user to student or community user
        #todo: add more instruction on register page)
            try:
                idNum = int(request.form['idNum'])
                i2 = int(request.form['id_two'])
                year = int(request.form["year"])
                school = request.form["school"]
            except:
            #set to community user by default if fields above were blank
                idNum = -1
                i2 = -1
                year = -1
                school = -1
                accType = 3

            try:
                tele = request.form["tele"]
            except:
                tele = -1
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            email = request.form["email"]
            user = request.form["user"]
            password = str(request.form["password"])
            p2 = str(request.form["p_two"])
            
            hashPSW = generate_password_hash(password)
        #default raffleNum: not participating
            raffleNum = -1
        #default account balance
            balance = float(0)
    
        #for staff user accounts / add 'or' for more admin accounts
            if (user == "green47"):
                accType = 1

        #check if user wants to participate in raffle and assign rand int 0-255, only added for student users
            if request.form.get("raffleTerms"):
                raffleNum = random.randint(0,255)

        #all users must agree to terms / (todo: create terms in html)
            if not request.form.get("agreement"):
                flash("Please read through and agree to the terms")
                return render_template("registration.html")

        #check phone #
            if(tele == -1):
                flash("enter a phone #")
                return render_template("registration.html")

        #check email format
            if('@' not in email):
                flash("invalid email address")
                return render_template("registration.html")
        #password matching check
            if(password != p2):
                flash("passwords must match")
                return render_template("registration.html")
        #verify id check
            if(idNum != i2 and accType==2):
            #-1 will math -1 for comm. users
                flash("id number could not be verified")
                return render_template("registration.html")
            if(type(idNum) != int and accType==2):
                flash("invalid ID")
                return render_template("registration.html")
       
        #name, email, username, and password are required
            if not firstName:
                flash("Please enter your first name")
                return render_template("registration.html")
            if not lastName:
                flash("Please enter your last name")
                return render_template("registration.html")
            if not email:
                flash("Please enter your email")
                return render_template("registration.html")
            if not user:
                flash("Please select a unique username")
                return render_template("registration.html")
            if not password:
                flash("Please select a password")
                return render_template("registration.html")
        #arbitrary length on password limit
            if len(password) > 16:
                flash("Please select a password fewer than sixteen characters")
                return render_template("registration.html")

        #code to check tables for existing usernames, emails, and ID num since these should be unique per account
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Staff WHERE userID=:un)""",{"un":user})
            checkUser1=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Staff WHERE email=:em)""",{"em":email})
            checkEmail1=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Students WHERE userID=:un)""",{"un":user})
            checkUser2=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Students WHERE email=:em)""",{"em":email})
            checkEmail2=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Community WHERE userID=:un)""",{"un":user})
            checkUser3=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Community WHERE email=:em)""",{"em":email})
            checkEmail3=cur.fetchone()[0]
            
            if (checkUser1 or checkUser2 or checkUser3):
                flash("username is taken")
                return render_template("registration.html")
            if (checkEmail1 or checkEmail1 or checkEmail3):
                flash("email address is already registered")
                return render_template("registration.html")

        #check id only for student and staff users
            if (accType==1 or accType==2):
                cur.execute("""SELECT EXISTS(SELECT 1 FROM Staff WHERE sID=:in)""",{"in":idNum})
                checkIDnum1=cur.fetchone()[0]
                cur.execute("""SELECT EXISTS(SELECT 1 FROM Students WHERE sID=:in)""",{"in":idNum})
                checkIDnum2=cur.fetchone()[0]
                if(checkIDnum1 or checkIDnum2):
                    flash("id number is already registered")
                    return render_template("registration.html")

        #staff user
            if(accType==1):
                try:
                    cur.execute("""INSERT INTO Staff VALUES (?,?,?,?,?,?,?,?)""",(user,hashPSW,idNum,firstName,lastName,email,tele, year))
                    conn.commit()
                    flash("Registration Successful for Staff User! Please login.")
                    return redirect(url_for('login'))
                except:
                
                    return render_template("registration.html")
        #student users
            if(accType==2):
                try:
                    cur.execute("""INSERT INTO Students VALUES (?,?,?,?,?,?,?,?,?,?,?)""",(user,hashPSW,idNum,firstName,lastName,email,tele,year,school,raffleNum, balance))
                    conn.commit()
                    flash("Registration Successful for Student User! Please login.")
                    return redirect(url_for('login'))
                except:
                   
                    return render_template("registration.html")
        #community users        
            if(accType==3):
                try:
                    cur.execute("""INSERT INTO Community VALUES (?,?,?,?,?,?,?)""",(user,hashPSW,firstName,lastName,email,tele,balance))
                    conn.commit()
                    flash("Registration Successful for Community User! Please login.")
                    return redirect(url_for('login'))
                except:
               
                    return render_template("registration.html")
                
        except Exception as e:
            print(e, file=sys.stdout)
            render_template("registration.html")
    return render_template("registration.html")

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

 


