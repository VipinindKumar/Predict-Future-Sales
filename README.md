# Predict-Future-Sales

### Predict total sales for every item and shop for the next month, from a time-series dataset consisting of daily sales data

#### Columns:
* items columns            :  ('item_name', 'item_id', 'item_category_id')
* sales columns            :  ('date', 'date_block_num', 'shop_id', 'item_id', 'item_price', 'item_cnt_day')
* item_categories columns  :  ('item_category_name', 'item_category_id')
* shops columns            :  ('shop_name', 'shop_id')
* test columns             :  ('ID', 'shop_id', 'item_id')

#### item_cnt_month:
`sales.groupby(['date_block_num', 'shop_id', 'item_id']).item_cnt_day.sum()`
turns daily sales data into monthly data for every shop/item pair

<hr/>

#### sales1(oct_as_pred)/ sales0.1 notebook:
    - using last month data (October) as predictions for next month data (November)
    - Score, root mean squared error (RMSE) => 1.16777
    

#### 'sales modified data csv'/ first half of sales0.15 notebook:
    - Create a grid of shop_ids and item_ids for different date_block_num with corresponding item_cnt_month
    

#### 'sales modified data csv(mean enc)'/ second half of sales0.15 notebook:
    - Add target mean encoding feature to the data


#### sales0.2-meanenc:
    - Create target mean encoding feature with CV loop regularization using KFold
    - item_id_target_mean = all_data.iloc[rest].groupby('item_id').target.mean()
    - all_data.loc[all_data.index[curr],'item_target_enc'] = all_data['item_id'].map(item_id_target_mean)


#### sales1-grid-itmcat-target-meanenc-lag:
    - Remove Outliers
    - Duplicate shops
    - City name from shop names
    - Types and Subtypes from categories of items
    - Revenue -> 
        - sales['revenue'] = sales['item_price'] * sales['item_cnt_day']
    - Target variables -> 
        - Add sum of sales in a month for shops (target_shop)
        - s = sales.groupby(['date_block_num', 'shop_id'], as_index=False).item_cnt_day.sum()
        - s = s.rename(columns={'item_cnt_day' : 'target_shop'})
    - Delta features ->
        - Chnage in particular value over a period (month)
        - Average item price 
        - Shop revenue trend
    - Mean/Target Encoding of all id variables
    - Lag Features, previous values over different periods (1, 2, 3, 6, ... months before)
    - division between train, val/dev sets
    - and all the new features in the test set too.


#### sales2-exttr-xgb:
    - First used XGBoost.XGBRegressor (ran out of memory)
    - Switched to ExtraTreesRegressor, with Mean Squared Error as metric
    - Next used Iterative Increment training or Batch training with XGBoost with rmse (to get around limited memory problem)
    - Sticked to 2 batches, to keep training/convergence faster and under memory limits
    - shop_id is highly important when using XGBoost, but not very important when using ExtraTreesRegressor


#### sales3-model_cnt:
    - Script used to bypass limited memory and time
    - by training, saving and re-training the models
    - lead to overfitting could not increase the complexity of the models 
    - and could not add the features dropped earlier because limited processing memory, while preparing the data

<hr/>

#### Feature importance for XGBoost:
<img src="https://github.com/VipinindKumar/Predict-Future-Sales/raw/master/feature_importance/xgboost.png" width="700">

#### Feature importance for ExtraTreesRegressor:
<img src="https://github.com/VipinindKumar/Predict-Future-Sales/raw/master/feature_importance/exttr.png" width="700">
