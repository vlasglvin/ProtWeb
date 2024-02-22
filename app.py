from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main_page():
    title = "PlanePedia - your source about planes"
    return render_template("index.html", title = title)

