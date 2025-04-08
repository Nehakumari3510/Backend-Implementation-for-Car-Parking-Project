# Complete Guide to Setup Backend Server in Flask for Car parking Project

## Getting Started

This guide will walk you through the steps to set up Android Studio and run this project on your machine.

## 1. Steps to Clone Project Inside Your Local Machine

 a. **Make sure you have Git Installed in your system.**

 b. Copy the follwing link and run it in you terminal.

    git clone https://github.com/Nehakumari3510/Backend-Implementation-for-Car-Parking-Project.git
        

 c. Now you can open that project in your VS code or any other editor of your choice-
    
## 2. Steps to Connect the Backend to the Database(PostgreSQL)

 a. Inside your pgAdmin (the GUI tool of PostgreSQL) you have one default user with name postgres you can use that or can create another if you need.

 b. Inside that user you need to create one database with name parking_db or you can change the name if you want then you need to change those configurations in your flask code accordingly.

 c. Then use the following code inside the terminal where you project is running to create all the tables needed for the backend.
   
    from solution3 import db, app  

    with app.app_context():
    db.create_all()

    print("Tables created successfully!")

 This code will create all the necessary tables

**Now you can run your backend code and one more thing to keep in mind that you need to change the port in frontend with the port on which Flask server is running.**
