from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from utils import *
from database import DataBase


app = Flask(__name__)

def get_bd():
    return DataBase()

@app.route('/')
def hello():
    num = generate_rd_n()
    return render_template('welcome.html', num=num)

@app.route('/signin', methods = ['POST', 'GET'])
def signin():
    num = generate_rd_n()
    # if current_user.is_authenticated:
    #     return redirect('/blogs')
    if request.method == 'POST':
        # A list to append all the possible issues to notify
        notifications = []

        username = request.form['username'].strip()
        password = request.form['password']
        password2 = request.form['r-password']
        db = get_bd()
        user = db.get_user(username)
        
        if len(username) < 3:
            notifications.append("The username is too short")
        if user.username != '':
            notifications.append("The username already exist")
        if password != password2:
            notifications.append("The passwords do not match")
        if len(password) < 5:
            notifications.append("The password need more than 5 letters")
        if len(notifications) == 0:
            user = User(username,generate_password_hash(password),'beginner')
            print(user)
            db.add_user(user)
            db.connection.close()

            # iniciar sesion (token)
            #ocultar datos de la url
            return redirect(url_for('play'))
        else:
            #Pasar la lista de notifications y printearlas todas
            return render_template('signin.html', num=num, page="Sign in",issues=notifications)
    return render_template('signin.html', num=num, page="Sign in",issues=[])

@app.route('/login', methods = ['POST', 'GET'])
def login():
    num = generate_rd_n()
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']


        db = get_bd()
        user = db.get_user(username)
        db.connection.close()
        if user.username == '':
            return render_template('signin.html', num=num, page="Log in",
                issues=['This user does not exist'])
        if check_password_hash(user.psw_hash,password):
            print('OLEE')
            # iniciar sesion (token)
            #ocultar datos de la url
            return redirect(url_for('play'))
        else:
            return render_template('signin.html', num=num, page="Log in",
                issues=['The password is incorrect'])

    return render_template('signin.html', num=num, page="Log in",issues=[])

@app.route("/play")
def play():
    return "Play!"

if __name__ == "__main__":
    app.run(debug = True)  