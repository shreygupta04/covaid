from covaid import app
from flask import render_template, url_for, flash, redirect


@app.route("/")
@app.route("/home")
def home():
    return render_template('layout.html')


@app.route("/about")
def about():
    return "<h1>About<h1>"


@app.route("/contact")
def contact():
    return "<h1>Home<h1>"


@app.route("/register")
def register():
    return "<h1>Home<h1>"


@app.route("/login")
def login():
    return "<h1>Home<h1>"

