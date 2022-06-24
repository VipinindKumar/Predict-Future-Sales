# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir("../input"))

# Any results you write to the current directory are saved as output.


import gc
from tqdm import tqdm_notebook
from math import ceil
import pickle

from sklearn.ensemble import ExtraTreesRegressor
import xgboost as xgb

from sklearn.metrics import mean_squared_error as mse
import matplotlib.pyplot as plt


# Loading in data
X_train = pd.read_pickle('../input/sales1-grid-itmcat-target-meanenc-lag/X_train.gzip')
X_val = pd.read_pickle('../input/sales1-grid-itmcat-target-meanenc-lag/X_val.gzip')
y_train = np.load('../input/sales1-grid-itmcat-target-meanenc-lag/y_train.gzip', allow_pickle=True)
y_val = np.load('../input/sales1-grid-itmcat-target-meanenc-lag/y_val.gzip', allow_pickle=True)

test = pd.read_pickle('../input/sales1-grid-itmcat-target-meanenc-lag/test.gzip')


# training the model

batch_size = int(len(X_train) / 2)
iterations = 30
model = pickle.load(open("../input/sales2-exttr-xgb/xgbmodel.dat", "rb"))
rmse_train_list = list()
rmse_val_list = list()

for i in tqdm_notebook(range(iterations)):
    for start in tqdm_notebook(range(0, len(X_train), batch_size)):
        model = xgb.train({
            'max_depth' : 5,
            'learning_rate': 0.1,
            'lambda': 300,  # L2,
            'seed' : 4,
            'eval_metric' : 'rmse',
            'min_child_weight' : 300,
            'alpha' : 300,
            'sub_sample' : 0.8
            #'verbosity' : 3
            #'predictor' : 'gpu_predictor'
        }, dtrain=xgb.DMatrix(X_train[start:start+batch_size], y_train[start:start+batch_size]), xgb_model=model)
        
    y_train_pr = model.predict(xgb.DMatrix(X_train))
    y_val_pr = model.predict(xgb.DMatrix(X_val))
    
    rmse_train_list.append(mse(y_train, y_train_pr) ** (1/2))
    rmse_val_list.append(mse(y_val, y_val_pr) ** (1/2))
    
    print('Train RMSE itr@{}: {}'.format(i, rmse_train_list[i]))
    print('Val RMSE itr@{}: {}'.format(i, rmse_val_list[i]))

    # plot the rmse
    plt.plot(rmse_train_list, label='train')
    plt.plot(rmse_val_list, label='val')
        
        
    #print('RMSE itr@{}: {}'.format(i, mse(y_val, y_pr) ** (1/2)))

y_pred = model.predict(xgb.DMatrix(X_val))
print('RMSE at the end: {}'.format(mse(y_val, y_pred) ** (1/2)))


# plot the feature importance
xgb.plot_importance(model)


# pickle model
pickle.dump(model, open("xgbmodel.dat", "wb"))


# predictions for test file
sub = model.predict(xgb.DMatrix(test))
sub = sub.clip(0, 20)
sub[:5]

sub = pd.DataFrame(sub, columns=['item_cnt_month'])

sub.to_csv('sub.csv', index_label='ID')



