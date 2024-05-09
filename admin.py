from flask import Flask, Blueprint, render_template,  request, redirect, url_for, flash
from db_scripts import PlanesDB
from flask_login import UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from settings import *
from app import login_manager, db

admin = Blueprint('admin', __name__,
                        template_folder='admin_templates')


@admin.route("/admin", methods=["GET", "POST"])
@login_required
def admin_page():
    if current_user.role != "admin":
                return redirect(url_for('main_page'))
    
    title = "PlanePedia - Administrator"
    plane_types = db.get_all_categories()
    planes = db.get_all_planes_by_categories()
    suggested_planes = db.get_suggested_planes()
    print(suggested_planes)

    return render_template("admin_page.html",
                            title = title,
                            planes = planes,
                            plane_types=plane_types,
                            suggested_planes = suggested_planes)


@admin.route("/admin/plane/<int:plane_id>/delete", methods=["GET", "POST"])
@login_required
def plane_delete_page(plane_id):
    if current_user.role != "admin":
                return redirect(url_for('main_page'))
    
    title = "PlanePedia - Administrator"
    plane_types = db.get_all_categories()
    if request.method == "POST":
          db.delete_plane(plane_id)
          return redirect(url_for("admin.admin_page"))
    

    return render_template("delete_confirmation.html",
                            title = title,
                            plane_types=plane_types)


@admin.route("/admin/new_plane", methods=["GET", "POST"])
@login_required
def add_plane_page():
    if current_user.role != "admin":
                return redirect(url_for('main_page'))
    
    plane_types = db.get_all_categories()
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category']
        image = request.files['image'] 
        country = request.form['country']
        quantity = request.form['quantity']
        prodused_start = request.form['prodused_start']
        prodused_end = request.form['prodused_end']
        cost = request.form['cost']
        wing_shape = request.form['wing_shape']
        specifications = request.form['specifications']
        description = request.form['description']
        history = request.form['history']

        is_valid = True
        for field in [name, category_id, country, quantity, prodused_start, cost, wing_shape, description, history]:
            if field.strip() == "":
                is_valid = False
                break
        
        #try:
        if is_valid:
            if request.form.get('present_days') == 'present_days':
                prodused_end = "present-day"
            if image:
                image.save(IMG_PATH + image.filename )
            db.create_plane(name, int(category_id), image.filename, country, quantity,
                            prodused_start, prodused_end, cost, wing_shape, specifications, description, history)

            flash("Plane added succesfully.", category="alert-primary")
        else:
            flash("Please fill in all fields", category="alert-danger")
        #except:
            #flash("Error. Try again!", category="alert-danger")

        
    
    return render_template("add_plane.html", title = "Add new plane", plane_types = plane_types)




@admin.route("/admin/plane/<int:plane_id>/update", methods=["GET", "POST"])
@login_required
def update_plane_page(plane_id):
    if current_user.role != "admin":
                return redirect(url_for('main_page'))
    
    plane_types = db.get_all_categories()
    plane = db.get_plane_by_id(plane_id)
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category']
        image = request.files['image'] 
        country = request.form['country']
        quantity = request.form['quantity']
        prodused_start = request.form['prodused_start']
        prodused_end = request.form['prodused_end']
        cost = request.form['cost']
        wing_shape = request.form['wing_shape']
        specifications = request.form['specifications']
        description = request.form['description']
        history = request.form['history']
        visibility = request.form["visibility"]

        image_name = plane['image']

        is_valid = True
        for field in [name, category_id, country, quantity, prodused_start, cost, wing_shape, description, history]:
            if field.strip() == "":
                is_valid = False
                break
        
        try:
            if is_valid:
                if request.form.get('present_days') == 'present_days':
                    prodused_end = "present-day"
                if image:
                    image.save(IMG_PATH + image.filename )
                    image_name = image.filename
                db.update_plane(plane['id'], name, int(category_id), image_name, country, quantity,
                                prodused_start, prodused_end, cost, wing_shape, specifications, description, history, visibility)

                flash("Plane saved succesfully.", category="alert-primary")
            else:
                flash("Please fill in all fields", category="alert-danger")
        except:
            flash("Error. Try again!", category="alert-danger")

        
    
    return render_template("update_plane.html", title = "Edit plane", plane=plane, plane_types = plane_types)



@admin.route("/admin/articles", methods=["GET", "POST"])
@login_required
def admin_articles_page():
    if current_user.role != "admin":
                return redirect(url_for('main_page'))
    
    title = "Plane History - Administrator"
    plane_types = db.get_all_categories()
    articles = db.get_all_articles()

    return render_template("admin_plane_history.html",
                            title = title,
                            articles = articles,
                            plane_types=plane_types)


@admin.route("/admin/new_article", methods=["GET", "POST"])
@login_required
def add_article_page():
    if current_user.role != "admin":
                return redirect(url_for('main_page'))
    
    plane_types = db.get_all_categories()
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        image = request.files['image'] 
        author = request.form['author']

        is_valid = True
        for field in [title, text, author]:
            if field.strip() == "":
                is_valid = False
                break
        
        try:
            if is_valid:
                if image:
                     image.save(IMG_PATH + image.filename )
                db.create_article(title, text, image.filename, author)

                flash("Article added succesfully.", category="alert-primary")
            else:
                flash("Please fill in all fields", category="alert-danger")
        except:
            flash("Error. Try again!", category="alert-danger")

        
    
    return render_template("add_article.html", title = "Add new article", plane_types = plane_types)


@admin.route("/admin/article/<int:article_id>/delete", methods=["GET", "POST"])
@login_required
def article_delete_page(article_id):
    if current_user.role != "admin":
                return redirect(url_for('main_page'))
    
    title = "Delete article"
    plane_types = db.get_all_categories()
    if request.method == "POST":
          db.delete_article(article_id)
          return redirect(url_for("admin.admin_articles_page"))
    

    return render_template("delete_confirmation.html",
                            title = title,
                            plane_types=plane_types)


@admin.route("/admin/article/<int:article_id>/update", methods=["GET", "POST"])
@login_required
def update_article_page(article_id):
    if current_user.role != "admin":
                return redirect(url_for('main_page'))
    
    plane_types = db.get_all_categories()
    article = db.get_article_by_id(article_id)

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        image = request.files['image'] 
        author = request.form['author']
        image_name = article['image']

        is_valid = True
        for field in [title, text, author]:
            if field.strip() == "":
                is_valid = False
                break
        
        try:
            if is_valid:
                if image:
                     image.save(IMG_PATH + image.filename )
                     image_name = image.filename

                db.update_article(article_id, title, text, image_name, author)

                flash("Article updated succesfully.", category="alert-primary")
            else:
                flash("Please fill in all fields", category="alert-danger")
        except:
            flash("Error. Try again!", category="alert-danger")

        
    
    return render_template("update_article.html", title = "Update article", article=article, plane_types = plane_types)


