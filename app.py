from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	ftr = np.array([int(x) for x in request.form.values()])

	pred = ftr
	return render_template('predict.html', pred)

if __name__ == '__main__':
	app.run()