from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ml_model import predict_disease, predict_noshow
from datetime import date
import sqlite3
import os
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'medibook_secret_123'

DATABASE = 'appointment.db'

SYMPTOMS_LIST = [
    'fever', 'cough', 'headache', 'fatigue', 'body_pain',
    'sore_throat', 'runny_nose', 'chest_pain', 'shortness_of_breath',
    'nausea', 'vomiting', 'diarrhea', 'skin_rash', 'joint_pain', 'dizziness'
]

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'patient',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT,
        available_days TEXT,
        available_time TEXT
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        doctor_id INTEGER,
        appointment_date TEXT NOT NULL,
        appointment_time TEXT NOT NULL,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (doctor_id) REFERENCES doctors(id)
    )''')

    cur.execute("SELECT COUNT(*) FROM doctors")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO doctors (name, specialty, available_days, available_time) VALUES (?,?,?,?)", [
            ('Dr. Priya Sharma', 'General Physician', 'Mon-Fri', '9AM-5PM'),
            ('Dr. Rohan Mehta', 'Cardiologist', 'Mon-Wed-Fri', '10AM-3PM'),
            ('Dr. Anita Nair', 'Dermatologist', 'Tue-Thu', '11AM-4PM'),
        ])

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = generate_password_hash(request.form['password'])
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        if user:
            flash('Email already registered!', 'danger')
        else:
            cur.execute("INSERT INTO users (name, email, password) VALUES (?,?,?)",
                        (name, email, password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            conn.close()
            return redirect(url_for('login'))
        conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user['password'], password):
            session['user_id']   = user['id']
            session['user_name'] = user['name']
            session['role']      = user['role']
            conn.close()
            return redirect(url_for('dashboard'))
        flash('Invalid email or password!', 'danger')
        conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()
    if request.method == 'POST':
        doctor_id        = request.form['doctor_id']
        appointment_date = request.form['date']
        appointment_time = request.form['time']
        reason           = request.form['reason']
        cur.execute("""INSERT INTO appointments
                       (user_id, doctor_id, appointment_date, appointment_time, reason)
                       VALUES (?,?,?,?,?)""",
                    (session['user_id'], doctor_id, appointment_date, appointment_time, reason))
        conn.commit()
        conn.close()
        return redirect(url_for('success'))
    conn.close()
    return render_template('book.html', doctors=doctors)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    if session['role'] == 'admin':
        cur.execute("""SELECT a.*, u.name as patient_name, d.name as doctor_name
                       FROM appointments a
                       JOIN users u ON a.user_id=u.id
                       JOIN doctors d ON a.doctor_id=d.id
                       ORDER BY a.appointment_date DESC""")
    else:
        cur.execute("""SELECT a.*, d.name as doctor_name, d.specialty
                       FROM appointments a
                       JOIN doctors d ON a.doctor_id=d.id
                       WHERE a.user_id=?
                       ORDER BY a.appointment_date DESC""",
                    (session['user_id'],))
    appointments = cur.fetchall()
    conn.close()
    return render_template('dashboard.html', appointments=appointments)

@app.route('/cancel/<int:id>')
def cancel(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE appointments SET status='cancelled' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Appointment cancelled successfully.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/confirm/<int:id>')
def confirm(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Admin access only!', 'danger')
        return redirect(url_for('index'))
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE appointments SET status='confirmed' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Appointment confirmed successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction          = None
    specialty           = None
    recommended_doctors = []

    if request.method == 'POST':
        selected = request.form.getlist('symptoms')
        if selected:
            prediction, specialty = predict_disease(selected)
            conn = get_db()
            cur  = conn.cursor()
            cur.execute("SELECT * FROM doctors WHERE specialty=?", (specialty,))
            recommended_doctors = cur.fetchall()
            conn.close()

    return render_template('predict.html',
                           symptoms_list=SYMPTOMS_LIST,
                           prediction=prediction,
                           specialty=specialty,
                           doctors=recommended_doctors)

@app.route('/admin/noshow')
def noshow():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Admin access only!', 'danger')
        return redirect(url_for('index'))
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("""SELECT a.*, u.name as patient_name, d.name as doctor_name
                   FROM appointments a
                   JOIN users u ON a.user_id=u.id
                   JOIN doctors d ON a.doctor_id=d.id
                   WHERE a.status='pending'""")
    appointments = cur.fetchall()
    conn.close()
    results = []
    today = date.today().strftime('%Y-%m-%d')
    for appt in appointments:
        risk = predict_noshow(appt['appointment_date'], today, appt['appointment_time'])
        results.append({'appt': appt, 'risk': risk})
    return render_template('noshow.html', results=results)

@app.route('/admin/doctors')
def manage_doctors():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Admin access only!', 'danger')
        return redirect(url_for('index'))
    conn = get_db()
    cur  = conn.cursor()
    cur.execute("SELECT * FROM doctors ORDER BY specialty")
    doctors = cur.fetchall()
    conn.close()
    return render_template('manage_doctors.html', doctors=doctors)

@app.route('/admin/doctors/add', methods=['POST'])
def add_doctor():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Admin access only!', 'danger')
        return redirect(url_for('index'))
    name            = request.form['name']
    specialty       = request.form['specialty']
    available_days  = request.form['available_days']
    available_time  = request.form['available_time']
    if not name or not specialty:
        flash('Name and specialty are required!', 'danger')
        return redirect(url_for('manage_doctors'))
    conn = get_db()
    conn.execute("INSERT INTO doctors (name, specialty, available_days, available_time) VALUES (?,?,?,?)",
                 (name, specialty, available_days, available_time))
    conn.commit()
    conn.close()
    flash(f'Dr. {name} added successfully!', 'success')
    return redirect(url_for('manage_doctors'))

@app.route('/admin/doctors/delete/<int:id>')
def delete_doctor(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        flash('Admin access only!', 'danger')
        return redirect(url_for('index'))
    conn = get_db()
    conn.execute("DELETE FROM doctors WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash('Doctor removed successfully!', 'info')
    return redirect(url_for('manage_doctors'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
