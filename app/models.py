from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db, login_manager

# Define the user_loader callback to reload the user object from the user ID stored in the session


from flask_login import UserMixin


def get_db():
    from app import db
    return db


def get_login_manager():
    from app import login_manager
    return login_manager


db = get_db()
login_manager = get_login_manager()

# Define the user_loader callback to reload the user object from the user ID stored in the session


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    favourites = db.relationship('Product', secondary='user_favourites', backref=db.backref(
        'favourited_by', lazy='dynamic'))
    basket_items = db.relationship(
        'Product', secondary='user_basket', backref=db.backref('in_baskets_of', lazy='dynamic'))

# Product model


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_level = db.Column(db.Integer, default=2)
    likes = db.Column(db.Integer, default=0)


# Association table for User and Product - Favourites
user_favourites = db.Table('user_favourites',
                           db.Column('user_id', db.Integer, db.ForeignKey(
                               'user.id'), primary_key=True),
                           db.Column('product_id', db.Integer, db.ForeignKey(
                               'product.id'), primary_key=True))

# Association table for User and Product - Basket
user_basket = db.Table('user_basket',
                       db.Column('user_id', db.Integer, db.ForeignKey(
                           'user.id'), primary_key=True),
                       db.Column('product_id', db.Integer, db.ForeignKey(
                           'product.id'), primary_key=True))
