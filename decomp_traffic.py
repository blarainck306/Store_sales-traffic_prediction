for_cross_sales_traffic = False
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import STL, seasonal_decompose


hourly_sales = pd.read_csv('data/hourly_sales.csv') # hourly_sales_partial
hourly_sales.hour = pd.to_datetime(hourly_sales.hour)

hourly_traffic = pd.read_csv('data/hourly_traffic.csv') 
hourly_traffic.hour = pd.to_datetime(hourly_traffic.hour)

# --------remove data according to dates:
# for sales traffic comparison
if for_cross_sales_traffic:
	hourly_traffic = hourly_traffic[hourly_traffic.hour<=hourly_sales.hour.iloc[-1]]

#------------using moving avereage based decomposition

res = seasonal_decompose(hourly_traffic.Value, model="additive",period = 24)
trend, seasonal, residual= res.trend, res.seasonal, res.resid
daily_components = seasonal
no_daily = hourly_traffic.Value - daily_components

res = seasonal_decompose(no_daily, model="additive",period = 24*7)
trend, seasonal, residual= res.trend, res.seasonal, res.resid
weekly_components = seasonal
no_weekly = no_daily - weekly_components

res = seasonal_decompose(no_weekly, model="additive",period = 24*365)
trend, seasonal, residual= res.trend, res.seasonal, res.resid
yearly_components = seasonal

# -----------using STL decomposition
# # robust makes fit robust more to outliers  ( uses a data-dependent weighting function)
# # we can modify poly nomial degree (0,1) to make fitting more smoother, smoother-->follows orgi data more closely, so if we want to let outlier more declared, use degree = 0
# res = STL(hourly_traffic.Value,period = 24,seasonal = 7, robust = True).fit()
# trend, seasonal, residual= res.trend, res.seasonal, res.resid
# daily_components = seasonal
# no_daily = hourly_traffic.Value - daily_components

# res = STL(no_daily,period = 24 *7,seasonal = 7, robust = True).fit()
# trend, seasonal, residual= res.trend, res.seasonal, res.resid
# weekly_components = seasonal
# no_weekly = no_daily - weekly_components
# #yearly (using STL with jump parameters (efficiency))
# period = 24*365
# low_pass_jump = seasonal_jump = int(0.15 * (period + 1))
# trend_jump = int(0.15 * 1.5 * (period + 1))
# res = STL(no_weekly, 
# 	        period = period, 
# 	        seasonal = 7,  #len(hourly_traffic.Value),
# 	        robust = True,
# 	        trend_jump = trend_jump,
# 	        seasonal_jump = seasonal_jump, 
# 	        low_pass_jump = low_pass_jump).fit() 
# trend, seasonal, residual= res.trend, res.seasonal, res.resid
# yearly_components = seasonal


#---------------time series plots
fig, axs = plt.subplots(6)
fig.suptitle('Deseasoning')

axs[0].plot(hourly_traffic.hour, hourly_traffic.Value)
axs[0].grid(True)
axs[0].set_ylabel('orig')
axs[0].set_xlim([hourly_traffic.hour.iloc[0],hourly_traffic.hour.iloc[-1]])

axs[1].plot(hourly_traffic.hour, trend)
axs[1].grid(True)
axs[1].set_ylabel('trend')
axs[1].set_xlim([hourly_traffic.hour.iloc[0],hourly_traffic.hour.iloc[-1]])
axs[1].set_ylim([0,12])

axs[2].plot(hourly_traffic.hour, daily_components)
axs[2].grid(True)
axs[2].set_ylabel('seasonal_daily')
axs[2].set_xlim([hourly_traffic.hour.iloc[0],hourly_traffic.hour.iloc[-1]])

axs[3].plot(hourly_traffic.hour, weekly_components)
axs[3].grid(True)
axs[3].set_ylabel('seasonal_weekly')
axs[3].set_xlim([hourly_traffic.hour.iloc[0],hourly_traffic.hour.iloc[-1]])

axs[4].plot(hourly_traffic.hour, yearly_components)
axs[4].grid(True)
axs[4].set_ylabel('seasonal_yearly')
axs[4].set_xlim([hourly_traffic.hour.iloc[0],hourly_traffic.hour.iloc[-1]])

axs[5].plot(hourly_traffic.hour, residual)
axs[5].grid(True)
axs[5].set_ylabel('residual')
axs[5].set_xlim([hourly_traffic.hour.iloc[0],hourly_traffic.hour.iloc[-1]])

fig.set_size_inches(46, 18)
plt.show()


# save results
results = pd.DataFrame({'hour':hourly_traffic.hour,'raw':hourly_traffic.Value,'trend':trend,'seasonal_daily':daily_components,'seasonal_weekly':weekly_components,'seasonal_yearly': yearly_components, 'residual':residual})


# for sales, traffic comparison
if for_cross_sales_traffic:
	results = results[~results.residual.isnull()]

results.to_csv('data/decomp_results_traffic.csv',index = False)



