from run import app
from extensions import db
from models.user import User

def create_test_user():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if the user already exists
        user = User.query.filter_by(email='test@example.com').first()
        if not user:
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()
            print("Test user created")
        else:
            print("Test user already exists")

if __name__ == "__main__":
    create_test_user()
