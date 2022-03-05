
from wtforms import Form, StringField, validators, PasswordField, BooleanField, SubmitField, DecimalField, SelectField, IntegerField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    submit = SubmitField('Register')

class RequestTutor(Form):
    grade = SelectField('Grade', choices=[('K', 'K'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    subject = SelectField('Subject', choices=[('Math', 'Math'), ('Science', 'Science'), ('English', 'English'), ('History', 'History'), ('Spanish', 'Spanish'), ('French', 'French'), ('German', 'German'), ('Latin', 'Latin'), ('Other', 'Other')])
    description = TextAreaField('Description', [validators.Length(min=10, max=1000)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    submit = SubmitField('Submit')

class BecomeTutor(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    subject = SelectField('Subject', choices=[('Math', 'Math'), ('Science', 'Science'), ('English', 'English'), ('History', 'History'), ('Spanish', 'Spanish'), ('French', 'French'), ('German', 'German'), ('Latin', 'Latin'), ('Other', 'Other')])
    grade = SelectField('Grade', choices=[('K', 'K'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    submit = SubmitField('Submit')
