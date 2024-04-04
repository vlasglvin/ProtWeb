from flask import Flask, render_template,  request, redirect, url_for, flash
from dotenv import load_dotenv

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

from db_scripts import PlanesDB
import os
load_dotenv()

app = Flask(__name__)
db = PlanesDB("planes.db")

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

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


@app.route("/")
def main_page():
    title = "PlanePedia - your source about planes"
    plane_types = db.get_all_categories()
    planes = db.get_all_planes_by_categories()

    return render_template("index.html",
                            title = title,
                            planes = planes,
                            plane_types=plane_types)


@app.route("/plane/<name>")
def plane_page(name):
    title = "Plane " + name
    plane = db.get_plane(name)
    plane_types = db.get_all_categories()

    return render_template("plane.html", 
                           title = title,
                           plane = plane,
                           plane_types=plane_types)

@app.route("/type/<int:category_id>")
def planes_by_type(category_id):
    plane_types = db.get_all_categories()
    planes = db.get_planes_by_category(category_id)
    title = db.get_category(category_id)

    return render_template("category_planes.html",
                            title = title,
                            planes = planes,
                            plane_types=plane_types)

@app.route("/search")
def search():
    plane_types = db.get_all_categories()
    planes = []
    title = "Search"
    
    if request.method == 'GET':
        query = request.args.get("query")
        planes = db.search_planes(query)


    return render_template("category_planes.html",
                            title = title,
                            planes = planes,
                            plane_types=plane_types)

@app.route("/articles")
def articles():
    title = "History of planes"
    plane_types = db.get_all_categories()
    articles = db.get_all_articles()

    return render_template("plane_history.html",
                            title = title,
                            articles = articles,
                            plane_types=plane_types)


@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_db = db.check_login_data(username, password)
        if user_db:
            user = User(user_db)
            login_user(user)
            return redirect(url_for('admin_page'))
        
        else:
            flash("Incorrect username or password")

    return render_template("login.html", title = "Login")

@login_required
@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    return render_template("admin_page.html", title = "Administartor")


@app.route("/admin/logout")
def logout():
    logout_user()
    return redirect(url_for('main_page'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        password_repeat = request.form['password_repeat']
        
        is_valid =  name.strip() != "" and email.strip() != "" and username.strip() != "" and password.strip() != "" and password_repeat.strip() != ""
        
        if is_valid:    
            if db.is_username_exist(username):
                flash("this username is already taken")

            elif db.is_email_exist(email):
                flash("this email is already taken")
            elif password!= password_repeat:
                flash("Passwords must match")
            else:
                db.create_user(name,username, email, password)
                flash("User created")
        else:
            flash("Please fill in all fields")


    return render_template("register.html", title = "Create new account")