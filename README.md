# greenbikesdbms

#database path (for user.db) will have to be changed in main.py \n

#different commands to run the app: \n

FLASK_APP=main.py flask run OR \\
FLASK_APP=main.py FLASK_DEBUG=1 flask run OR \n
FLASK_APP=main.py flask run \\


commands to make the existing tables in the user.db file: \n
'sqlite3' to open sqlite  \n
'.open user.db' to open db \n
'.schema' to see tables in user.db \n

CREATE TABLE Staff (userID varchar(255), hash varchar(255), sID INT, first varchar (255), last varchar(255), email varchar(255), phone varchar(255), year INT, wordHash varchar(255), PRIMARY KEY(userID));

CREATE TABLE Students (userID varchar(255), hash varchar(255), sID INT, first varchar (255), last varchar(255), email varchar(255), phone varchar(255), year INT, school varchar(255), raffleNo tinyint, bal double, wordHash varchar(255), PRIMARY KEY(userID));

CREATE TABLE Community (userID varchar(255), hash varchar(255), first varchar (255), last varchar(255), email varchar(255), phone varchar(255), bal double, wordHash varchar(255), PRIMARY KEY(userID));
