# greenbikesdbms

some paths may need to be changed for the database

#different commands to run the app:

FLASK_APP=main.py flask run or
FLASK_APP=main.py FLASK_DEBUG=1 flask run or
FLASK_APP=main.py flask run


#commands to make the existing tables in the user.db file:

CREATE TABLE Staff (userID varchar(255), hash varchar(255), sID INT, first varchar (255), last varchar(255), email varchar(255), phone varchar(255), year INT, PRIMARY KEY(userID));

CREATE TABLE Students (userID varchar(255), hash varchar(255), sID INT, first varchar (255), last varchar(255), email varchar(255), phone varchar(255), year INT, school varchar(255), raffleNo tinyint, bal double, PRIMARY KEY(userID));

CREATE TABLE Community (userID varchar(255), hash varchar(255), first varchar (255), last varchar(255), email varchar(255), phone varchar(255), bal double, PRIMARY KEY(userID));
