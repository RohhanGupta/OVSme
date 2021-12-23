from flask import Blueprint,Flask, render_template, request, redirect, url_for,flash
from . import db
from flask_login import login_required, current_user
from .models import candidate, voter

admin = Blueprint("admin", __name__)

@admin.route("/")
def admin_landing():
    if current_user.admin == "Admin":
        status = current_user.status
        admin = current_user.admin
        return render_template("admin.html", status=status, admin=admin)
    return render_template("error.html")
    
@admin.route("/dashboard")
@login_required
def dashboard():
    status = current_user.status
    admin = current_user.admin
    all_data = voter.query.all()
    return render_template("dashboard.html", status=status, voters = all_data, admin=admin)

@admin.route('/delete/<int:id>/', methods = ['GET', 'POST'])
def delete(id):
    if current_user.admin == "Admin":
        my_data = voter.query.get_or_404(id)
        db.session.delete(my_data)
        db.session.commit() 
        return redirect(url_for("admin.dashboard"))
    return render_template("error.html")

@admin.route("/addcandidate", methods=["POST", "GET"])
@login_required
def addcandidate():
    if current_user.admin == "Admin":
        status = current_user.status
        admin = current_user.admin
        if request.method == "POST":
            candidate_name = request.form.get("name")
            description = request.form.get("description")
            new_candidate = candidate(candidate_name=candidate_name, description=description)
            db.session.add(new_candidate)
            db.session.commit()
        return render_template("admin_candidate_register.html", status=status, admin=admin)
    return render_template("error.html")
    
@admin.route('/updatedetails/<int:id>/', methods = ['GET', 'POST'])
def updatedetails(id):
    if current_user.admin == "Admin":
        admin = current_user.admin
        status = current_user.status
        data = voter.query.get_or_404(id)
        if request.method == 'POST':
            my_data = voter.query.get_or_404(id)
            my_data.name = request.form.get('name')
            my_data.email = request.form.get('email')
            my_data.phone = request.form.get('phone_number')
            my_data.roll = request.form.get('roll_number')
            my_data.password = request.form.get('password')
            my_data.admin = request.form.get('admin')
            my_data.status = request.form.get('status')
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
        return render_template("updatedetails.html", voter=data, status=status, admin=admin)
    return render_template("error.html")

