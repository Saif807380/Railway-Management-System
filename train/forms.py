from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, ValidationError
from train.models import User

class AddTrain(FlaskForm):
    trainName = StringField('Train Name',
                           validators=[DataRequired()])
    trainID = StringField('Train ID',
                        validators=[DataRequired(),Length(min=6,max=6)])
    starting = StringField('Starting Station',
                           validators=[DataRequired()])
    ending = StringField('Ending Station',
                           validators=[DataRequired()])
    monday = BooleanField('Monday')
    tuesday = BooleanField('Tuesday')
    wednesday = BooleanField('Wednesday')
    thursday = BooleanField('Thursday')
    friday = BooleanField('Friday')
    saturday = BooleanField('Saturday')
    sunday = BooleanField('Sunday')
    coaches = SelectField('Coaches',choices = [('18','18'),('20','20'),('22','22')],validators = [Required()])
    submit = SubmitField('Add Train')


class UpdateTrain(FlaskForm):
    trainName = StringField('Train Name',
                           validators=[DataRequired()])
    trainID = StringField('Train ID',
                        validators=[DataRequired(),Length(min=6,max=6)])
    starting = StringField('Starting Station',
                           validators=[DataRequired()])
    ending = StringField('Ending Station',
                           validators=[DataRequired()])
    monday = BooleanField('Monday')
    tuesday = BooleanField('Tuesday')
    wednesday = BooleanField('Wednesday')
    thursday = BooleanField('Thursday')
    friday = BooleanField('Friday')
    saturday = BooleanField('Saturday')
    sunday = BooleanField('Sunday')
    coaches = SelectField('Coaches',choices = [('18','18'),('20','20'),('22','22')],validators = [Required()])
    submit = SubmitField('Update Train')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=15)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('This username is taken. Try another')

    def validate_email(self,email):
        user = User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('Account already exist for this email')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    employeeid = StringField('Employee Id',validators=[DataRequired(), Length(min=10)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=5 ,max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
