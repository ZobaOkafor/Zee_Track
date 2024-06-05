from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from models.user import User
from models import Task, Project, Notification
from forms import RegistrationForm, LoginForm, TaskForm, ProjectForm
# from app import app, db
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


@main.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    tasks = user.tasks.order_by(Task.due_date).all()
    projects = user.projects.order_by(Project.start_date).all()
    notifications = user.notifications.order_by(
            Notification.created_at.desc()).all()
    return render_template('dashboard.html', tasks=tasks, projects=projects,
                           notifications=notifications, title='Dashboard')


@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    tasks = current_user.tasks.all()
    # Create an instance of the form
    form = TaskForm()
    return render_template('tasks.html', tasks=tasks, form=form, title='Tasks')


@main.route('/tasks/add', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('main.tasks'))
    return render_template('tasks.html', form=form, title='Add Task')


@main.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    task = Task.query.get_or_404(id)
    if task.author != current_user:
        abort(403)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.status = form.status.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('main.tasks'))
    return render_template('tasks.html', form=form, title='Edit Task')


@main.route('/tasks/<int:id>/delete', methods=['POST'])
@login_required
def delete_task(id):
    task = Task.query.get_or_404(id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('main.tasks'))


@main.route('/projects', methods=['GET', 'POST'])
@login_required
def projects():
    projects = current_user.projects.all()
    form = ProjectForm()
    return render_template('projects.html', projects=projects,
                           form=form, title='Projects')


@main.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
            user_id=current_user.id
        )
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('main.projects'))
    return render_template('projects.html', form=form, title='Add Project')


@main.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    if project.author != current_user:
        abort(403)
    form = ProjectForm(obj=project)
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.status = form.status.data
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('main.projects'))
    return render_template('projects.html', form=form,
                           title='Edit Project')


@main.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    if project.author != current_user:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('main.projects'))


@main.route('/notifications')
@login_required
def notifications():
    notifications = current_user.notifications.order_by(
            Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=notifications,
                           title='Notifications')


@main.route('/notifications/<int:id>/delete', methods=['POST'])
@login_required
def delete_notification(id):
    notification = Notification.query.get_or_404(id)
    if notification.user_id != current_user.id:
        abort(403)
    db.session.delete(notification)
    db.session.commit()
    flash('Notification deleted successfully!', 'success')
    return redirect(url_for('main.notifications'))


@main.route('/calendar')
@login_required
def calendar():
    tasks = current_user.tasks.all()
    projects = current_user.projects.all()
    events = []

    for task in tasks:
        events.append({
            'title': task.title,
            'start': task.due_date.strftime("%Y-%m-%d"),
            'color': 'red' if task.priority == 'High' else 'orange'
                     if task.priority == 'Medium' else 'green'
        })

    for project in projects:
        events.append({
            'title': project.title,
            'start': project.start_date.strftime("%Y-%m-%d"),
            'end': project.end_date.strftime("%Y-%m-%d"),
            'color': 'blue'
        })

    return render_template('calendar.html', events=events, title='Calendar')


@main.route('/')
def landing_page():
    return render_template('landing_page.html')

# Other routes for tasks and projects will follow the same structure
