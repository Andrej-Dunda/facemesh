import random
from flask import Flask, render_template, redirect, request, send_file, url_for, session
from werkzeug.exceptions import abort
import sqlite3
import pandas as pd
from datetime import datetime

# Establishes the connection with the foto database
def get_foto_db_connection():
    conn = sqlite3.connect('foto_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Establishes the connection with the user database
def get_user_db_connection():
    conn = sqlite3.connect('user_database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Fetches and returns a pair of two random fotos from the database
def get_random_foto_pair():
    conn = get_foto_db_connection()

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
    conn = get_foto_db_connection()

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fotos WHERE foto_id = ?", (foto_id,))
    foto = cursor.fetchone()

    cursor.close()
    conn.close()
    if foto is None:
        abort(404)
    return foto

def evaluate_encounter_result(winner, loser, gender):
    # New fotos that will be returned with updated values
    updated_winner = winner
    updated_loser = loser
    
    # general encounters count increment
    updated_winner['general_encounters_count'] += 1
    updated_loser['general_encounters_count'] += 1

    # general elo calculation and update
    winner_general_k_factor = evaluate_k_factor(winner['general_encounters_count'], winner['general_reached_2400'])
    loser_general_k_factor = evaluate_k_factor(loser['general_encounters_count'], loser['general_reached_2400'])
    general_elo_change = count_elo_change(winner['elo_general'], loser['elo_general'], winner_general_k_factor, loser_general_k_factor)
    updated_winner['elo_general'] += general_elo_change[0]
    updated_loser['elo_general'] += general_elo_change[1]

    if updated_winner['elo_general'] >= 2400:
        updated_winner['general_reached_2400'] = 1
    if updated_loser['elo_general'] >= 2400:
        updated_loser['general_reached_2400'] = 1

    # determines if we update the male or female parts of the foto (elo and encounters count)
    if gender == "Žena":
        # female encounters count increment
        updated_winner['female_encounters_count'] += 1
        updated_loser['female_encounters_count'] += 1

        # female elo calculation and update
        winner_female_k_factor = evaluate_k_factor(winner['female_encounters_count'], winner['female_reached_2400'])
        loser_female_k_factor = evaluate_k_factor(loser['female_encounters_count'], loser['female_reached_2400'])
        female_elo_change = count_elo_change(winner['elo_female'], loser['elo_female'], winner_female_k_factor, loser_female_k_factor)
        updated_winner['elo_female'] += female_elo_change[0]
        updated_loser['elo_female'] += female_elo_change[1]

        if updated_winner['elo_female'] >= 2400:
            updated_winner['female_reached_2400'] = 1
        if updated_loser['elo_female'] >= 2400:
            updated_loser['female_reached_2400'] = 1

        return [updated_winner, updated_loser]
    
    # male encounters count increment
    updated_winner['male_encounters_count'] += 1
    updated_loser['male_encounters_count'] += 1

    # male elo calculation and update
    winner_male_k_factor = evaluate_k_factor(winner['male_encounters_count'], winner['male_reached_2400'])
    loser_male_k_factor = evaluate_k_factor(loser['male_encounters_count'], loser['male_reached_2400'])
    male_elo_change = count_elo_change(winner['elo_male'], loser['elo_male'], winner_male_k_factor, loser_male_k_factor)
    updated_winner['elo_male'] += male_elo_change[0]
    updated_loser['elo_male'] += male_elo_change[1]

    if updated_winner['elo_male'] >= 2400:
        updated_winner['male_reached_2400'] = 1
    if updated_loser['elo_male'] >= 2400:
        updated_loser['male_reached_2400'] = 1

    return [updated_winner, updated_loser]

def count_elo_change(winner_elo, loser_elo, winner_k_factor, loser_k_factor):
  r1 = 10**(winner_elo/400)
  r2 = 10**(loser_elo/400)
  E1 = r1 / (r1 + r2)
  E2 = r2 / (r2 + r1)
  winner_elo_change = round(winner_k_factor * (1 - E1))
  loser_elo_change = round(loser_k_factor * (0 - E2))
  return [winner_elo_change, loser_elo_change]

def evaluate_k_factor(encounters_count, reached_2400):
    if encounters_count < 30:
        return 30
    elif not reached_2400:
        return 15
    return 10

app = Flask(__name__)
app.secret_key = 'ff932ab9b2ecb7e5db6592992172cb648832de06e8cb6628'

# Login protocol - sets the age and gender of the user for the whole application
@app.route('/login', methods=['POST'])
def login():
    age = request.form.get('age')
    gender = request.form.get('gender')

    if age and gender:
        if age != session.get('age') or gender != session.get('gender'):
          session['age'] = age
          session['gender'] = gender

          conn = get_user_db_connection()
          cur = conn.cursor()
          cur.execute("INSERT INTO users (user_age, user_gender, user_timestamp) VALUES (?, ?, ?)", (age, gender, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
          print(f"\n\n\nNew user inserted\nAge: {age}\nGender: {gender}\n\n\n")

          conn.commit()
          conn.close()
        return redirect('/index')
    return redirect('/')


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
@app.route('/foto-data-table')
def fotoDataTable():
    conn = get_foto_db_connection()
    fotos = conn.execute('SELECT * FROM fotos').fetchall()
    conn.close()
    return render_template('foto-data-table.html', fotos=fotos)

# This page shows a table of all users and their ages and gender
@app.route('/user-data-table')
def userDataTable():
    conn = get_user_db_connection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('user-data-table.html', users=users)

# Protocol for updating the elo ratings of the fotos based on the result of the encounter
@app.route('/edit')
def edit():
    winner = get_foto(request.args.get('winner_foto_id'))
    loser = get_foto(request.args.get('loser_foto_id'))

    processed_winner = {
        'foto_id': winner['foto_id'],
        'file_name': winner['file_name'],
        'elo_general': winner['elo_general'],
        'elo_male': winner['elo_male'],
        'elo_female': winner['elo_female'],
        'general_encounters_count': winner['general_encounters_count'],
        'male_encounters_count': winner['male_encounters_count'],
        'female_encounters_count': winner['female_encounters_count'],
        'general_reached_2400': winner['general_reached_2400'],
        'male_reached_2400': winner['male_reached_2400'],
        'female_reached_2400': winner['female_reached_2400']
    }
    
    processed_loser = {
        'foto_id': loser['foto_id'],
        'file_name': loser['file_name'],
        'elo_general': loser['elo_general'],    
        'elo_male': loser['elo_male'],
        'elo_female': loser['elo_female'],
        'general_encounters_count': loser['general_encounters_count'],
        'male_encounters_count': loser['male_encounters_count'],
        'female_encounters_count': loser['female_encounters_count'],
        'general_reached_2400': loser['general_reached_2400'],
        'male_reached_2400': loser['male_reached_2400'],
        'female_reached_2400': loser['female_reached_2400']
    }

    [updated_winner, updated_loser] = evaluate_encounter_result(processed_winner, processed_loser, session.get('gender'))

    conn = get_foto_db_connection()

    # Update winner foto
    conn.execute('UPDATE fotos SET elo_general = ?, elo_male = ?, elo_female = ?, general_encounters_count = ?, male_encounters_count = ?, female_encounters_count = ?, general_reached_2400 = ?, male_reached_2400 = ?, female_reached_2400 = ? WHERE foto_id = ?',
                  (updated_winner['elo_general'], updated_winner['elo_male'], updated_winner['elo_female'], updated_winner['general_encounters_count'], updated_winner['male_encounters_count'], updated_winner['female_encounters_count'], updated_winner['general_reached_2400'], updated_winner['male_reached_2400'], updated_winner['female_reached_2400'], updated_winner['foto_id']))
    # Update loser foto
    conn.execute('UPDATE fotos SET elo_general = ?, elo_male = ?, elo_female = ?, general_encounters_count = ?, male_encounters_count = ?, female_encounters_count = ?, general_reached_2400 = ?, male_reached_2400 = ?, female_reached_2400 = ? WHERE foto_id = ?',
                  (updated_loser['elo_general'], updated_loser['elo_male'], updated_loser['elo_female'], updated_loser['general_encounters_count'], updated_loser['male_encounters_count'], updated_loser['female_encounters_count'], updated_loser['general_reached_2400'], updated_loser['male_reached_2400'], updated_loser['female_reached_2400'], updated_loser['foto_id']))
    conn.commit()
    conn.close()
    return redirect('/index')

# Exports the table of fotos to Excel
@app.route('/export-fotos')
def export_foto_table():
    conn = get_foto_db_connection()
    # Query the database and retrieve data into a DataFrame
    query = "SELECT * FROM fotos"
    df = pd.read_sql_query(query, conn)
    
    # Save DataFrame to an Excel file
    excel_file = 'fotos-table.xlsx'
    df.to_excel(excel_file, index=False)

    # Close the database connection
    conn.close()
    
    # Send the Excel file for download
    return send_file(excel_file, as_attachment=True)

# Exports the table of users to Excel
@app.route('/export-users')
def export_users_table():
    conn = get_user_db_connection()
    # Query the database and retrieve data into a DataFrame
    query = "SELECT * FROM users"
    df = pd.read_sql_query(query, conn)
    
    # Save DataFrame to an Excel file
    excel_file = 'users-table.xlsx'
    df.to_excel(excel_file, index=False)

    # Close the database connection
    conn.close()
    
    # Send the Excel file for download
    return send_file(excel_file, as_attachment=True)

@app.route('/delete-user-log', methods=['DELETE'])
def delete_user_log():
    delete_user_log_id = request.args.get('delete_log_id')

    conn = get_user_db_connection()
    cursor = conn.cursor()

    # Execute the DELETE statement
    cursor.execute("DELETE FROM users WHERE user_id = ?", (delete_user_log_id,))

    conn.commit()
    conn.close()

    return 'User deleted successfully', 200

# Error handler for "Method not allowed" errors
@app.errorhandler(405)
def handle_method_not_allowed_error(error):
    return redirect('/')

# Error handler for "Page not found" errors
@app.errorhandler(404)
def handle_method_not_allowed_error(error):
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
