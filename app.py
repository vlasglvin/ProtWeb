from flask import Flask, render_template

from db_scripts import PlanesDB

app = Flask(__name__)
db = PlanesDB("planes.db")

@app.route("/")
def main_page():
    title = "PlanePedia - your source about planes"
    planes = db.get_all_planes()

    return render_template("index.html", title = title, planes = planes)

@app.route("/plane/<name>")
def plane_page(name):
    title = "Plane " + name
    plane = db.get_plane(name)
    
    return render_template("plane.html", title = title, plane = plane)
