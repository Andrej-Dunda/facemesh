import sqlite3
from datetime import datetime
# import os

# Connect to the database
connection = sqlite3.connect('user_database.db')

# Execute the schema script
with open('user_db_schema.sql') as f:
    connection.executescript(f.read())

# # Create a cursor
cur = connection.cursor()

# for i in range(40):
#   cur.execute("INSERT INTO users (user_age, user_gender, user_timestamp) VALUES (?, ?, ?)", (18, "Muž", datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))

# # Commit the changes and close the connection
connection.commit()
connection.close()
