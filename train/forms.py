from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,DateField,IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Required, ValidationError
from train.models import User,Train
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from train import db

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


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AdminLoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=5 ,max=15)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CancelBookingForm(FlaskForm):
    pnrNo = StringField('PNR No',validators=[DataRequired(),Length(min=10,max=10)])
    submit = SubmitField('Next')

def source_station_choices():      
    return db.session.query(Train).group_by(Train.source).all()

def destination_station_choices():      
    return db.session.query(Train).group_by(Train.destination).all()

class BookTicket(FlaskForm):
    source = QuerySelectField('Select source station',query_factory=source_station_choices, get_label='source')  
    destination = QuerySelectField('Select destination',query_factory=destination_station_choices, get_label='destination')
    date = DateField('Date',format='%d/%m/%Y', validators=[DataRequired()])
    tier = SelectField('Tier',choices = [('1A','AC First Class'),('2A','AC 2 Tier'),('3A','AC 3 Tier'),('Sl','Sleeper')],validators = [Required()])
    submit = SubmitField('Find All Trains')

class AddPassengers(FlaskForm):
    name = StringField('Passenger Name',validators=[DataRequired()])
    age = IntegerField('Age', validators=[NumberRange(min=1, max=2), Required()] )
