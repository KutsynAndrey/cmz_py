# Online judge for Competitive Programming problems.

## Installing environment

* **git clone https://github.com/KutsynAndrey/cmz_py.git**
* **cd cmz_py**
* **python3 -m venv venv**
* **source venv/bin/activate**
* **pip3 install -r requirements.txt**

## Setup and connect database
### Installing
* **sudo apt-get update**
* **sudo apt-get install mysql-server**
* **sudo mysql**
### Creating user in mySQL
* **CREATE USER (username)@(host) IDENTIFIED BY (password);** (Where (username), (host) and (password) is variables. If mySQL says, that the password "does not satisfy the current policy requirements." you should change password limits as follows: *SET GLOBAL validate_password.length = 6;* and *SET GLOBAL validate_password.number_count = 0;*
* **GRANT ALL PRIVILEGES ON * . * TO (username)@(host);**
### Connecting to database from python
* Open script db.py (in folder /app)
* Change params in fifth line of code according to your password, host and username. (Instead of (connector) write *mysqlconnector*. If you use database on system, where you start flask app, write (localhost) in place with host variable)

## Running app
* **python3 Mysite.py**

## Adding problems to database
* Only admins can add problems and other admins to database, so you should add first admin manually to the database.
