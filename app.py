from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
import xgboost
import sys

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
	data = data[data.shop_id == ftr[0]]
	data = data[data.item_id == ftr[1]]

	# if shop or item is not available
	if data.empty:
		output = 'This Shop and Item combination is not available'

		return render_template('predict.html', pred=output)

	# drop columns not used for training
	dropcols = ['type_id', 'target_item_cat_lag_5', 'city_id', 'target_item_cat_lag_3', 'target_city_lag_5', 'target_item_type_lag_6', 
            'delta_avg_shop_revenue_lag_6', 'delta_avg_shop_revenue_lag_3', 'delta_avg_item_price_lag_2', 'item_category_id',
            'delta_avg_item_price_lag_4', 'target_city_lag_4', 'target_item_cat_lag_4', 'subtype_id', 'target_city_lag_3', 
            'target_item_lag_3', 'target_item_subtype_lag_4', 'target_item_lag_5', 'target_item_cat_lag_6', 'target_item_subtype_lag_6']

	print('before drop')
	sys.stdout.flush()
	data = data.drop(columns=dropcols)
	print('afetr drop')
	sys.stdout.flush()

	# load the xgboost model
	model = pickle.load(open('files/xgbmodel.dat', 'rb'))
	print('model loaded')
	sys.stdout.flush()
	# make the prediction on the shop and item
	output = model.predict(data)
	print('prediction made')
	sys.stdout.flush()
	output = output[0]
	print('int selected')
	sys.stdout.flush()

	return render_template('predict.html', pred=output)

if __name__ == '__main__':
	app.run(debug=True)