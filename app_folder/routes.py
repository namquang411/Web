from app_folder import app
from app_folder import db
from flask import render_template, redirect, flash, url_for, request, Flask
from app_folder.forms import LoginForm, ChangePasswordForm
from app_folder.forms import RegistrationForm, AppointmentForm, DeleteForm
from app_folder.models import User , Appointment
from flask_login import current_user, login_user, login_required
from flask_login import logout_user
from datetime import datetime
from werkzeug.urls import url_parse


@app.before_request
def befor_request():
	"""
	Stores the last login of the account user on the app if their account is authenticated.
	"""
	if current_user.is_authenticated:
		current_user.last_seen= datetime.utcnow()
		db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
	"""
	Welcomes the user to the application.
	"""
	return render_template("calendar_events.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	"""
	Allows the user to login to the application if they have a valid username and password that has been stored
	in the application's data. If the information given by the user is invalid, they are prompted to re enter
	a valid username and password.
	"""
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page= request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html',title = 'Sign In', form=form)

@app.route('/logout')
def logout():
	"""
	Allows the user to logout of the application.
	"""
	logout_user()
	return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
	"""
		Allows the user to register and create an account using a username, email, and a created password through forms.
	"""

	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form= RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html',title ='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts=[
		{'author': user, 'body': 'Test #1'}
	      ]
	return render_template('user.html', user=user, posts=posts)
@app.route('/edit_profile', methods=['Get','POST'])
@login_required
def change_password():
	form= ChangePasswordForm()
	if form.validate_on_submit():
		user = current_user
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Your changes have been saved.')
		return redirect(url_for('login'))
	return render_template('change_password.html',title='Change Password', form=form)

@app.route('/inventory/<style>')
def inventory(style):
    try:
        appointment = Appointment.query.filter_by(style=style).order_by(Appointment.name).all()
        return render_template('list.html', appointment=appointment, style=style)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/appointment', methods=['Get','POST'])
@login_required
def appointment():
	form1=AppointmentForm()
	if form1.validate_on_submit():
		name = request.form['name']
		phonenumber = request.form['phonenumber']
		time= request.form['time']
		timelength= request.form['timelength']
		record = Appointment(name, phonenumber, time, timelength)
		db.session.add(record)
		db.session.commit()
		flash('Added New Appointment')
		return redirect(url_for('login'))
	return render_template('appointment.html', form=form1)

@app.route('/select_record/<letters>')
def select_record(letters):
    return render_template('select_record.html')

# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete', methods=['POST'])
def edit_or_delete():
    id = request.form['id']
    choice = request.form['choice']
    apt = Appointment.query.filter(Appointment.id == id).first()
    # two forms in this template
    form1 = appointment()
    form2 = DeleteForm()
    return render_template('edit_or_delete.html', apt=apt, form1=form1, form2=form2, choice=choice)

# result of delete - this function deletes the record
@app.route('/delete_result', methods=['POST'])
def delete_result():
    id = request.form['id_field']
    purpose = request.form['purpose']
    apt = Appointment.query.filter(Appointment.id == id).first()
    if purpose == 'delete':
        db.session.delete(apt)
        db.session.commit()
        message = f"The appointment has been deleted from the database."
        return render_template('result.html', message=message)
@app.route('/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')
    # You'd normally use the variables above to limit the data returned
    # you don't want to return ALL events like in this code
    # but since no db or any real storage is implemented I'm just
    # returning data from a text file that contains json elements

    with open("flaskcalendar/events.json", "r") as input_data:
        # you should use something else here than just plaintext
        # check out jsonfiy method or the built in json module
        # http://flask.pocoo.org/docs/0.10/api/#module-flask.json
        return input_data.read()