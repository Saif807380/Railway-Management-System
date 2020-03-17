from train import db, user_login_manager
from flask_login import UserMixin

@user_login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return f"Admin('{self.username}', '{self.email}')"

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	passengers = db.relationship('Passenger', backref='booker', lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

class Passenger(db.Model):
	pass_id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(20),nullable=False)
	age = db.Column(db.Integer,nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
	ticket = db.relationship('Ticket',backref='passenger',lazy=True,uselist=False)  #uselist=False implies one-to-one relationship
	def __repr__(self):
		return f"Passenger('{self.pass_id}','{self.name}','{self.age}','{self.user_id}')"

class Ticket(db.Model):
	pnr_number = db.Column(db.String(10),primary_key=True)
	destination = db.Column(db.String(20),nullable=False)
	source = db.Column(db.String(20),nullable=False)
	journey_date = db.Column(db.DateTime,nullable=False)
	seat_no = db.Column(db.Integer,unique=True,nullable=False)
	pass_id = db.Column(db.Integer,db.ForeignKey('passenger.pass_id'),nullable=False)
	train_no = db.Column(db.Integer,db.ForeignKey('train.train_no'),nullable=False)

	def __repr__(self):
		return f"Ticket('{self.pnr_number}', '{self.source}', '{self.destination}', '{self.journey_date}', '{self.train_no}', '{self.seat_no}', '{self.pass_id}')"

class Train(db.Model):
	train_no = db.Column(db.Integer,primary_key=True)
	train_name = db.Column(db.String(30),unique=True,nullable=False)
	num_of_coaches = db.Column(db.Integer,nullable=False)
	source = db.Column(db.String(20),nullable=False)
	destination = db.Column(db.String(20),nullable=False)

	def __repr__(self):
		return f"Train('{self.train_no}', '{self.train_name}')"

class Station(db.Model):
	station_id = db.Column(db.Integer,primary_key=True)
	station_name = db.Column(db.String(20),nullable=False,unique=True)
	# train_source = db.relationship('Train',backref='starting_trains',lazy=True)
	# train_destination = db.relationship('Train',backref='ending_trains',lazy=True)

	def __repr__(self):
		return f"Station('{self.station_id}', '{self.station_name}')"

# class Days(db.Model):
# 	train_id = db.Column(db.Integer,db.ForeignKey('Train'),primary_key=True)
# 	monday = db.Column(db.Integer,nullable=False,default=0)
# 	tuesday = db.Column(db.Integer,nullable=False,default=0)
# 	wednesday = db.Column(db.Integer,nullable=False,default=0)
# 	thursday = db.Column(db.Integer,nullable=False,default=0)
# 	friday = db.Column(db.Integer,nullable=False,default=0)
# 	saturday = db.Column(db.Integer,nullable=False,default=0)
# 	sunday = db.Column(db.Integer,nullable=False,default=0)

# 	def __repr__(self):
# 		return f"Days"


