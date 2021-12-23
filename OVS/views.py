from flask import Blueprint,Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import candidate
from . import db
import matplotlib.pyplot as plt
import os

views = Blueprint("views", __name__)

@views.route("/")
def landing():
    return render_template("landing.html")

@views.route("/uploadface")
@login_required
def uploadface():
    status = current_user.status
    admin = current_user.admin
    return render_template("uploadFace.html", status=status, admin=admin)

@views.route("/profile")
@login_required
def profile():
    info = current_user
    status = current_user.status
    admin = current_user.admin
    return render_template("profile.html", status=status, admin=admin, info=info)

@views.route("/voting")
@login_required
def voting():
    status = current_user.status
    admin = current_user.admin
    candidates = candidate.query.filter_by().all()
    if current_user.voted == 1:
        flash("You have already voted!")
        return redirect(url_for("auth.home"))
    if status == "Not Verified":
         flash("User not Verified")
         return redirect(url_for("auth.home"))
    return render_template("voting.html", candidates=candidates, status=status, admin=admin)

@views.route("/vote/<int:id>/")
def vote(id):
    my_candidate = candidate.query.get_or_404(id)
    my_candidate.vote_count = my_candidate.vote_count + 1
    current_user.voted = 1
    db.session.commit()
    return redirect(url_for("auth.home"))

@views.route("/result")
@login_required
def result():
    status = current_user.status
    admin = current_user.admin
    candidates = candidate.query.filter_by().all()
    votes = []
    person = []
    for candid in candidates:
        votes.append(candid.vote_count)
        person.append(candid.candidate_name)
    max_vote = max(votes)
    details = candidate.query.filter_by(vote_count=max_vote).first()
    winner = details.candidate_name
    fig = plt.figure()
    plt.bar(person, votes, color ='maroon',width = 0.4)
    my_path = os.path.abspath(os.getcwd())
    fig.savefig(my_path + '\\OVS\\static\\result\\resultbar.png')

    plt.pie(votes, labels = person, autopct='%1.0f%%', )
    my_path = os.path.abspath(os.getcwd())
    fig.savefig(my_path + '\\OVS\\static\\result\\resultpie.png')

    return render_template("result.html", status=status, admin=admin, max_vote=max_vote, winner=winner)