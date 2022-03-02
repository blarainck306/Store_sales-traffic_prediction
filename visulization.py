import sys
print("Python version")
print (sys.version)

import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

hourly_sales = pd.read_csv('data/hourly_sales.csv') 
hourly_sales_partial = pd.read_csv('data/hourly_sales_partial.csv') 
hourly_traffic = pd.read_csv('data/hourly_traffic.csv') 

daily_sales = pd.read_csv('data/daily_sales.csv') 
daily_traffic = pd.read_csv('data/daily_traffic.csv') 

weekly_sales = pd.read_csv('data/weekly_sales.csv') 
weekly_traffic = pd.read_csv('data/weekly_traffic.csv') 

monthly_sales = pd.read_csv('data/monthly_sales.csv') 
monthly_traffic = pd.read_csv('data/monthly_traffic.csv') 

yearly_sales = pd.read_csv('data/yearly_sales.csv') 
yearly_traffic = pd.read_csv('data/yearly_traffic.csv') 


# ---to datetime
hourly_sales.hour = pd.to_datetime(hourly_sales.hour)
hourly_traffic.hour = pd.to_datetime(hourly_traffic.hour)

daily_sales.day = pd.to_datetime(daily_sales.day)
daily_traffic.day = pd.to_datetime(daily_traffic.day)

monthly_sales.month =  pd.to_datetime(monthly_sales.month)
monthly_traffic.month =  pd.to_datetime(monthly_traffic.month )

yearly_sales.year =  pd.to_datetime(yearly_sales.year)
yearly_traffic.year =  pd.to_datetime(yearly_traffic.year )


# time series plots
fig, axs = plt.subplots(4)
fig.suptitle('sales time series plots')


markerline1, stemlines1, baseline = axs[0].stem(hourly_sales.hour, hourly_sales.Value, use_line_collection = True)
plt.setp(stemlines1, 'linewidth', 0.5)
axs[0].set_xlim(pd.to_datetime('2014-05-06'), pd.to_datetime('2014-06-06'))
axs[0].grid(True)
axs[0].set_title('hourly sales')


markerline1, stemlines1, baseline = axs[1].stem(daily_sales.day, daily_sales.Value, use_line_collection = True)
plt.setp(stemlines1, 'linewidth', 0.5)
axs[1].set_xlim(pd.to_datetime('2014-05-06'), pd.to_datetime('2014-06-06'))
axs[1].grid(True)
axs[1].set_title('daily sales')


markerline1, stemlines1, baseline = axs[2].stem(weekly_sales.num_of_weeks, weekly_sales.Value, use_line_collection = True)
plt.setp(stemlines1, 'linewidth', 0.5)
axs[2].grid(True)
axs[2].set_title('weekly sales')

markerline1, stemlines1, baseline = axs[3].stem(monthly_sales.month, monthly_sales.Value, use_line_collection = True)
plt.setp(stemlines1, 'linewidth', 0.5)
axs[3].grid(True)
axs[3].set_title('monthly sales')

fig.set_size_inches(46, 18)
plt.show()


# auto correlation reference: https://stackoverflow.com/questions/14297012/estimate-autocorrelation-using-python
import numpy
def acf(series):
    n = len(series)
    data = numpy.asarray(series)
    mean = numpy.mean(data)
    c0 = numpy.sum((data - mean) ** 2) / float(n)

    def r(h):
        acf_lag = ((data[:n - h] - mean) * (data[h:] - mean)).sum() / float(n) / c0
        return round(acf_lag, 3)
    x = numpy.arange(n) # Avoiding lag 0 calculation
    acf_coeffs = map(r, x)
    return acf_coeffs


fig, axs = plt.subplots(4)
fig.suptitle('sales time series plots')

# hourly 
temp_acf = list(acf(hourly_sales.Value))[:400]
markerline1, stemlines1, baseline = axs[0].stem(range(len(temp_acf)), temp_acf, use_line_collection = True)
plt.setp(stemlines1, 'linewidth', 0.5)
axs[0].set_xlim(0,400)
axs[0].grid(True)
axs[0].set_title('ACF hourly sales')

# hourly 
temp_acf = list(acf(daily_sales.Value))[:400]
markerline1, stemlines1, baseline = axs[1].stem(range(len(temp_acf)), temp_acf, use_line_collection = True)
plt.setp(stemlines1, 'linewidth', 0.5)
axs[1].set_xlim(0,400)
axs[1].grid(True)
axs[1].set_title('ACF daily sales')

# weekly 
temp_acf = list(acf(weekly_sales.Value))[:70]
markerline1, stemlines1, baseline = axs[2].stem(range(len(temp_acf)), temp_acf, use_line_collection = True)
plt.setp(stemlines1, 'linewidth', 0.5)
axs[2].grid(True)
axs[2].set_title('ACF weekly sales')

# monthly 
temp_acf = list(acf(monthly_sales.Value))[:70]
markerline1, stemlines1, baseline = axs[3].stem(range(len(temp_acf)), temp_acf, use_line_collection = True)
plt.setp(stemlines1, 'linewidth', 0.5)
axs[3].grid(True)
axs[3].set_title('ACF monthly sales')

fig.set_size_inches(46, 18)
plt.show()