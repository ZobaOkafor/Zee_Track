from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from models.user import User
from forms import RegistrationForm, LoginForm, TaskForm, ProjectForm
from extensions import db 

# Define a Blueprint
main = Blueprint('main', __name__)


@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if request.method == 'POST':
        print(f"Form data: {request.form}")
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid email or password', 'error')
                return redirect(url_for('main.login'))
        
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        else:
            print("Form errors:", form.errors)
    
    return render_template('login.html', title='Sign In', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if request.method == 'POST':
        print(f"Form data: {request.form}")
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('main.login'))
        else:
            print("Form errors:", form.errors)

    return render_template('register.html', title='Register', form=form)

# Other routes for tasks and projects will follow the same structure
