from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def addTrain():
	return render_template('add_train.html',title="Add Train")

@app.route('/update_train')
def update():
	return render_template('update_train.html',title="Update Train")


if __name__ == "__main__":
	app.run(debug=True)