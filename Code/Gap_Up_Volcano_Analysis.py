import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

def process(df,max_percent,top,min_ratio):
    df = df[['Date','Gap_Up_Percent','Profit_Percent_x','Avg_Volume_Last_4_Days_Today_Volume_Ratio']]
    df = df[(df['Gap_Up_Percent']<=max_percent) & (df['Avg_Volume_Last_4_Days_Today_Volume_Ratio']>=min_ratio)]
    df_date_sorted = df.sort_values(['Date','Gap_Up_Percent'],ascending = [True,False])
    df_date_sorted['Trade order in day'] = df_date_sorted.groupby('Date').cumcount() + 1
    df_date_top_gap_up = df_date_sorted[df_date_sorted['Trade order in day']<=top]
    final = df_date_top_gap_up.groupby('Date').agg({'Profit_Percent_x':np.mean})
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
    for p in profit_percent_day:
        temp_negative = min(temp_negative+p[0],0)
        max_negative = min(max_negative,temp_negative)
    return max_negative*-1

max_percent = 2 #The stocks which gapped up above this value are not considered.
min_ratio = 2
top_stocks = 10
#top is key for all of them
profit_percent_day = {} #profit percent for all days in a year
dates = {} #all days when gap up occured in a year
total_profit = {}
capital_compounding = {}
compounding_day = {}
draw_down = {}
year = [2015,2016,2017]
file_names = ['Gap_Volcano_2015_Data.csv','Gap_Volcano_2016_Data.csv','Gap_Volcano_2017_Data.csv']
for i in range(len(year)):
    y = year[i]
    file_name = file_names[i]
    df = pd.read_csv(file_name)
    for top in range(1,top_stocks):
        temp_profit_percent,temp_capital_compounding,temp_dates,final = process(df,max_percent,top,min_ratio)
        draw_down[top] = max_draw_down(final.values)
        profit_percent_day[top] = temp_profit_percent
        dates[top] = temp_dates
        compounding_day[top] = temp_capital_compounding
        total_profit[top] = temp_profit_percent[-1]
        capital_compounding[top] = temp_capital_compounding[-1]
        print(y,"Top: ",top,"Total capital at end:",capital_compounding[top])
        print(y,"Top: ",top,"Total profit percent:",total_profit[top])
        print(y,"Top: ",top,"Maximum Draw Down:",draw_down[top])
    fig = plt.figure()
    for top in range(1,top_stocks):
        plt.plot(dates[top],profit_percent_day[top],label = 'Top: ' + str(top))
    plt.xlabel('All dates in '+str(y))
    plt.ylabel('Total profit(starting from 0 at the start)')
    plt.legend()
    fig.savefig('Gap_Up_'+str(y)+'_different_top_total_profit_1.png',dpi=fig.dpi)

    fig = plt.figure()
    for top in range(1,top_stocks):
        plt.plot(dates[top],compounding_day[top],label = 'Top: ' + str(top))
    plt.xlabel('All dates in '+str(y))
    plt.ylabel('Total capital(starting from 1 at the start)')
    plt.legend()
    fig.savefig('Gap_Up_'+str(y)+'_different_top_compounding_1.png',dpi=fig.dpi)
