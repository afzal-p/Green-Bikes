# greenbikesdbms

#database path (for user.db) will have to be changed in main.py\
\
#different commands to run the app: \

FLASK_APP=main.py flask run OR \
FLASK_APP=main.py FLASK_DEBUG=1 flask run OR \
FLASK_APP=main.py flask run \

#to test multiple users: \
localhost:port/rent and \
127.0.0.1:port/  \
(change port)

commands to make the existing tables in the user.db file: \
'sqlite3' to open sqlite  \
'.open user.db' to open db \
'.schema' to see tables in user.db \

CREATE TABLE Staff (userID varchar(255), hash varchar(255), sID INT, first varchar (255), last varchar(255), email varchar(255), phone varchar(255), year INT, wordHash varchar(255), PRIMARY KEY(userID)); \
\
CREATE TABLE Students (userID varchar(255), hash varchar(255), sID INT, first varchar (255), last varchar(255), email varchar(255), phone varchar(255), year INT, school varchar(255), raffleNo tinyint, bal double, wordHash varchar(255), PRIMARY KEY(userID));\
\
CREATE TABLE Community (userID varchar(255), hash varchar(255), first varchar (255), last varchar(255), email varchar(255), phone varchar(255), bal double, wordHash varchar(255), PRIMARY KEY(userID)); \
 \
 CREATE TABLE GB(BikeNo tinyint, model varchar(255), year varchar(255), size tinyint, available boolean, image varchar(255), PRIMARY KEY(BikeNo));
