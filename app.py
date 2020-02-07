from flask import Flask, render_template, url_for, flash, redirect
from forms import AddTrain, UpdateTrain, RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

@app.route('/',methods=['GET', 'POST'])
def addTrain():
	form = AddTrain()
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
	return render_template('view_train.html',title= "View Trains")

@app.route('/register', methods=['GET', 'POST'])
def register():
	form =RegistrationForm()
	if form.validate_on_submit():
		flash(f'Account created for  {form.username.data}!', 'success')
		return redirect(url_for('addTrain'))
	return render_template('register.html', title= "Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form =LoginForm()
	if form.validate_on_submit():
		if form.email.data == 'abc@abc.com' and form.password.data == 'password':
			flash('You have been logged in!', 'success')
			return redirect (url_for('addTrain'))
		else:
			flash('Invalid Credentials', 'danger')
	return render_template('login.html', title= "Login", form=form)

if __name__ == "__main__":
	app.run(debug=True)