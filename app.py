from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.appointments = []

class Appointment:
    def __init__(self, title, start_time, end_time, location):
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.confirmed = False

users = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User(name, email, password)
        users.append(user)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = next((user for user in users if user.email == email and user.password == password), None)
        if user:
            return redirect(url_for('dashboard', email=email))
    return render_template('login.html')

@app.route('/dashboard/<email>')
def dashboard(email):
    user = next((user for user in users if user.email == email), None)
    if user:
        return render_template('dashboard.html', user=user)
    return redirect(url_for('login'))

@app.route('/appointment/<email>', methods=['GET', 'POST'])
def appointment(email):
    user = next((user for user in users if user.email == email), None)
    if user:
        if request.method == 'POST':
            title = request.form['title']
            start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%dT%H:%M')
            end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%dT%H:%M')
            location = request.form['location']
            appointment = Appointment(title, start_time, end_time, location)
            user.appointments.append(appointment)
            return redirect(url_for('dashboard', email=email))
        return render_template('appointment.html', user=user)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
