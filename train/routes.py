from train import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from train.models import Admin, User, Train
from train.forms import AddTrain, UpdateTrain, RegistrationForm, LoginForm, AdminLoginForm
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html')

@app.route('/book_ticket')
@login_required
def bookTicket():
	return render_template('book_ticket.html',title= "Book Ticket")


@app.route('/train_status')
@login_required
def trainStatus():
	return render_template('train_status.html',title= "Train Status")


@app.route('/cancel_booking')
@login_required
def cancelBooking():
	return render_template('cancel_booking.html',title= "Cancel Booking")


@app.route('/account')
@login_required
def account():
	return render_template('account.html', title= "Account")

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
	form = AddTrain()
	print(form.errors)
	if form.validate_on_submit():
		train = Train(train_no = form.trainID.data,train_name = form.trainName.data,num_of_coaches = form.coaches.data,source= form.starting.data,destination = form.ending.data)
		print(form.monday.data,form.tuesday.data)
		db.session.add(train)
		db.session.commit()
		flash('Your train has been added', 'success')
		return redirect(url_for('view'))
	return render_template('add_train.html',title="Add Train",form = form)

@app.route('/update_train',methods=['GET', 'POST'])
def update():
	form = UpdateTrain()
	return render_template('update_train.html',title="Update Train",form = form)

@app.route('/update_train/<loaded>',methods=['GET', 'POST'])
def updateTrain(loaded):
	form = UpdateTrain()
	return render_template('update_train.html',title="Update Train",loaded=loaded, form = form)

@app.route('/view')
def view():
	trains = Train.query.all()
	print(trains)
	return render_template('view_train.html',title= "View Trains",trains= trains)

@app.route('/admin_login',methods=['GET' , 'POST'])
def adminLogin():
	form = AdminLoginForm()
	if  form.validate_on_submit():
		flash(f'Logged in successfully as {form.employeeid.data}!','success')
		return redirect(url_for('addTrain'))
	return render_template('admin_login.html', title= "Admin Login", form=form)
