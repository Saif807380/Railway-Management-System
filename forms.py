from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required


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