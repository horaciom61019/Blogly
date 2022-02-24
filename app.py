"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret" 
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route("/")
def base():
    """ Homepage redirects to list of users """

    return redirect("/users")


@app.route("/users")
def users_page():
    """ Display all users info """

    # Get users from database
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("/users/index.html", users=users)


@app.route("/users/new", methods=["GET"])
def new_user_form():
    """ Display form to submit new user """

    return render_template("/users/new.html")


@app.route("/users/new", methods=["POST"])
def new_user():
    """ Handles form submission for new users """

    first_name=request.form['first_name']
    last_name=request.form['last_name']
    image_url=request.form['image_url'] or None

    new_user = User( first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """ Display user's information """

    user = User.query.get_or_404(user_id)
    return render_template("/users/show.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """ Display form to edit existing user """

    user = User.query.get_or_404(user_id)
    return render_template("/users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """ Handle form submission for updating existing user """

    user = User.query.get_or_404(user_id)

    user.first_name=request.form['first_name'] or user.first_name
    user.last_name=request.form['last_name'] or user.last_name
    user.image_url=request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Handle form submission for deleting an existing user """

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")