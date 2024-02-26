"""Blogly application."""
from flask import Flask, render_template, request, redirect, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Secret key for DebugToolbar
app.config['SECRET_KEY'] = "oh_so_secret"

# Initialize DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

# Redirect to list of users
@app.route('/')
def show_recent_posts():
    """Show the 5 most recent posts on the homepage."""
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('homepage.html', recent_posts=recent_posts)

# Show all users
@app.route('/users')
def show_all_users():
    """Show all users."""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('user_listing.html', users=users)

# Show an add form for users
@app.route('/users/new', methods=['GET'])
def show_add_user_form():
    return render_template('new_user_form.html')

# Process the add form, adding a new user and going back to /users
@app.route('/users/new', methods=['POST'])
def add_new_user():
    """Add new user and redirect to list of users."""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    
    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/users')

# Show information about the given user
@app.route('/users/<int:user_id>')
def show_user_detail(user_id):
    """Show information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)

# Show the edit page for a user
@app.route('/users/<int:user_id>/edit', methods=['GET'])
def show_edit_user_form(user_id):
    """Show the edit page for a user."""
    user = User.query.get_or_404(user_id)
    return render_template('user_edit.html', user=user)

# Process the edit form, returning the user to the /users page
@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.commit()
    return redirect('/users')

# Delete the user
@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# Show form to add a new post
@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def show_add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('new_post_form.html', user=user)

# Handle form submission to add a new post
@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, user=user)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('show_user_detail', user_id=user_id))

# Show details of a specific post
@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

# Show form to edit a post
@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post_form.html', post=post)

# Handle form submission to edit a post
@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.commit()
    return redirect(url_for('show_post_detail', post_id=post_id))

# Delete a post
@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id  # Store user_id before deleting post
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('show_user_detail', user_id=user_id))

# Error handler for 404 error
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    if app.config['ENV'] == 'development':
        app.run(debug=True)
    else:
        app.run()