from app_folder import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from app_folder import login
from hashlib import md5

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index =True, unique=True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy = 'dynamic')
	about_me = db.Column(db.String(140))
	

	def __repr__(self):
		"""
		Returns the User as an account on the application.
		"""
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		"""
		Generates a hash to track the pasword for 'self' aka the user.
		"""
		self.password_hash = generate_password_hash(password)
	def check_password(self, password):
		"""
		Checks the hash corresponding to the pasword for 'self' aka the user.
		"""
		return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
	"""
	Returns the id of the user.
	"""
	return User.query.get(int(id))

class Post(db.Model):
	id =db.Column(db.Integer, primary_key =True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index =True, default = datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Post{}>'.format(self.body)

class Appointment(db.Model):
	__tablename__='appointment'
	id = db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String, index =True)
	phonenumber=db.Column(db.String,index =True)
	time=db.Column(db.Integer,index =True)
	timelength=db.Column(db.Integer,index =True)

	def __init__(self, name, phonenumber, time, timelength):
		self.name= name
		self.phonenumber=phonenumber
		self.time= time
		self.timelength=timelength

	

