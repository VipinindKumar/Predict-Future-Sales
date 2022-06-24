from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
import xgboost

import mysql.connector
import json

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

	data = data.drop(columns=dropcols)

	# load the xgboost model
	model = xgboost.Booster()  # init model
	model.load_model('files/xgbmodel.json')

	# make the prediction on the shop and item
	output = model.predict(xgboost.DMatrix(data))
	output = output[0]

	return render_template('predict.html', pred=output)

@app.route('/checkdb')
def get_widgets():
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="12345",
    database="inventory"
  )
  cursor = mydb.cursor()

  cursor.execute("SELECT * FROM widgets")

  row_headers=[x[0] for x in cursor.description] #this will extract row headers

  results = cursor.fetchall()

  json_data=[]
  for result in results:
    json_data.append(dict(zip(row_headers,result)))

  cursor.close()

  return json.dumps(json_data)

@app.route('/initdb')
def db_init():
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="12345"
  )
  cursor = mydb.cursor()

  # cursor.execute("DROP DATABASE IF EXISTS inventory")
  cursor.execute("CREATE DATABASE IF NOT EXISTS inventory")

  cursor.close()

  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="12345",
    database="inventory"
  )
  cursor = mydb.cursor()

  # cursor.execute("DROP TABLE IF EXISTS widgets")
  cursor.execute("CREATE TABLE IF NOT EXISTS widgets (name VARCHAR(255), description VARCHAR(255))")

  cursor.close()

  return 'init database'

@app.route('/adddb')
def db_add():
  # Initializes the database
  db_init()

  # connect to the database
  mydb = mysql.connector.connect(
    host="mysqldb",
    user="root",
    password="12345",
    database="inventory"
  )
  cursor = mydb.cursor()

  # add some values to the table
  # cursor.execute("USE inventory")
  # cursor.execute("INSERT INTO widgets (name, description) VALUES (\"Vipin\", \"hoho decription\")")

  # insert many
  sql = "INSERT INTO widgets (name, description) VALUES (%s, %s)"
  val = [
    ('Peter', 'Lowstreet 4'),
    ('Amy', 'Apple st 652'),
    ('Hannah', 'Mountain 21'),
    ('Michael', 'Valley 345'),
    ('Sandy', 'Ocean blvd 2'),
    ('Betty', 'Green Grass 1'),
    ('Richard', 'Sky st 331'),
    ('Susan', 'One way 98'),
    ('Vicky', 'Yellow Garden 2'),
    ('Ben', 'Park Lane 38'),
    ('William', 'Central st 954'),
    ('Chuck', 'Main Road 989'),
    ('Viola', 'Sideway 1633')
  ]

  cursor.executemany(sql, val)

  mydb.commit()

  cursor.close()

  return "Succesfully Created and Added values to the database"



if __name__ == '__main__':
	app.run(host="172.20.0.100")