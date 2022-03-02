import pandas as pd

def add_long_range_hod(hourly_sales,aux_hourly_sales,num_days):
  '''
  given 'num_years',
  return the same day of week, hour of 'day num_years' years ago
  '''
  num_hours =   num_days*24
  col_name = str(num_days)+'_DAYS_ago'+'_same_hod'
  hourly_sales[col_name] = hourly_sales.num_of_hours - num_hours

  temp_aux_hourly_sales = aux_hourly_sales.copy(deep = True)
  temp_aux_hourly_sales = temp_aux_hourly_sales[['num_of_hours','Value']]
  temp_aux_hourly_sales.rename(columns = {'num_of_hours':col_name, 'Value':'AR__sales_'+col_name},inplace = True)
  hourly_sales = hourly_sales.merge(temp_aux_hourly_sales, how = 'left', on = col_name)
  hourly_sales.drop(columns = [col_name],axis = 1, inplace = True)
  return hourly_sales

def add_mid_range_features(hourly_sales,aux_hourly_sales,num_weeks):
  '''
  add features to pandas df 'hour_sales', specifically, +/- 1 hour of hourly sales from 'num_weeks' ago were added
  '''
  num_hours = num_weeks * 168 # 168 hours in 1 week
  for i in [0]:#: # +/- 1 hour # [-1,0,1]; exactly use [0]
    sign = ('p' if i>=0 else 'm')
    col_name = str(num_weeks) + '_weeks_ago_'+sign+'_'+str(abs(i))+'h'#temp col name for some time ago specified by num_weeks
    hourly_sales[col_name] = hourly_sales.num_of_hours - (num_hours+i)
    temp_aux_hourly_sales = aux_hourly_sales.copy(deep = True)
    temp_aux_hourly_sales = temp_aux_hourly_sales[['num_of_hours','Value']]
    temp_aux_hourly_sales.rename(columns = {'num_of_hours':col_name, 'Value':'AR__sales_'+col_name},inplace = True)
    hourly_sales = hourly_sales.merge(temp_aux_hourly_sales, how = 'left', on = col_name)
    hourly_sales.drop(columns = [col_name],axis = 1, inplace = True)
  return hourly_sales

def add_short_range_features(hourly_sales,aux_hourly_sales,num_days):
  '''
  add features to pandas df 'hour_sales', specifically, +/- 1 hour of hourly sales from 'num_days' ago were added
  '''
  num_hours = num_days * 24 # 24 hours in 1 day
  for i in [0]:#: # +/- 1 hour [-1,0,1]; exactly use [0]
    sign = ('p' if i>=0 else 'm')
    col_name = str(num_days) + '_days_ago_'+sign+'_'+str(abs(i))+'h'#temp col name for some time ago specified by num_days
    hourly_sales[col_name] = hourly_sales.num_of_hours - (num_hours+i)
    temp_aux_hourly_sales = aux_hourly_sales.copy(deep = True)
    temp_aux_hourly_sales = temp_aux_hourly_sales[['num_of_hours','Value']]
    temp_aux_hourly_sales.rename(columns = {'num_of_hours':col_name, 'Value':'AR__sales_'+col_name},inplace = True)
    hourly_sales = hourly_sales.merge(temp_aux_hourly_sales, how = 'left', on = col_name)
    hourly_sales.drop(columns = [col_name],axis = 1, inplace = True)
  return hourly_sales


def add_micro_range_features(hourly_sales,aux_hourly_sales):
  '''
  add features to pandas df 'hour_sales', specifically, the  hourly sales from previous 1-22 hours ago

  '''
  for i in range(1,23):# (original) 1-23 hours ago: range(1,23); 
    col_name = 'pre_'+str(i)+'_h'#temp col name for some time ago specified by num_days
    hourly_sales[col_name] = hourly_sales.num_of_hours - i

    temp_aux_hourly_sales = aux_hourly_sales.copy(deep = True)
    temp_aux_hourly_sales = temp_aux_hourly_sales[['num_of_hours','Value']]
    temp_aux_hourly_sales.rename(columns = {'num_of_hours':col_name, 'Value':'AR__sales_'+col_name},inplace = True)
    # join on 'col_name'
    hourly_sales = hourly_sales.merge(temp_aux_hourly_sales, how = 'left', on = col_name)
    # remove temparary column 'col_name'
    hourly_sales.drop(columns = [col_name],axis = 1, inplace = True)
  return hourly_sales



thanksgiving_list = ['2013-11-28','2014-11-27','2015-11-26','2016-11-24','2017-11-23','2018-11-22'] 
thanksgiving_dic = {int(item[0:4]): pd.to_datetime(item) for item in thanksgiving_list}

def calc_thanksgiving_same_year(date):
  '''
  given a date (pd.datetime)
  return thanksgiving_same_year (datetime format)
  '''
  return thanksgiving_dic[date.year]



def calc_christmas_same_year(date):
  '''
  given a date (pd.datetime)
  return thanksgiving_same_year (datetime format)
  '''
  return pd.to_datetime(str(date.year)+'-12-25') 

def calc_next_immediate_christmas(date):
  '''
  given a date (pd.datetime)
  return next immediate christmas in pd.datetime
  '''
  same_year_christmas = calc_christmas_same_year(date)
  next_year_christmas = pd.to_datetime(str(date.year+1)+'-12-25') 
  return same_year_christmas if date <= same_year_christmas else next_year_christmas

def calc_row_index_hourly(feature_str):
  '''
  given a column/feature name, return the offset in hours
  idea, column name suggest offset_hours  hours ago sales/traffic 
  '''
  num_weeks = 0
  num_days = 0
  num_hours = 0

  if feature_str[12:17] =='weeks':
    num_weeks = int(feature_str[10])
    num_days = 0
    num_hours = int(feature_str[-2])
    if feature_str[-4] == 'm':
      num_hours *= -1

  elif feature_str[12:16] =='days':
    num_days = int(feature_str[10])
    num_hours = int(feature_str[-2])
    if feature_str[-4] == 'm':
      num_hours *= -1
  elif feature_str[10:13] =='pre':
    num_hours = int(feature_str[-3])
    if feature_str[-4].isnumeric():
      num_hours += int(feature_str[-4])*10


  offset_hours = num_weeks * 168 + num_days*24 + num_hours
  return offset_hours

def find_the_same_week(datetime):
  '''
  given a pandas datetime
  return the week number
  '''
  return



# traffic = pd.read_csv('data/explored_traffic.csv')
# hourly_traffic = pd.read_csv('data/hourly_traffic.csv')
# weekly_traffic = pd.read_csv('data/weekly_traffic.csv')
# monthly_traffic = pd.read_csv('data/monthly_traffic.csv')

# traffic.hour = pd.to_datetime(traffic.hour)
# traffic.Date = pd.to_datetime(traffic.Date)
# hourly_traffic.hour = pd.to_datetime(hourly_traffic.hour)