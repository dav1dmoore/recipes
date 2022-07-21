from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['post'])
def register():
    print(request.form)
    if User.validate_user(request.form):
        print("registration OK")
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }

        user = User.create_user(data)
        print(user)
        session['user_id'] = user.id
        session['user_first_name'] = data['first_name']
        session['user_last_name'] = data['last_name']
        session['user_email'] = data['email']
        return redirect("/recipes")
    else:
        print("Validation Fails")
        return redirect("/")

@app.route('/login', methods=['post'])
def login():
    data = {
        'email': request.form['email']
    }
    users = User.get_user_by_email(data)

    if len(users) != 1:
        flash('Username is incorrect', "error_message_users")
        print(request.form['password'])
        return redirect('/')
    
    user = users[0]

    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')

    session['user_id'] = user['id']
    session['user_first_name'] = user['first_name']
    session['user_last_name'] = user['last_name']
    session['user_email'] = user['email']
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

