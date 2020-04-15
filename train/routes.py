from train import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, session
from train.models import Admin, User, Train, Passenger, SeatStatus, Ticket
from train.forms import AddTrain, UpdateTrain, RegistrationForm, LoginForm, AdminLoginForm ,CancelBookingForm ,BookTicket , UpdateAccountForm
from flask_login import login_user, current_user, logout_user, login_required
adminLog = 0    #To check if admin is logged in or not

@app.route('/')
@app.route('/home')
def home():
	return render_template('index.html',admin = adminLog)

@app.route('/book_ticket',methods=['GET','POST'])
@login_required
def bookTicket():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	form =BookTicket()
	if request.method=='POST':
		session["source"] = (form.source.data).source
		session["destination"]=(form.destination.data).destination
		session["date"]=form.date.data
		session["tier"]=form.tier.data
		print(session["source"],type(session["date"]))
		return redirect(url_for('availableTrain'))
	else:
		return render_template('book_ticket.html', title= "Book Ticket", form=form,admin = adminLog)


@app.route('/book_ticket/available_train',methods=['GET','POST'])
@login_required
def availableTrain():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	print(session["source"],session["destination"])
	selected_trains = [train for train in Train.query.filter_by(source = session["source"], destination=session["destination"])]
	if request.method=='POST':
		session["train_no"] = request.form['select_train']
		return redirect(url_for('addPassenger'))		
	return render_template('available_trains.html', selected_trains=selected_trains,source = session['source'],destination=session['destination'])


@app.route('/book_ticket/add_passengers', methods=['GET','POST'])
@login_required
def addPassenger():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	if request.method == "POST":
		if 'passengers' in request.form:
			session["passengers"] = int(request.form["passengers"])
			return render_template('add_passengers.html',title="Add Passengers",passengers=session["passengers"],admin = adminLog,loaded=True)
		elif 'addp' in request.form:		
			form = request.form	
			print(session['source'],session['destination'])
			for i in range(session['passengers']):
				passenger = Passenger(name =form[f"name{i+1}"], age= form[f"age{i+1}"], user_id=current_user.id,source=session['source'],destination=session['destination'],tier=session['tier'],train_no=session['train_no'],date=session['date'])
				seat = SeatStatus.query.filter_by(train_no = session['train_no'],  pass_id=0, seat_type=session['tier']).first()
				seat_no = seat.seat_no
				print(seat_no)
				pnr_no = int(session['train_no'])*10000 + int(seat_no)			
				db.session.add(passenger)
				db.session.commit()
				seat.pass_id= passenger.pass_id	
				ticket = Ticket(pnr_number = pnr_no,user_id=current_user.id, source=session['source'], destination=session['destination'], journey_date=session['date'], seat_no=seat_no, pass_id=passenger.pass_id, train_no=session['train_no'], tier=session['tier'])
				db.session.add(ticket)
			db.session.commit()
			flash('Ticket has been booked successfully', 'info')
			return redirect(url_for('myBookings'))
	return render_template('add_passengers.html',title="Add Passengers",passengers=0,admin = adminLog,loaded=False)


@app.route('/train_status')
@login_required
def trainStatus():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	return render_template('train_status.html',title= "Train Status",admin = adminLog)

@app.route('/my_bookings', methods=['GET', 'POST'])
@login_required
def myBookings():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	my_bookings = [ticket for ticket in Ticket.query.filter_by(user_id = current_user.id)]
	return render_template('my_bookings.html',title= "My Bookings",my_bookings=my_bookings)

@app.route("/ticket/<string:pnr>")
def ticket(pnr):
	ticket = Ticket.query.get(pnr)
	passenger = ticket.passenger
	return render_template('ticket.html',ticket=ticket,passenger=passenger)

@app.route("/ticket/<string:pnr>/cancel", methods=['POST'])
@login_required
def cancelTicket(pnr):
	ticket = Ticket.query.get(pnr)
	passenger = ticket.passenger
	seat = SeatStatus.query.filter_by(pass_id=passenger.pass_id).first()
	seat.pass_id=0
	db.session.delete(ticket)
	db.session.delete(passenger)
	db.session.commit()
	flash('Ticket has been canceled', 'info')
	return redirect(url_for('myBookings'))

@app.route('/fare', methods=['GET', 'POST'])
@login_required
def fare():
	return render_template('fare.html',title= "Fare Chart")

@app.route('/account' , methods=['GET', 'POST'])
@login_required
def account():
	global adminLog
	if adminLog == 1:
		adminLog = 0
	form = UpdateAccountForm()
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated!', 'success')
		return redirect(url_for('account'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	return render_template('account.html' , title = "Account" , admin = adminLog , form = form)

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
			print("Yes")
			days=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
			for day in days:
				if form[day].data:
					form[day].data = 1
				else:
					form[day].data = 0
			train = Train(train_no = form.trainID.data,train_name = form.trainName.data,
						source= form.starting.data,destination = form.ending.data,
						monday=form.monday.data,tuesday=form.tuesday.data,wednesday=form.wednesday.data,thursday=form.thursday.data,
						friday=form.friday.data,saturday=form.saturday.data,sunday=form.sunday.data,ac_first_class_coaches=form.acFirstClassCoaches.data,
						ac_two_tier_coaches=form.acTwoTierCoaches.data,ac_three_tier_coaches=form.acThreeTierCoaches.data,sleeper_class_coaches=form.sleeperClassCoaches.data,
						ac_first_class_available_seats=24*int(form.acFirstClassCoaches.data),
						ac_two_tier_available_seats=54*int(form.acTwoTierCoaches.data), ac_three_tier_available_seats=64*int(form.acThreeTierCoaches.data),
						sleeper_class_available_seats=72*int(form.sleeperClassCoaches.data),
						ac_first_class_fare=form.acFirstClassFare.data,ac_two_tier_fare=form.acTwoTierFare.data,ac_three_tier_fare=form.acThreeTierFare.data,
						sleeper_class_fare=form.sleeperClassFare.data)
			db.session.add(train)
			print("Train read Success")
			ac1_seats = 24*int(form.acFirstClassCoaches.data)
			for i in range(ac1_seats):
				print("Inside Loop")
				seat = SeatStatus(train_no = form.trainID.data, seat_no = 1000+i+1, seat_type="1A")
				db.session.add(seat)

			ac2_seats = 54*int(form.acTwoTierCoaches.data)
			for i in range(ac2_seats):
				seat = SeatStatus(train_no = form.trainID.data, seat_no = 2000+i+1, seat_type="2A")
				db.session.add(seat)
			
			ac3_seats = 64*int(form.acThreeTierCoaches.data)
			for i in range(ac3_seats):
				seat = SeatStatus(train_no = form.trainID.data, seat_no = 3000+i+1, seat_type="3A")
				db.session.add(seat)
			
			sleep_seats = 72*int(form.sleeperClassCoaches.data)
			for i in range(sleep_seats):
				seat = SeatStatus(train_no = form.trainID.data, seat_no = 4000+i+1, seat_type="Sl")
				db.session.add(seat)

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
						friday=form.friday.data,saturday=form.saturday.data,sunday=form.sunday.data,ac_first_class_seats=form.acFirstClassSeats.data,
						ac_two_tier_seats=form.acTwoTierSeats.data,ac_three_tier_seats=form.acThreeTierSeats.data,sleeper_class_seats=form.sleeperClassSeats.data,
						ac_first_class_fare=form.acFirstClassFare.data,ac_two_tier_fare=form.acTwoTierFare.data,ac_three_tier_fare=form.acThreeTierFare.data,
						sleeper_class_fare=form.sleeperClassFare.data)
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
