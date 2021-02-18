from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	ftr = np.array([int(x) for x in request.form.values()])

	
	return render_template('predict.html', pred=ftr)

if __name__ == '__main__':
	app.run()