"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag


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

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

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

    user.first_name = request.form['first_name'] or user.first_name
    user.last_name = request.form['last_name'] or user.last_name
    user.image_url = request.form['image_url'] or user.image_url

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



###################################### PART TWO - Adding Posts ####################################

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def new_post_form(user_id):
    """ Display form to submit new post for specfic user """

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("posts/new.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post(user_id):
    """ Handles form submission for new post for specfic user """

    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']
    # return list of tag ids
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post( title=title, content=content, user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """ Display information for specfic post  """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("/posts/show.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """ Display form to edit existing post """

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("/posts/edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """ Handle form submission for updating existing post """

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title'] or post.title
    post.content = request.form['content'] or post.content

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """ Handle form submission for deleting an existing post """

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")



################################# PART THREE - Add M2M Relationship ################################

@app.route("/tags")
def tags_page():
    """ Display all tags info """

    tags = Tag.query.all()
    
    return render_template("/tags/index.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """ Display information for specfic tag  """

    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tags/show.html", tag=tag)


@app.route("/tags/new")
def new_tag_form():
    """ Display form to submit new tag """

    return render_template("/tags/new.html")


@app.route("/tags/new", methods=["POST"])
def new_tag():
    """ Handles form submission for new tags """

    tag_name = request.form['tag_name']

    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """ Display form to edit existing tag """

    tag = Tag.query.get_or_404(tag_id)
    return render_template("/tags/edit.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def update_tag(tag_id):
    """ Handle form submission for updating existing tag """

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form['tag_name'] or tag.name

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """ Handle form submission for deleting an existing tag """

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")