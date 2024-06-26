from flask_wtf import FlaskForm
from wtforms import (
        StringField, PasswordField, SubmitField, BooleanField,
        TextAreaField, DateField)
from wtforms.validators import (
        DataRequired, Length, Email, EqualTo, ValidationError)
from models.user import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                           Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=128)])
    password2 = PasswordField(
            'Confirm Password', validators=[DataRequired(),
                                            EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                    'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due Date', format='%Y-%m-%d')
    priority = StringField('Priority')
    status = StringField('Status')
    submit = SubmitField('Create Task')


class EditTaskForm(FlaskForm):
    name = StringField('Task Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_date = DateField('Due Date', format='%Y-%m-%d')
    submit = SubmitField('Update Task')


class ProjectForm(FlaskForm):
    project_name = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    status = StringField('Status')
    submit = SubmitField('Create Project')
