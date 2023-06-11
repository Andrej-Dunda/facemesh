import sqlite3
import os

# Connect to the database
connection = sqlite3.connect('foto_database.db')

# Execute the schema script
with open('foto_db_schema.sql') as f:
    connection.executescript(f.read())

# Create a cursor
cur = connection.cursor()

# Directory containing the .jpg files
directory = 'C:/Users/dunda/Programs/facemesh/static/images'

# Iterate over the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.jpg'):
        # Insert the file name into the database
        cur.execute("INSERT INTO fotos (file_name) VALUES (?)", (filename,))

# Commit the changes and close the connection
connection.commit()
connection.close()
