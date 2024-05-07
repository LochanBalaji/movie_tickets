
"""
Created on Tue May  7 09:55:24 2024

@author: Lochan
"""

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('movies.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                (id INTEGER PRIMARY KEY, name TEXT NOT NULL, show_time TEXT NOT NULL, price REAL NOT NULL)''')
conn.commit()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM movies LIMIT 1")
    movie = cursor.fetchone()
    return render_template('index.html', movie=movie)

@app.route('/movies')
def movies():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return render_template('movies.html', movies=movies)

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        name = request.form['movie_name']
        show_time = request.form['movie_show_time']
        price = request.form['movie_price']
        cursor.execute("INSERT INTO movies (name, show_time, price) VALUES (?, ?, ?)", (name, show_time, price))
        conn.commit()
        return redirect(url_for('movies'))
    return render_template('add_movie.html')

@app.route('/update_movie/<int:id>', methods=['GET', 'POST'])
def update_movie(id):
    if request.method == 'POST':
        name = request.form['movie_name']
        show_time = request.form['movie_show_time']
        price = request.form['movie_price']
        cursor.execute("UPDATE movies SET name=?, show_time=?, price=? WHERE id=?", (name, show_time, price, id))
        conn.commit()
        return redirect(url_for('movies'))
    cursor.execute("SELECT * FROM movies WHERE id=?", (id,))
    movie = cursor.fetchone()
    return render_template('update_movie.html', movie=movie)

@app.route('/delete_movie/<int:id>', methods=['POST'])
def delete_movie(id):
    cursor.execute("DELETE FROM movies WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for('movies'))

if __name__ == '__main__':
    app.run(debug=True)
