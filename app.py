import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # N'oubliez pas de définir une clé secrète pour la session

con = sqlite3.connect("tutorial.db",check_same_thread=False)
logged =False
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
             )''')
cur.execute('''CREATE TABLE IF NOT EXISTS cars (
                year INTEGER NOT NULL,
                make TEXT NOT NULL,
                color TEXT NOT NULL,
                id INTEGER PRIMARY KEY AUTOINCREMENT
             )''')
@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Insert user data into the database
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
        return redirect(url_for('hello'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        
        if user:
            logged = True
            flash('Connexion réussie!', 'success')
            return redirect(url_for('get_cars'))
        else:
            flash('Identifiants invalides. Veuillez réessayer.', 'error')
    return render_template("login.html")



# Modify your add route to handle both GET and POST requests
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        year = request.form['year']
        make = request.form['make']
        color = request.form['color']
        
        # Insert data into the database
        cur.execute("INSERT INTO cars (year, make, color) VALUES (?, ?, ?)", (year, make, color))
        con.commit()
        flash('Car added successfully!')
    return render_template("add.html")


@app.route('/get_cars')
def get_cars():
    global logged  # Ajoutez cette ligne pour indiquer que vous voulez utiliser la variable globale
    
    if not logged:
        return redirect(url_for('login'))
    
    # Le reste de votre code pour récupérer et afficher les voitures

    # Fetch data from the database
    cur.execute("SELECT *,rowid FROM cars")
    cars = cur.fetchall()  # Fetch all rows
    
    # Render the template and pass the retrieved data
    return render_template("cars.html", cars=cars)


@app.route('/delete_car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    if request.method == 'POST':
        cur.execute("DELETE FROM cars WHERE rowid=?", (car_id,))
        con.commit()
        flash('Voiture supprimée avec succès!', 'success')
        return redirect(url_for('get_cars'))


if __name__ == '__main__':
    app.run(debug=True)

