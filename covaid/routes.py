from covaid import app, db, bcrypt
from covaid.forms import RegistrationForm, LoginForm, ContactForm, RequestForm
from flask import render_template, url_for, flash, redirect, request
from covaid.models import User, Request
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    form = ContactForm()
    return render_template('contact.html', title='Contact Us', form=form)

@app.route("/requests", methods=['GET', 'POST'])
@login_required
def requests():
    user = current_user
    form = RequestForm()
    user_requests = User.query.filter_by(email=user.email).first().requests
    if form.validate_on_submit():
        request = Request(item_name=form.item.data.title(), quantity=form.quantity.data, instruct=form.instruct.data)
        user.requests.append(request)
        db.session.commit()
        return redirect(url_for('requests'))
    return render_template('requests.html', form=form, user_requests=user_requests)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, email=form.email.data, password=hashed_pw, street=form.street.data, city=form.city.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('requests'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(url_for(next_page))
            else:
                return redirect(url_for('requests'))
            return redirect(url_for('requests'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
