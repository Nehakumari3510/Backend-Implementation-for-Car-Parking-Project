<<<<<<< HEAD
# Python CRUD App with MySQL

## Description

This is a simple python CRUD application that manages a parking_lot stored in a database. The app supports**MySQL**, allowing users to create, read, put, and delete vehicle. Depending on your database preference, the app will automatically direct you to use **app_mysql.py** (for MySQL).

## Prerequisites

Ensure the following are installed on your system:
- Python 3.x
- Flask (framework)
- MySQL


## Technologies Used

- python (Backend Framework)
- **MySQL**:
- mysql-connector-python (MySQL driver for Python)

## commands for install packages-
sudo dnf install python3
-pip install mysql-connector-python or download from browser   

   
# DATABASE SETUP-

**create a database**
CREATE DATABASE parking_db;

**Create the table in the parking_db database:**
-- Create the database
CREATE DATABASE IF NOT EXISTS parking_db;

-- Use the database
USE parking_db;

-- Create the `floors` table
CREATE TABLE floors (
    floor_id INT AUTO_INCREMENT PRIMARY KEY,
    floor_name VARCHAR(50) NOT NULL
);

-- Create the `users` table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone_number VARCHAR(50),
    address VARCHAR(255),
    registration_no VARCHAR(20)
);

-- Create the `rows` table (use backticks around `rows` because it is a reserved keyword)
CREATE TABLE `rows` (
    row_id INT AUTO_INCREMENT PRIMARY KEY,
    floor_id INT NOT NULL,
    row_name VARCHAR(50) NOT NULL,
    FOREIGN KEY (floor_id) REFERENCES floors(floor_id) ON DELETE CASCADE
);

-- Create the `slots` table
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

-- Create the `reservations` table
CREATE TABLE reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    slot_id INT NOT NULL,
    hour INT NOT NULL,
    reserved BOOLEAN NOT NULL,
    user_id INT,
    FOREIGN KEY (slot_id) REFERENCES slots(slot_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Create the `parkingsessions` table
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
