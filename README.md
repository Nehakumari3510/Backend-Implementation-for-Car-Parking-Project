## Python CRUD App with MySQL
## Parking Management System 

This project is a Flask-based Parking Management System that uses MySQL as the database to manage floors, rows, slots, users, and parking reservations. It includes APIs for parking cars, removing cars, and displaying the parking lot structure.

## Features

Relational Database Structure: Models for floors, rows, slots, users, reservations, and parking sessions.

RESTful API Endpoints:

Display the parking lot structure.

Park a car.

Remove a car by ticket ID.

MySQL Integration: Uses Flask-SQLAlchemy and PyMySQL to connect to MySQL.



## ChatGpt conversation**

Word file attached on GitHub if you have any query so you can check word file on GitHub. there is mention how we create this code.   

## Prerequisites

- Python (3.7 or later)

- MySQL

- Flask

- Flask-SQLAlchemy

- PyMySQL

## commands for install python -

sudo dnf install python3


## commands for install MYSQL -
-pip install mysql-connector-python or download from browser 
pip install pymysql
pip install sqlalchemy

## commands for push the data to GitHub -
- git init
- git add .
- git commit -m "Initial commit"
- git remote add origin https://github.com/Khalid-IBS/parking_lot.git
- git branch -M main
- git push -u origin main
- git add .
- git commit -m "Your commit message"
- git push

   
# DATABASE SETUP-

## First create the database name in your mysql workbench by run as below mention**

CREATE DATABASE parking_db;       ## name whatever you want.


## then type in your MYSQL workbench as below mention**

USE parking_db;

## then your SCHEMA (folder name in your MYSQL workbench) is ready to create the table**

## Create the `floors` table by run data as below mention** 


CREATE TABLE floors (
    floor_id INT AUTO_INCREMENT PRIMARY KEY,
    floor_name VARCHAR(50) NOT NULL
);


## Create the `users` table by run data as below mention** 


CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(50),
    address VARCHAR(255),
    registration_no VARCHAR(20)
);

## Create the `rows` table  by run data as below mention (use backticks around `rows` because it is a reserved keyword) **


CREATE TABLE `rows` (
    row_id INT AUTO_INCREMENT PRIMARY KEY,
    floor_id INT NOT NULL,
    row_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (floor_id) REFERENCES floors(floor_id) ON DELETE CASCADE
);

## Create the `slots` table by run data as below mention**


CREATE TABLE slots (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    row_id INT NOT NULL,
    slot_name VARCHAR(50) NOT NULL,
    status INT DEFAULT 1, -- 0 = Occupied, 1 = Free, 2 = Not in use
    vehicle_reg_no VARCHAR(20),
    ticket_id VARCHAR(20),
    user_id INT,
    FOREIGN KEY (row_id) REFERENCES `rows`(row_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

## Create the `reservations` table by run data as below mention**


CREATE TABLE reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_id INT NOT NULL,
    hour INT NOT NULL,
    reserved BOOLEAN NOT NULL,
    user_id INT,
    FOREIGN KEY (slot_id) REFERENCES slots(slot_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

## Create the `parkingsessions` table by run data as below mention**
CREATE TABLE parkingsessions (
    ticket_id VARCHAR(20) PRIMARY KEY,
    slot_id INT NOT NULL,
    vehicle_reg_no VARCHAR(20),
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    user_id INT,
    FOREIGN KEY (slot_id) REFERENCES slots(slot_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


## Configure the database in your code: In the respective Python file (app_mysql.py for MySQL or app.py for PostgreSQL), update the db_config object with your database credentials:

db_config = {
    'host': 'localhost',
    'user': '<your-username>',  # Use your MySQL
    'password': '<your-password>',  # Your MySQL password
    'dbname': 'parking_db'  # The database name
}

# Run the Application:

python3 solution6.py


## Usage
Once the app is running, you can interact with it through your browser at http://localhost:5000.



=======
# parking_lot
>>>>>>> 51f70788ebe9f69305c81901e29d5e2bf1e3d0c9
