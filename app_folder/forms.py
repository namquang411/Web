from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, HiddenField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app_folder.models import User
from app_folder.models import Appointment

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()])
	email = StringField('Email', validators =[DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	password2 = PasswordField('Repeat Password', validators =[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		"""
		This function checks to see if the username matches a username that is stored in the app's system
		and requests a different username to be entered if there is no match.
		"""
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Plaese use a different username.')

	def validate_email(self, email):
		"""
		This function checks to see if the email associated with the account on the app is valid and
		is stored in the app's email database. If it is not a valid email, the user is prompted to
		enter a different email address.
		"""
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Plaese use a different email address.')
class ChangePasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	submit= SubmitField('Submit')

class AppointmentForm(FlaskForm):
	id_field = HiddenField()
	name= StringField('Username')
	phonenumber = StringField('Phone')
	time = SelectField('Choose your time', choices=[('',''),('9am to 10pm', '9am to 10pm')])
	timelength= SelectField('Choose your length',choices=[('',''),('15','15' ),('30','30' ),('60','60' )])
	submit= SubmitField('Add')

class DeleteForm(FlaskForm):
	id_field=HiddenField()
	purpose=HiddenField()
	submit=SubmitField('Delete')