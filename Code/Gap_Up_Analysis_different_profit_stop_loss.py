#This file is for Gap Up data analysis when the file has different target and stoploss values

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

def process(df,max_percent,top):
    df = df[['Date','Gap_Up_Percent','Profit_Percent']]
    df = df[df['Gap_Up_Percent']<=max_percent]
    df_date_sorted = df.sort_values(['Date','Gap_Up_Percent'],ascending = [True,False])
    df_date_sorted['Trade order in day'] = df_date_sorted.groupby('Date').cumcount() + 1
    df_date_top_gap_up = df_date_sorted[df_date_sorted['Trade order in day']<=top]
    final = df_date_top_gap_up.groupby('Date').agg({'Profit_Percent':np.mean})
    profit_percent_day = list(final.values)
    dates = list(final.index)
    new_profit_percent_day_compounding = []
    new_profit_percent_day_total = []
    compounding_val = 1
    total_val = 0
    for p in profit_percent_day:
      #Compounding of the returns
      compounding_val*=(1+p[0]*0.01)
      total_val+=p[0]
      new_profit_percent_day_compounding.append(compounding_val)
      new_profit_percent_day_total.append(total_val)
    new_dates = []
    for d in dates:
        d = d.split('-')
        new_dates.append(datetime(int(d[0]),int(d[1]),int(d[2])))
    return new_profit_percent_day_total,new_profit_percent_day_compounding,new_dates,final

def max_draw_down(profit_percent_day):
    max_negative = 0
    temp_negative = 0
    temp_days = 0
    max_days = 0
    for p in profit_percent_day:
        temp_negative+=p[0]
        temp_days+=1
        if temp_negative > 0:
            temp_negative = 0
            temp_days = 0
        if max_negative > temp_negative:
            max_negative = temp_negative
            max_days = temp_days
    return [max_negative*-1,max_days]

def win_loss(profit_percent_day):
    profit_percent_arr = np.array(profit_percent_day)
    profit_percent_arr[profit_percent_arr < 0] = -1
    profit_percent_arr[profit_percent_arr > 0] = 0
    loss_percent = (profit_percent_arr.sum()*100)/len(profit_percent_day)
    loss_percent = -1*loss_percent
    return [100-loss_percent,loss_percent]
#files = {2016:'Gap_Up_Backtest_All_FO_2016.csv',2017:'Gap_Up_Backtest_All_FO_2017.csv',2018:'Gap_Up_Backtest_2018-01-01_2018-03-22.csv'}
file_prefix = 'Gap_Up_Backtest_'
file_suffix = '_30_3_18.csv'
max_percent = 2 #The stocks which gapped up above this value are not considered.
#top is key for all of them
profit_percent_day = {} #profit percent for all days in a year
dates = {} #all days when gap up occured in a year
total_profit = {}
capital_compounding = {}
compounding_day = {}
draw_down = {}
year = [2014,2015,2016,2017,2018]
file_name = file_prefix + str(2017) + file_suffix


df = pd.read_csv(file_name)
target = list(set(df['Target'].values))
target.sort()
stop_loss = list(set(df['Stop loss'].values))
stop_loss.sort()

print("Year,Target,Stop Loss,No. of top stocks,Capital at end of year,Total profit percent,Maximum Draw Down,Days for Maximum Draw Down,Win Loss Ratio")
for y in year:
    file_name = file_prefix + str(y) + file_suffix
    #print(f,file_path)
    df_1 = pd.read_csv(file_name)
    #print("For year:",y)
    for tar in target:
        for st in stop_loss:
            df = df_1[(df_1['Target'] == tar) & (df_1['Stop loss'] == st)]
            #print("For target:",(tar*100),"% and stop loss:",(st*100),"%")
            for top in range(1,10):
                key = (tar,st,top)
                temp_profit_percent,temp_capital_compounding,temp_dates,final = process(df,max_percent,top)
                draw_down[key] = max_draw_down(final.values)
                profit_percent_day[key] = temp_profit_percent
                dates[key] = temp_dates
                compounding_day[key] = temp_capital_compounding
                #print(final)
                total_profit[key] = temp_profit_percent[-1]
                win_loss_ratio = win_loss(final.values)
                capital_compounding[key] = temp_capital_compounding[-1]
                #print("Top: ",top,"Total capital at end:",capital_compounding[key])
                #print("Top: ",top,"Total profit percent:",total_profit[key])
                #print("Top: ",top,"Maximum Draw Down:",draw_down[key])
                #print("Top: ",top,"Win Loss Ratio",win_loss_ratio)
                win_loss_ratio[0] = int(win_loss_ratio[0]+0.5)
                win_loss_ratio[1] = int(win_loss_ratio[1]+0.5)
                print(str(y)+","+str(tar)+","+str(st)+","+str(top)+","+str(capital_compounding[key])+","+str(total_profit[key])+","+str(draw_down[key][0])+","+str(draw_down[key][1])+","+str(win_loss_ratio[0])+":"+str(win_loss_ratio[1]))
    #print("==============================================================================")
