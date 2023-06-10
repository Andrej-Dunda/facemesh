from flask import Flask, render_template, redirect, request, url_for
from werkzeug.exceptions import abort
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_foto(foto_id):
    conn = get_db_connection()
    foto = conn.execute('SELECT * FROM fotos WHERE id = ?',
                        (foto_id,)).fetchone()
    conn.close()
    if foto is None:
        abort(404)
    return foto

app = Flask(__name__)

@app.route('/login')
def login():
    age = request.args.get('age')
    gender = request.args.get('gender')
    return render_template('login.html', age=age, gender=gender)

@app.route('/index', methods=['POST'])
def index():
    conn = get_db_connection()
    fotos = conn.execute('SELECT * FROM fotos').fetchall()
    conn.close()

    age = request.form.get('age')
    gender = request.form.get('gender')
    return render_template('index.html', fotos=fotos, gender=gender, age=age)

@app.route('/data-table')
def dataTable():
    conn = get_db_connection()
    fotos = conn.execute('SELECT * FROM fotos').fetchall()
    conn.close()
    return render_template('data-table.html', fotos=fotos)

@app.errorhandler(405)
def handle_method_not_allowed_error(error):
    # Perform the redirect to a different URL
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)