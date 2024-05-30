import unittest
from run import app
from extensions import db
from models.user import User

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = false # Disable CSRF for testing
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
			# Create a test user
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpassword')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
        	db.drop_all()

    # def test_password_hashing(self):
       # u = User(username='testuser')
       # u.set_password('testpassword')
       # self.assertFalse(u.check_password('wrongpassword'))
       # self.assertTrue(u.check_password('testpassword'))

    def test_register_user(self):
        response = self.app.post('/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'confirm_password': 'newpassword'
        }, follow_redirects=True)

		# Debugging output
		if response.status_code != 302:
            print("Register form errors:", response.data.decode())
		 # Expect redirect after successful registration
        self.assertEqual(response.status_code, 302)

    def test_login_user(self):
        # Now, log in with the new user
        response = self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)

		# Debugging output
        if response.status_code != 200:
            print("Login form errors:", response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Zee Track', response.data)

	def test_login_user_invalid_credentials(self):
        response = self.app.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)

        self.assertIn(b'Invalid email or password', response.data)


if __name__ == '__main__':
    unittest.main()
