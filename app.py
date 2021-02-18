from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
import xgboost

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	# input shop_id and item_id
	ftr = np.array([int(x) for x in request.form.values()])
	
	# load the file to get all the engineered features
	data = pickle.load(open('files/test.gzip', 'rb'))

	# get all the features 
	data = data[test.shop_id == ftr[0]]
	data = data[test.item_id == ftr[1]]

	# if shop or item is not available
	if data.empty:
		output = 'This Shop and Item combination is not available'

	# load the xgboost model
	model = pickle.load(open('files/xgbmodel.dat', 'rb'))
	output = model.predict(data)

	return render_template('predict.html', pred=output)

if __name__ == '__main__':
	app.run()