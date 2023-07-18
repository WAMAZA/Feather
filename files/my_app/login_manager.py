from flask_login import LoginManager
from . import app
from .models import User


login_manager = LoginManager(app)
login_manager.login_view = 'connexion'
login_manager.login_message_category = 'info'
login_manager.login_message = 'You cannot access this page. Please log in to access this page.'
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))