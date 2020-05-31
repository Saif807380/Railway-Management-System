from train import db
from train.models import Admin, User, Passenger, Ticket, Train , Station, SeatStatus
from train import bcrypt
import os

db.create_all()
hashed_pw = bcrypt.generate_password_hash(os.environ.get("ADMIN_PASSWORD")).decode('utf-8')
admin = Admin(username='admin', email="admin@train.com", password=hashed_pw)
db.session.add(admin)
db.session.commit()