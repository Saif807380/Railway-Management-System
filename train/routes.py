from train import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from train.models import Admin, User, Train
from train.forms import AddTrain, UpdateTrain, RegistrationForm, LoginForm, AdminLoginForm
from flask_login import login_user, current_user, logout_user, login_required
adminLog = 0    #To check if admin is logged in or not

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html',admin = adminLog)

@app.route('/book_ticket')
@login_required
def bookTicket():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	return render_template('book_ticket.html',title= "Book Ticket",admin = adminLog)


@app.route('/train_status')
@login_required
def trainStatus():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	return render_template('train_status.html',title= "Train Status",admin = adminLog)


@app.route('/cancel_booking')
@login_required
def cancelBooking():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	return render_template('cancel_booking.html',title= "Cancel Booking",admin = adminLog)


@app.route('/account')
@login_required
def account():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	return render_template('account.html', title= "Account",admin = adminLog)

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form =RegistrationForm()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', title= "Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form =LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful! Please check email & Password', 'danger')
	return render_template('login.html', title= "Login", form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('home'))




@app.route('/add_train',methods=['GET', 'POST'])
def addTrain():
	if adminLog == 1:
		form = AddTrain()
		if form.validate_on_submit():
			days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
			running_days = list()
			for day in days:
				if form[day].data:
					form[day].data = 1
				else:
					form[day].data = 0
			train = Train(train_no = form.trainID.data,train_name = form.trainName.data,
						num_of_coaches = form.coaches.data,source= form.starting.data,destination = form.ending.data,
						monday=form.monday.data,tuesday=form.tuesday.data,wednesday=form.wednesday.data,thursday=form.thursday.data,
						friday=form.friday.data,saturday=form.saturday.data,sunday=form.sunday.data)
			print(form.monday.data,form.tuesday.data)
			db.session.add(train)
			db.session.commit()
			flash('Your train has been added', 'success')
			return redirect(url_for('view'))
		return render_template('add_train.html',title="Add Train",form = form,admin = adminLog)
	else:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		else:
			flash('Please log in to access this page.', 'info')
			return redirect(url_for('adminLogin'))
		

@app.route('/update_train',methods=['GET', 'POST'])
def update():
	if adminLog == 1:
		form = UpdateTrain()
		train = ""
		return render_template('update_train.html',title="Update Train",form = form,train=train,admin = adminLog)
	else:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		else:
			flash('Please log in to access this page.', 'info')
			return redirect(url_for('adminLogin'))
	

train = ""

@app.route('/update_train/<loaded>',methods=['GET', 'POST'])
def updateTrain(loaded):
	if adminLog ==1:
		global train
		form = UpdateTrain()
		try:
			global train
			train_no = request.form["train_no"]
			train = Train.query.filter_by(train_no=train_no).first()
			print(train_no)
		except:
			if form.validate_on_submit():
				db.session.delete(train)
				db.session.commit()
				train = Train(train_no = form.trainID.data,train_name = form.trainName.data,
							num_of_coaches = form.coaches.data,source= form.starting.data,destination = form.ending.data,
							monday=form.monday.data,tuesday=form.tuesday.data,wednesday=form.wednesday.data,thursday=form.thursday.data,
							friday=form.friday.data,saturday=form.saturday.data,sunday=form.sunday.data)
				db.session.add(train)
				db.session.commit()
				flash('Your train has been updated', 'success')
				return redirect(url_for('view'))
		return render_template('update_train.html',title="Update Train",loaded=loaded, form = form, train=train,admin = adminLog)
	else:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		else:
			flash('Please log in to access this page.', 'info')
			return redirect(url_for('adminLogin'))


@app.route('/view')
def view():
	if adminLog == 1:
		trains = Train.query.all()
		if len(trains) > 0:
			return render_template('view_train.html',title= "View Trains",trains= trains,admin = adminLog)
		else:
			return "no trains found"
	else:
		if current_user.is_authenticated:
			return redirect(url_for('home'))
		else:
			flash('Please log in to access this page.', 'info')
			return redirect(url_for('adminLogin'))
	

@app.route('/admin_login', methods=['GET', 'POST'])
def adminLogin():
	if current_user.is_authenticated:
		flash('Please log out from the user first', 'info')
		return redirect(url_for('adminLogin'))
	form =LoginForm()
	if form.validate_on_submit():
		admin = Admin.query.filter_by(email=form.email.data).first()
		if admin and bcrypt.check_password_hash(admin.password, form.password.data):
			next_page = request.args.get('next')
			global adminLog
			adminLog = 1				#admin is logged in
			if next_page:
				return redirect(next_page)
			else:
				return redirect(url_for('home'))
		else:
			flash('Login Unsuccessful! Please check email & Password', 'danger')
	return render_template('admin_login.html', title= "Admin Login", form=form)

@app.route('/admin_logout')
def adminLogout():
	global adminLog
	adminLog = 0
	return redirect(url_for('home'))
