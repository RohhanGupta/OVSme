from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from . import db
from .models import voter
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)

@auth.route("/registration", methods=["POST", "GET"])
def registration():
    if request.method=="POST":
        name = request.form.get("name")
        email = request.form.get("email")
        rollnumber = request.form.get("rollnumber")
        phonenumber = request.form.get("phonenumber")
        password = request.form.get("password")
        confirmpassword = request.form.get("confirmpassword")

        email_exists = voter.query.filter_by(email=email).first()
        rollnumber_exists = voter.query.filter_by(roll_number=rollnumber).first()
        if email_exists:
            flash('Email already in use!', category='error')
        elif "@thapar.edu" not in email:
            flash('Invalid email!', category='error')
        elif rollnumber_exists:
            flash('Roll number already in use!', category='error')
        elif password != confirmpassword:
            flash('Passwords don\'t match', category='error')
        elif len(password)<6:
            flash('Password too short!', category='error')
        else:
            new_voter = voter(name=name, email=email, roll_number=rollnumber, phone_number=phonenumber, password_1=generate_password_hash(password, method='sha256'))
            db.session.add(new_voter)
            db.session.commit()
            login_user(new_voter, remember=True)
            flash('User Created!')
            return redirect(url_for('auth.login'))
    
    return render_template("registration.html")

@auth.route("/login", methods=['POST','GET'])
def login():
    if request.method=="POST":
        login_email = request.form.get("login_email")
        login_password = request.form.get("login_password")
        user = voter.query.filter_by(email = login_email).first()
        if user:
            if check_password_hash(user.password_1, login_password):
                login_user(user, remember=True)
                return redirect(url_for('auth.home'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.landing'))

@auth.route("/home")
@login_required
def home():
    admin = current_user.admin
    status = current_user.status
    return render_template("home.html", admin=admin,status=status)