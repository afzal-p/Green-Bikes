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

#begin login 
@app.route("/loginHome", methods=["GET"])
def loginHome():
    if request.method == "GET":
        return render_template("loginHome.html")

@app.route("/staffLogin", methods=["GET","POST"])
def stafflogin():
    if request.method == "GET":
        return render_template("staffLogin.html")
    elif request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        un = request.form.get("loginID")
        pw = request.form.get("password")

        if not un:
            flash("Please enter your username")
            return render_template("staffLogin.html")
        if not pw:
            flash("Please enter your password")
            return render_template("staffLogin.html")

        #userID must be registered
        cur.execute("""SELECT EXISTS(SELECT 1 FROM Staff WHERE userID=:un)""",{"un":un})
        checkUser1 = cur.fetchone()[0]
  
        if(checkUser1):
            #entered password must = hashed password for entered userID
            cur.execute("""SELECT hash FROM Staff WHERE userID=:un""",{"un":un})
            checkHash1=cur.fetchone()[0]
            if(check_password_hash(checkHash1, pw)):
                session['logged'] = True 
                session['user'] = un
                return render_template("homePage.html", user=un)
            else:
                flash("invalid credentials. Please try again.")
                return render_template("staffLogin.html")
        else:
            flash("invalid credentials. Please try again.")
            return render_template("staffLogin.html")
    else:
        flash("invalid credentials. Please try again.")
        return render_template("staffLogin.html")

@app.route("/stuLogin", methods=["GET","POST"])
def stulogin():
    if request.method == "GET":
        return render_template("stuLogin.html")
    elif request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        un = request.form.get("loginID")
        pw = request.form.get("password")

        if not un:
            flash("Please enter your username")
            return render_template("stuLogin.html")
        if not pw:
            flash("Please enter your password")
            return render_template("stuLogin.html")

        #userID must be registered
        cur.execute("""SELECT EXISTS(SELECT 1 FROM Students WHERE userID=:un)""",{"un":un})
        checkUser1 = cur.fetchone()[0]
  
        if(checkUser1):
            #entered password must = hashed password for entered userID
            cur.execute("""SELECT hash FROM Students WHERE userID=:un""",{"un":un})
            checkHash1=cur.fetchone()[0]
            if(check_password_hash(checkHash1, pw)):
                session['logged'] = True 
                session['user'] = un
                return render_template("homePage.html", user=un)
            else:
                flash("invalid credentials. Please try again.")
                return render_template("stuLogin.html")
        else:
            flash("invalid credentials. Please try again.")
            return render_template("stuLogin.html")
    else:
        flash("invalid credentials. Please try again.")
        return render_template("stuLogin.html")

@app.route("/commLogin", methods=["GET","POST"])
def commLogin():
    if request.method == "GET":
        return render_template("commLogin.html")
    elif request.method == "POST":
        conn = get_db()
        cur = conn.cursor()
        un = request.form.get("loginID")
        pw = request.form.get("password")

        if not un:
            flash("Please enter your username")
            return render_template("commLogin.html")
        if not pw:
            flash("Please enter your password")
            return render_template("commLogin.html")

        #userID must be registered
        cur.execute("""SELECT EXISTS(SELECT 1 FROM Community WHERE userID=:un)""",{"un":un})
        checkUser1 = cur.fetchone()[0]
  
        if(checkUser1):
            #entered password must = hashed password for entered userID
            cur.execute("""SELECT hash FROM Community WHERE userID=:un""",{"un":un})
            checkHash1=cur.fetchone()[0]
            if(check_password_hash(checkHash1, pw)):
                session['logged'] = True 
                session['user'] = un
                return render_template("homePage.html", user=un)
            else:
                flash("invalid credentials. Please try again.")
                return render_template("commLogin.html")
        else:
            flash("invalid credentials. Please try again.")
            return render_template("commLogin.html")
    else:
        flash("invalid credentials. Please try again.")
        return render_template("commLogin.html")
#end login 

#begin registration 
@app.route("/registerHome", methods=["GET"])
def registerHome():
    if request.method == "GET":
        return render_template("registerHome.html")

@app.route("/staffReg", methods=["GET","POST"])
def staffReg():
    if request.method == "GET":
        return render_template("staffReg.html")
    else:
        conn = get_db()
        cur = conn.cursor()
        try:
            idNum = int(request.form['idNum'])
            i2 = int(request.form['id_two'])
            year = int(request.form["year"])
            school = request.form["school"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            email = request.form["email"]
            user = request.form["user"]
            password = str(request.form["password"])
            p2 = str(request.form["p_two"])
            word = str(request.form["word"])
            hashWord = generate_password_hash(word)
            hashPSW = generate_password_hash(password)

            try:
                tele = request.form["tele"]
            except:
                tele = -1

            if not word:
                flash("Please choose a secret word")
                return render_template("staff.html")

        #check phone #
            if(tele == -1):
                flash("enter a phone #")
                return render_template("staffReg.html")
    
        #for staff user accounts / add 'or' for more admin accounts
            if (user == "green47"):
                accType = 1

        #all users must agree to terms / (todo: create terms in html)
            if not request.form.get("agreement"):
                flash("Please read through and agree to terms")
                return render_template("staffReg.html")

        #check phone #
            if(len(tele) < 9):
                flash("enter a valid phone #")
                return render_template("staffReg.html")

        #check email format
            if('@' not in email):
                flash("invalid email address")
                return render_template("staffReg.html")
        #password matching check
            if(password != p2):
                flash("passwords must match")
                return render_template("staffReg.html")
        #verify id check
            if(idNum != i2):
                flash("id number could not be verified")
                return render_template("staffReg.html")
            if(type(idNum) != int):
                flash("invalid ID")
                return render_template("staffReg.html")
       
        #name, email, username, and password are required
            if not firstName:
                flash("Please enter your first name")
                return render_template("staffReg.html")
            if not lastName:
                flash("Please enter your last name")
                return render_template("staffReg.html")
            if not email:
                flash("Please enter your email")
                return render_template("staffReg.html")
            if not user:
                flash("Please select a unique username")
                return render_template("staffReg.html")
            if not year:
                flash("Please select a year")
                return render_template("staffReg.html")
            if not password:
                flash("Please select a password")
                return render_template("staffReg.html")
        #arbitrary length on password limit
            if len(password) > 16:
                flash("Please select a password fewer than sixteen characters")
                return render_template("staffReg.html")

        #code to check tables for existing usernames, emails, and ID num since these should be unique per account
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Staff WHERE userID=:un)""",{"un":user})
            checkUser1=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Staff WHERE email=:em)""",{"em":email})
            checkEmail1=cur.fetchone()[0]
            
            if (checkUser1):
                flash("username is taken")
                return render_template("staffReg.html")
            if (checkEmail1):
                flash("email address is already registered")
                return render_template("staffReg.html")

        #check id only for student and staff users
   
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Staff WHERE sID=:in)""",{"in":idNum})
            checkIDnum1=cur.fetchone()[0]
            if(checkIDnum1):
                flash("id number is already registered")
                return render_template("staffReg.html")

        #staff user
            if(accType==1):
                try:
                    cur.execute("""INSERT INTO Staff VALUES (?,?,?,?,?,?,?,?,?)""",(user,hashPSW,idNum,firstName,lastName,email,tele, year,hashWord))
                    conn.commit()
                    flash("Registration Successful for Staff User! Please login.")
                    return redirect(url_for('staffLogin'))
                except:
                    return render_template("staffReg.html")
        
        except Exception as e:
            #print(e, file=sys.stdout)
            render_template("staffReg.html")
    return render_template("staffReg.html")

@app.route("/stuReg", methods=["GET","POST"])
def stuReg():
    if request.method == "GET":
        return render_template("stuReg.html")
    else:
        conn = get_db()
        cur = conn.cursor()
        try:
            accType = 2
            idNum = int(request.form['idNum'])
            i2 = int(request.form['id_two'])
            year = int(request.form["year"])
            school = request.form["school"]
  
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
            word = str(request.form["word"])
            hashWord = generate_password_hash(word)
            hashPSW = generate_password_hash(password)
        #default raffleNum: not participating
            raffleNum = -1
        #default account balance
            balance = float(0)

        #check if user wants to participate in raffle and assign rand int 0-255, only added for student users
            if request.form.get("raffleTerms"):
                raffleNum = random.randint(0,255)

            if not word:
                flash("Please choose a secret word")
                return render_template("stuReg.html")
        #all users must agree to terms / (todo: create terms in html)
            if not request.form.get("agreement"):
                flash("Please read through and agree to the terms")
                return render_template("stuReg.html")

        #check phone #
            if(tele == -1):
                flash("enter a phone #")
                return render_template("stuReg.html")

        #check email format
            if('@' not in email):
                flash("invalid email address")
                return render_template("stuReg.html")
        #password matching check
            if(password != p2):
                flash("passwords must match")
                return render_template("stuReg.html")
        #verify id check
            if(idNum != i2 and accType==2):
                flash("id number's could not be verified")
                return render_template("stuReg.html")
            if(type(idNum) != int and accType==2):
                flash("invalid ID")
                return render_template("stuReg.html")
       
        #name, email, username, and password are required
            if not firstName:
                flash("Please enter your first name")
                return render_template("stuReg.html")
            if not lastName:
                flash("Please enter your last name")
                return render_template("stuReg.html")
            if not email:
                flash("Please enter your email")
                return render_template("stuReg.html")
            if not user:
                flash("Please select a unique username")
                return render_template("stuReg.html")
            if not password:
                flash("Please select a password")
                return render_template("stuReg.html")
            if not year:
                flash("Please select a year")
                return render_template("stuReg.html")
        #arbitrary length on password limit
            if len(password) > 16:
                flash("Please select a password fewer than sixteen characters")
                return render_template("stuReg.html")

        #code to check tables for existing usernames, emails, and ID num since these should be unique per account
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Students WHERE userID=:un)""",{"un":user})
            checkUser2=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Students WHERE email=:em)""",{"em":email})
            checkEmail2=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Students WHERE sID=:in)""",{"in":idNum})
            checkIDnum2=cur.fetchone()[0]
    
            if (checkUser2 or checkEmail2 or checkIDnum2):
                flash("username, email, or id is already taken")
                return render_template("stuReg.html")

        #student users
            if(accType==2):
                try:
                    cur.execute("""INSERT INTO Students VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",(user,hashPSW,idNum,firstName,lastName,email,tele,year,school,raffleNum, balance, hashWord))
                    conn.commit()
                    flash("Registration Successful for Student User! Please login.")
                    return redirect(url_for('stuLogin'))
                except:
                    return render_template("stuReg.html")
        except Exception as e:
            #print(e, file=sys.stdout)
            render_template("stuReg.html")
    return render_template("stuReg.html")

@app.route("/commReg", methods=["GET","POST"])
def commReg():
    if request.method == "GET":
        return render_template("commReg.html")
    else:
        conn = get_db()
        cur = conn.cursor()
        try:
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
            word = str(request.form["word"])
            hashWord = generate_password_hash(word)
            hashPSW = generate_password_hash(password)
      
        #default account balance
            balance = float(0)
    
            if not word:
                flash("Please choose a secret word")
                return render_template("commReg.html")
        #all users must agree to terms / (todo: create terms in html)
            if not request.form.get("agreement"):
                flash("Please read through and agree to the terms")
                return render_template("commReg.html")

        #check phone #
            if(tele == -1):
                flash("enter a phone #")
                return render_template("commReg.html")

        #check email format
            if('@' not in email):
                flash("invalid email address")
                return render_template("commReg.html")
        #password matching check
            if(password != p2):
                flash("passwords must match")
                return render_template("commReg.html")

       
        #name, email, username, and password are required
            if not firstName:
                flash("Please enter your first name")
                return render_template("commReg.html")
            if not lastName:
                flash("Please enter your last name")
                return render_template("commReg.html")
            if not email:
                flash("Please enter your email")
                return render_template("commReg.html")
            if not user:
                flash("Please select a unique username")
                return render_template("commReg.html")
            if not password:
                flash("Please select a password")
                return render_template("commReg.html")
        #arbitrary length on password limit
            if len(password) > 16:
                flash("Please select a password fewer than sixteen characters")
                return render_template("commReg.html")

        #code to check tables for existing usernames, emails, and ID num since these should be unique per account
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Community WHERE userID=:un)""",{"un":user})
            checkUser3=cur.fetchone()[0]
            cur.execute("""SELECT EXISTS(SELECT 1 FROM Community WHERE email=:em)""",{"em":email})
            checkEmail3=cur.fetchone()[0]
            
            if (checkUser3 or checkEmail3):
                flash("username or email is already taken")
                return render_template("commReg.html")
    
        #community users        
            if(accType==3):
                try:
                    cur.execute("""INSERT INTO Community VALUES (?,?,?,?,?,?,?,?)""",(user,hashPSW,firstName,lastName,email,tele,balance,hashWord))
                    conn.commit()
                    flash("Registration Successful for Community User! Please login.")
                    return redirect(url_for('commLogin'))
                except:
                    return render_template("commReg.html")
                
        except Exception as e:
            #print(e, file=sys.stdout)
            render_template("commReg.html")
    return render_template("commReg.html")
#end registration 

#begin pw reset
@app.route("/passwordHelpHome", methods=["GET","POST"])
def passwordHelpHome():
    if request.method == "GET":
        return render_template("passwordHelpHome.html")

@app.route("/staffHelp", methods=["GET","POST"])
def staffHelp():
    if request.method == "GET":
        return render_template("staffPasswordHelp.html")
    else:
        conn = get_db()
        cur = conn.cursor()
        try:  
            un = request.form.get("user")  
            w = request.form.get("word")
            p1 = request.form.get("p1")
            p2 = request.form.get("p2")
        except:
            w=-1
            p1=-1
            p2=-2

        if ((w or p1) == -1):
            flash(" invalid. Try Again.")
            return render_template("staffPasswordHelp.html")
        if not un:
            flash(" invalid user. Try Again.")
            return render_template("staffPasswordHelp.html")

        if (p1 != p2):
            flash(" passwords do not match")
            return render_template("staffPasswordHelp.html")

        cur.execute("""SELECT wordHash FROM Staff WHERE userID=:un""",{"un":un})
        checkHash1=cur.fetchone()[0]
        if(check_password_hash(checkHash1, w)):
            newHashPSW = generate_password_hash(p1)
            try:
                cur.execute("""UPDATE Staff SET hash=:x WHERE userID=:un""",{"x":newHashPSW,"un":un})
                conn.commit()
                flash("Update Successful for Staff User! Please login.")
                return redirect(url_for('staffLogin'))
            except:
                return render_template("staffPasswordHelp.html")
                
        else:
            flash("invalid credentials. Please try again.")
            return render_template("staffPasswordHelp.html")
   
@app.route("/stuHelp", methods=["GET","POST"])
def stuHelp():
    if request.method == "GET":
        return render_template("stuPasswordHelp.html")
    else:
        conn = get_db()
        cur = conn.cursor()
        try:  
            un = request.form.get("user")  
            w = request.form.get("word")
            p1 = request.form.get("p1")
            p2 = request.form.get("p2")
        except:
            w=-1
            p1=-1
            p2=-2

        if ((w or p1) == -1):
            flash(" invalid. Try Again.")
            return render_template("stuPasswordHelp.html")
        if not un:
            flash(" invalid user. Try Again.")
            return render_template("stuPasswordHelp.html")

        if (p1 != p2):
            flash(" passwords do not match")
            return render_template("stuPasswordHelp.html")

        cur.execute("""SELECT wordHash FROM Students WHERE userID=:un""",{"un":un})
        checkHash1=cur.fetchone()[0]
        if(check_password_hash(checkHash1, w)):
            newHashPSW = generate_password_hash(p1)
            try:
                cur.execute("""UPDATE Students SET hash=:x WHERE userID=:un""",{"x":newHashPSW,"un":un})
                conn.commit()
                flash("Update Successful for Student User! Please login.")
                return redirect(url_for('stuLogin'))
            except:
                return render_template("stuPasswordHelp.html")
    
        else:
            flash("invalid credentials. Please try again.")
            return render_template("stuPasswordHelp.html")
 
@app.route("/commHelp", methods=["GET","POST"])
def commHelp():
    if request.method == "GET":
        return render_template("commPasswordHelp.html")
    else:
        conn = get_db()
        cur = conn.cursor()
        try:  
            un = request.form.get("user")  
            w = request.form.get("word")
            p1 = request.form.get("p1")
            p2 = request.form.get("p2")
        except:
            w=-1
            p1=-1
            p2=-2

        if ((w or p1) == -1):
            flash(" invalid. Try Again.")
            return render_template("commPasswordHelp.html")
        if not un:
            flash(" invalid user. Try Again.")
            return render_template("commPasswordHelp.html")

        if (p1 != p2):
            flash(" passwords do not match")
            return render_template("commPasswordHelp.html")

        cur.execute("""SELECT wordHash FROM Community WHERE userID=:un""",{"un":un})
        checkHash1=cur.fetchone()[0]
        if(check_password_hash(checkHash1, w)):
            newHashPSW = generate_password_hash(p1)
            try:
                cur.execute("""UPDATE Community SET hash=:x WHERE userID=:un""",{"x":newHashPSW,"un":un})
                conn.commit()
                flash("Update Successful for Staff User! Please login.")
                return redirect(url_for('commLogin'))
            except:
                return render_template("commPasswordHelp.html")

        else:
            flash("invalid credentials. Please try again.")
            return render_template("commPasswordHelp.html")
#end pw reset


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

 


