from flask import Flask, Blueprint, render_template,  request, redirect, url_for, flash
from dotenv import load_dotenv
from datetime import timedelta
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from db_scripts import PlanesDB
import os
load_dotenv()

from settings import *


app = Flask(__name__)
db = PlanesDB("planes.db")


app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SESSION_REMEMBER_ME_DURATION'] = timedelta(days=31)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "alert-warning"

from admin import admin
from accounts import accounts
app.register_blueprint(accounts)
app.register_blueprint(admin)

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

