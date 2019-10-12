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

- sales1(oct_as_pred) notebook
    - using last month data (October) as predictions for next month data (November)
    - Score, root mean squared error (RMSE) => 1.16777
    

- sales modified data csv notebook
    - Create a grid of shop_ids and item_ids for different date_block_num with corresponding item_cnt_month
    

- sales modified data csv(mean enc) notebook
    - Add target mean encoding feature to the data
