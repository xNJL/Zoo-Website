# README

This project was realized during the Fall 2018 term for the CS-4400 course at the Georgia Institute of Technology.
It consists of a website managing the database for a Zoo.

## How to Run

### 1) Install Requirements

pip install -r requirements.txt

### 2) MySQL Setup

##### On Mac

From terminal:

1) /usr/local/mysql/bin/mysql -u root -p
2) CREATE USER 'test'@'localhost' IDENTIFIED BY 'test';
3) GRANT ALL PRIVILEGES ON * . * TO 'test'@'localhost';

##### On Ubuntu

From terminal:

1) mysql -u root -p
2) CREATE USER 'test'@'localhost' IDENTIFIED BY 'test';
3) GRANT ALL PRIVILEGES ON * . * TO 'test'@'localhost';

### 3) Run the files create_fake_db.py and populate_db.py located in the /database folder

This will create a db and populate it with some data.

### 4) Run the file __init__.py located in the /App folder

### 5) Visit http://127.0.0.1:5000/login and log in

You can find credentials in the User.csv file located in the /database folder.

Example (username password email):
- martha_johnson password1 marthajohnson@hotmail.com will log you as a staff member
- robert_bernheardt password7 robertbernheardt@yahoo.com will log you as a visitor 
- admin1 adminpassword adminemail@mail.com will log you as an admin 

Alternatively, you can register either as a visitor or a staff member.


