from flask import Flask, render_template, url_for
from forms import AddTrain, UpdateTrain

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

if __name__ == "__main__":
	app.run(debug=True)