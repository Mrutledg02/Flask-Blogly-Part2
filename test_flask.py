import os
import unittest
from datetime import datetime
from flask import Flask
from models import db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/test_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True

db.init_app(app)


class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        # Create a new user
        new_user = User(first_name='John', last_name='Doe', image_url='john.jpg')
        db.session.add(new_user)
        db.session.commit()

        # Retrieve the user from the database
        user = User.query.filter_by(first_name='John').first()

        # Check if the user is not None
        self.assertIsNotNone(user)

    def test_post_creation(self):
        # Create a new user
        new_user = User(first_name='John', last_name='Doe', image_url='john.jpg')
        db.session.add(new_user)
        db.session.commit()

        # Create a new post
        new_post = Post(title='Test Post', content='This is a test post.', created_at=datetime.utcnow(), user=new_user)
        db.session.add(new_post)
        db.session.commit()

        # Retrieve the post from the database
        post = Post.query.filter_by(title='Test Post').first()

        # Check if the post is not None
        self.assertIsNotNone(post)
        # Check if the post belongs to the correct user
        self.assertEqual(post.user, new_user)


if __name__ == '__main__':
    unittest.main()
