from flask_login import LoginManager
from models.user import User  # Import your User model here

login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # 'auth' is the blueprint name, 'login' is the endpoint name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
