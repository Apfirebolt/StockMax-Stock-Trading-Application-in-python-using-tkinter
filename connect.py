import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="chart_user",
    password="password",
    database="charts"
)

# Check if the connection was successful
if connection.is_connected():
    print("Connected to MySQL database")

    # Create a cursor object
    cursor = connection.cursor()

    # Create a table with username, first_name and last_name columns
    cursor.execute("CREATE TABLE users (username VARCHAR(50), first_name VARCHAR(50), last_name VARCHAR(50))")

    # Close the cursor
    cursor.close()
else:
    print("Connection failed")

# Perform database operations here...

# Close the connection
connection.close()