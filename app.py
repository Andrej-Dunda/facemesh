import random
from flask import Flask, render_template, redirect, request, url_for, session
from werkzeug.exceptions import abort
import sqlite3

# Establishes the connection with the database
def get_db_connection():
    conn = sqlite3.connect('foto_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fetches and returns a pair of two random fotos from the database
def get_random_foto_pair():
    conn = get_db_connection()

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fotos")
    total_rows = cursor.fetchone()[0]

    index1 = random.randint(0, total_rows - 1)
    index2 = random.randint(0, total_rows - 1)

    while index2 == index1:
      index2 = random.randint(0, total_rows - 1)

    cursor.execute("SELECT * FROM fotos LIMIT 1 OFFSET ?", (index1,))
    foto1 = cursor.fetchone()

    cursor.execute("SELECT * FROM fotos LIMIT 1 OFFSET ?", (index2,))
    foto2 = cursor.fetchone()

    cursor.close()
    conn.close()
    if foto1 is None or foto2 is None:
        abort(404)
    return [foto1, foto2]

# Fetches and returns a data row for a certain foto based on the given foto_id
def get_foto(foto_id):
    conn = get_db_connection()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fotos WHERE foto_id = ?", (foto_id,))
    foto = cursor.fetchone()

    cursor.close()
    conn.close()
    if foto is None:
        abort(404)
    return foto

app = Flask(__name__)
app.secret_key = 'ff932ab9b2ecb7e5db6592992172cb648832de06e8cb6628'

# Login protocol - sets the age and gender of the user for the whole application
@app.route('/login', methods=['POST'])
def login():
    age = request.form.get('age')
    gender = request.form.get('gender')

    if age and gender:
        session['age'] = age
        session['gender'] = gender
    return redirect('/index')

# Login form route - user selects their age and gender here
@app.route('/')
def login_form():
    age = session.get('age')
    gender = session.get('gender')
    return render_template('login.html', age=age, gender=gender)

# Main page - this is where the user selects between fotos from random pairs of pictures, the results are saved in the database
@app.route('/index')
def index():
    age = session.get('age')
    gender = session.get('gender')
    
    [foto1, foto2] = get_random_foto_pair()

    return render_template('index.html', foto1=foto1, foto2=foto2, age=age, gender=gender)

# This page shows a table of all fotos and their elo ratings
@app.route('/data-table')
def dataTable():
    conn = get_db_connection()
    fotos = conn.execute('SELECT * FROM fotos').fetchall()
    conn.close()
    return render_template('data-table.html', fotos=fotos)

# Protocol for updating the elo ratings of the fotos
@app.route('/edit')
def edit():
    winning_foto = get_foto(request.args.get('winning_foto_id'))
    losing_foto = get_foto(request.args.get('losing_foto_id'))
    elo_change = random.randint(1, 20)

    conn = get_db_connection()

    # Update winning foto
    conn.execute('UPDATE fotos SET elo_general = ?, elo_male = ?, elo_female = ? WHERE foto_id = ?',
                  (winning_foto['elo_general'] + elo_change, winning_foto['elo_male'] + elo_change, winning_foto['elo_female'] + elo_change, winning_foto['foto_id'] + elo_change))
    # Update losing foto
    conn.execute('UPDATE fotos SET elo_general = ?, elo_male = ?, elo_female = ? WHERE foto_id = ?',
                  (losing_foto['elo_general'] - elo_change, losing_foto['elo_male'] - elo_change, losing_foto['elo_female'] - elo_change, losing_foto['foto_id'] - elo_change))
    conn.commit()
    conn.close()
    return redirect('/index')

# Error handler for "Method not allowed" errors
@app.errorhandler(405)
def handle_method_not_allowed_error(error):
    # Perform the redirect to a different URL
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
