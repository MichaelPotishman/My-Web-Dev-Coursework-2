from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager



app = Flask(__name__)
app.config.from_object('config')

Bootstrap(app)
csrf = CSRFProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/'


from app.models import User  # Import User model explicitly

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Use query.get() to fetch the user


from app import views, models
