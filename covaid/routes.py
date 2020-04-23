from covaid import app, db, bcrypt, model, mail
from covaid.forms import RegistrationForm, LoginForm, RequestForm, RequestResetForm, ResetPasswordForm
from flask import render_template, url_for, flash, redirect, request
from covaid.models import User, Request
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
from covaid.config import API_KEY
import numpy as np
import requests as r


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/requests", methods=['GET', 'POST'])
@login_required
def requests():
    user = current_user
    form = RequestForm()
    user_requests = User.query.filter_by(email=user.email).first().requests
    users = User.query.all()
    all_users_requests = []

    for u in users:
        if u.id != user.id:
            miles, time = distance(user.city, user.street, u.city, u.street)
            # all_users_requests += u.requests
            list_of_requests_user = []
            for req in u.requests:
                if req.status == "Posted":
                    parameters = np.array(
                        [float(miles[:-3]), has_requested(req.item_name), num_requested(req.item_name)])
                    parameters = np.reshape(parameters, (1, 3))
                    relevance = model.predict(parameters)
                    relevance = np.argmax(relevance)
                    temp = (req, miles, time, relevance)
                    list_of_requests_user.append(temp)
            all_users_requests += list_of_requests_user

    if form.validate_on_submit():
        db_request = Request(item_name=form.item.data.title(), quantity=form.quantity.data, instruct=form.instruct.data)
        user.requests.append(db_request)
        db.session.commit()
        return redirect(url_for('requests'))

    if request.method == 'POST' and request.form.get('accept'):
        user_id = request.form.get('accept')
        specific_request = Request.query.filter_by(id=user_id).first()
        specific_request.status = 'In Progress'
        db.session.commit()
        return redirect(url_for('requests'))

    if request.method == 'POST' and request.form.get('delivered'):
        user_id = request.form.get('delivered')
        specific_request = Request.query.filter_by(id=user_id).first()
        specific_request.status = 'Delivered'
        db.session.commit()
        return redirect(url_for('requests'))

    return render_template('requests.html', form=form, user_requests=user_requests,
                           all_users_requests=all_users_requests)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data.title(), email=form.email.data, password=hashed_pw,
                    street=form.street.data.title(), city=form.city.data.title())
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


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('requests'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to ' + form.email.data + ' to reset password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('requests'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Your account password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


def distance(origin_city, origin_street, destination_city, destination_street):
    origin_street = origin_street.replace(' ', ',')
    destination_street = destination_street.replace(' ', ',')
    origin_city = origin_city.replace(' ', ',')
    destination_city = destination_city.replace(' ', ',')
    origin = origin_city + ',' + origin_street
    destination = destination_city + ',' + destination_street
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={}&destinations={}&key='.format(
        origin, destination) + API_KEY
    response = r.get(url)
    data = response.json()
    miles = data['rows'][0]['elements'][0]['distance']['text']
    time = data['rows'][0]['elements'][0]['duration']['text']
    if "," in miles:
        miles = miles.replace(',', "")
    return miles, time


def has_requested(item):
    item_exists = Request.query.filter_by(item_name=item).first()
    if item_exists:
        return 1
    else:
        return 0


def num_requested(item):
    return int(Request.query.filter_by(item_name=item).count())


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@covaid.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then you can ignore this email and your account will not be affected.
'''
    mail.send(msg)
