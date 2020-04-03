from covaid import app
from covaid.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return "<h1>About<h1>"


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
<<<<<<< HEAD
    return "<h1>Home<h1>"
=======
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@covaid.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

>>>>>>> 09befd9f24f88bafebbb39e4b4c7332c9cf7c1f4
