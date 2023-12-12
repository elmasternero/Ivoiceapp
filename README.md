Invoice Manager GUI
Description
Invoice Manager GUI is a desktop application developed in Python using Tkinter and MySQL. It allows users to manage invoices, including features to insert, modify, and view invoice data.

Environment Setup
Requirements
Python 3.x
MySQL Server
Python Libraries: mysql-connector-python, tkinter
Installing Dependencies
To install necessary dependencies, run the following command:

bash
Copy code
pip install mysql-connector-python
Tkinter usually comes pre-installed with Python. If not installed, please refer to the official Python documentation for installation.

Database Setup
MySQL Installation: Ensure MySQL Server is installed on your machine. If not, download it from MySQL Downloads.

Creating the Database: Launch MySQL and create a new database for the project:

sql
Copy code
CREATE DATABASE facturacion;
Creating the Invoices Table: Within the facturacion database, create a table to store invoices:

sql
Copy code
USE facturacion;

CREATE TABLE facturas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    provider VARCHAR(255) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    yield DATE NOT NULL
);
Database Connection Configuration: In your project file (usually funciones.py), make sure to configure the database connection details:

python
Copy code
def connect_to_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='facturacion',
            user='YOUR_USERNAME',
            password='YOUR_PASSWORD'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
Replace 'YOUR_USERNAME' and 'YOUR_PASSWORD' with your MySQL credentials.

Running the Project: Run your Python application. You should be able to connect to the database and perform operations.

Using the Application
To insert a new invoice, select the 'Insert Invoice' option.
To modify an existing invoice, use the 'Modify Invoice' option.
To view invoices, choose 'View Database'.
