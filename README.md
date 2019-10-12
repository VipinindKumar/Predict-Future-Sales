# PredictFutureSales

### Predict total sales for every product and store in the next month from a  time-series dataset consisting of daily sales data

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
