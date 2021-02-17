from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict')
def predict(input):
	#
	return render_template('predict.html', pred)

if __name__ == '__main__':
	app.run()