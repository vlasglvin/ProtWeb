from flask import Flask, Blueprint, render_template,  request, redirect, url_for, flash
from db_scripts import PlanesDB
from flask_login import UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from settings import *
from app import login_manager, db

accounts = Blueprint('accounts', __name__,
                        template_folder='admin_templates')

class User(UserMixin):
    def __init__(self, user_data):
        super().__init__()
        self.id = str(user_data['id'])
        self.name = user_data['name']
        self.username = user_data['username']
        self.role = user_data['role']


@login_manager.user_loader
def load_user(user_id):
    user_data = db.get_user(user_id)
    return User(user_data)

@accounts.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if 'remember_me' in request.form:
            remember = True
        else:
            remember = False
        user_db = db.check_login_data(username)
        if user_db and check_password_hash(user_db['password'], password):
            
            user = User(user_db)
            login_user(user, remember=remember)
            if user.role == "admin":
                return redirect(url_for('admin.admin_page'))

            return redirect(url_for('main_page'))
        
        else:
            flash("Incorrect username or password", category="alert-warning")

    return render_template("login.html", title = "Login")


@accounts.route("/admin/logout")
def logout():
    logout_user()
    return redirect(url_for('main_page'))


@accounts.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_page'))
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        
        is_valid =  name.strip() != "" and email.strip() != "" and username.strip() != "" and password.strip() != "" and password_repeat.strip() != ""
        
        if is_valid:    
            if db.is_username_exist(username):
                flash("this username is already taken", category="alert-warning")

            elif db.is_email_exist(email):
                flash("this email is already taken", category="alert-warning")
            elif password!= password_repeat:
                flash("Passwords must match", category="alert-warning")
            elif len(password) < 8:
                flash("Password has to be longer than 8 characters", category="alert-warning")
               
            else:
                password_hash = generate_password_hash(password)
                db.create_user(name,username, email, password_hash)
                flash("User created", category="alert-primary")
                return redirect(url_for('accounts.login'))

        else:
            flash("Please fill in all fields", category="alert-warning")


    return render_template("register.html", title = "Create new account")
