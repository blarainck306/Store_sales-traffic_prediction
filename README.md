# Store_sales-traffic_prediction

Currently, I used two separate models for prediction of sales and traffic uses . So the codes are almost identical except that predicted sales was used as one of the features when predicting traffic. Later, we may use a single neural network for multi-task learning prediction.
To review the codes, please start with the sales directory.

ipython notebooks in each directory have uses suggested by their names:
- data exploration
- feature engineering
- model training

Ohter python scripts:
- decomp_sales: use STL or moving average for data detrending and Deseasonalization (sales data)
- decomp_traffic: use STL or moving average for data detrending and Deseasonalization (traffic data)
- utility.py:  contains some utility function used by ipython notebook
- visulization.py: for data visualization
