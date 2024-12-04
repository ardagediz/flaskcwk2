import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config.from_pyfile(os.path.join(base_dir, '../config.py'))

db = SQLAlchemy(app)
csrf = CSRFProtect(app)  # Initialize CSRF protection

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

migrate = Migrate(app, db)


def setup_database():
    with app.app_context():
        from .models import Product  # Import here to avoid circular import
        db.create_all()
        if not Product.query.first():
            products = [
                Product(name="Generic Product 1", price=70.00, stock_level=10),
                Product(name="Generic Product 2", price=50.00, stock_level=20),
                Product(name="Generic Product 3", price=40.00, stock_level=30)
            ]
            db.session.bulk_save_objects(products)
            db.session.commit()


setup_database()


def register_views():
    from . import views  # Import here to avoid circular import


register_views()
