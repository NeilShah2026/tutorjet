from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from functools import wraps

#import other functions and classes
from forms import *

#other dependencies
import time
import random

app = Flask(__name__)
app.secret_key = 'some_secret'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'shs'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
from helpers import *

def is_loggin_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

def log_in_user(username):
    users = Table("users", "name", "email", "username", "password")
    user = users.getone("username", username)

    session['logged_in'] = True
    session['username'] = username
    session['name'] = user.get('name')
    session['email'] = user.get('email')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    users = Table("users", "name", "email", "username", "password")

    if request.method == 'POST' and form.validate():
        username = form.username.data
        name = form.name.data
        email = form.email.data

        if isnewuser(username):
            password = str(form.password.data)
            users.insert(name, email, username, password)
            log_in_user(username)
            return redirect(url_for('dashboard'))
        else:
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    #if form is submitted
    if request.method == 'POST':
        #collect form data
        username = request.form['username']
        candidate = request.form['password']

        #access users table to get the user's actual password
        users = Table("users", "name", "email", "username", "password")
        user = users.getone("username", username)
        accPass = user.get('password')

        #if the password cannot be found, the user does not exist
        if accPass is None:
            flash("Username is not found", 'danger')
            return redirect(url_for('login'))
        else:
            #verify that the password entered matches the actual password
            if candidate == accPass:
                #log in the user and redirect to Dashboard page
                log_in_user(username)
                flash('You are now logged in.', 'success')
                return redirect(url_for('dashboard'))   
            else:
                #if the passwords do not match
                flash("Invalid password", 'danger')
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@is_loggin_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@is_loggin_in
def dashboard():
    return render_template('dashboard.html')

@app.route('/requesttutor', methods=['GET', 'POST'])
@is_loggin_in
def requesttutor():
    form = RequestTutor(request.form)
    if request.method == 'POST' and form.validate():
        grade = form.grade.data
        subject = form.subject.data
        description = form.description.data
        email = form.email.data

        requestTutor(grade, subject, description, email)

        flash('Request sent', 'success')
        return redirect(url_for('dashboard'))

    return render_template('requesttutor.html', form=form)

@app.route('/becometutor', methods=['GET', 'POST'])
@is_loggin_in
def becometutor():
    form = BecomeTutor(request.form)
    tutors = Table("tutors", "name", "email", "subject", "grade")
    if request.method == 'POST' and form.validate():
        name = form.name.data
        grade = form.grade.data
        subject = form.subject.data
        email = form.email.data

        if isnewtutor(email):
            tutors.insert(name, email, subject, grade)
            flash('You are now a tutor', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email already exists', 'danger')
            return redirect(url_for('becometutor'))

    return render_template('becometutor.html', form=form)

@app.route('/todo', methods=['GET', 'POST'])
@is_loggin_in
def todo():
    form = ToDoForm(request.form)
    tasks = Table('todo', 'email', 'task', 'code')
    email = session['email']
    if request.method == 'POST' and form.validate():
        task = form.task.data
        # random number to be used as a unique id
        rand = random.randint(1, 1000000)
        tasks.insert(email, task, rand)


        return redirect(url_for('todo'))
    # get all tasks where email = session email
    task_list = tasks.getall()
    # get all tasks where email = session email

    tasks = []
    ids = []
    # loop through all tasks and add the task to the list
    for task in task_list:
        if task.get('email') == email:
            tasks.append(task['task'])
            ids.append(task['code'])
    print(tasks)
    return render_template('todo.html', form=form, tasks=tasks, ids=ids)

# @app.route('/todo/delete/<>', methods=['GET', 'POST'])
# @is_loggin_in
# def delete():

#     tasks = Table('todo', 'email', 'task')
#     email = session['email']
#     if request.method == 'POST' and form.validate():
#         task = form.task.data
#         tasks.delete(email, task)


#         return redirect(url_for('todo'))
#     # get all tasks where email = session email
#     task_list = tasks.getall()
#     # get all tasks where email = session email
#     tasks = []
#     for task in task_list:
#         if task.get('email') == email:
#             tasks.append(task)

#     return render_template('delete.html', form=form, tasks=tasks)

if __name__ == '__main__':
    app.run(debug = True)