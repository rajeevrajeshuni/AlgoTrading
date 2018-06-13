import pandas as pd
import numpy as np
from datetime import datetime


def process_nth(df,max_percent,top):
    #print(df.head())
    print("Printing the value of top nth stop everyday")
    df = df[['Date','Gap_Up_Percent','Profit_Percent']]
    df = df[df['Gap_Up_Percent']<=max_percent]
    df_date_sorted = df.sort_values(['Date','Gap_Up_Percent'],ascending = [True,False])
    df_date_sorted['Trade order in day'] = df_date_sorted.groupby('Date').cumcount() + 1
    df_date_top_gap_up = df_date_sorted[df_date_sorted['Trade order in day']==top]
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


def process(df,max_percent,top):
    print("Printing the average of top n stocks every day")
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


#This calculates the R value in kelly's ratio
def get_R(profit_percent_day):
    #print(profit_percent_day)
    total_gain = 0
    total_loss = 0
    gain_trades = 0
    loss_trades = 0
    for p in profit_percent_day:
        p = p[0]
        if p < 0:
            total_loss+=p
            loss_trades+=1
        else:
            total_gain+=p
            gain_trades+=1
    avg_gain = total_gain/gain_trades
    avg_loss = abs(total_loss/loss_trades)
    #print(avg_gain,avg_loss)
    return avg_gain/avg_loss


#printed = True
#files = {2015:'Gap_Up_Backtest_NiftyMidCap50_2015.csv',2016:'Gap_Up_Backtest_NiftyMidCap50_2016.csv',2017:'Gap_Up_Backtest_NiftyMidCap50_2017.csv'}
files = {2015:'Gap_Up_Backtest_All_FO_2015.csv',2016:'Gap_Up_Backtest_All_FO_2016.csv',2017:'Gap_Up_Backtest_All_FO_2017.csv'}
#file_prefix = 'Gap_Up_Backtest_'
#file_suffix = '_30_3_18.csv'
max_percent = 2 #The stocks which gapped up above this value are not considered.

#top is key for all of them
profit_percent_day = {} #profit percent for all days in a year
dates = {} #all days when gap up occured in a year
total_profit = {}
capital_compounding = {}
compounding_day = {}
draw_down = {}
draw_down_days = {}
#year = [2015,2016,2017,2018]
#year = [2018]
n_days={}
df_list = []
for y in files:
    #file_name = file_prefix + str(y) + file_suffix
    file_name = files[y]
    n_days[y]=[]
    #print(f,file_path)
    df = pd.read_csv(file_name)
    for top in range(1,33):
        temp_profit_percent,temp_capital_compounding,temp_dates,final = process(df,max_percent,top)
        draw_down[top] = max_draw_down(final.values)[0]
        draw_down_days[top] = max_draw_down(final.values)[1]
        #print(len(final))
        n_days[y].append(len(final))
        profit_percent_day[top] = temp_profit_percent
        dates[top] = temp_dates
        compounding_day[top] = temp_capital_compounding
        total_profit[top] = temp_profit_percent[-1]
        capital_compounding[top] = temp_capital_compounding[-1]
        win_loss_ratio = win_loss(final.values)
        win_loss_ratio[0] = int(win_loss_ratio[0]+0.5)
        win_loss_ratio[1] = int(win_loss_ratio[1]+0.5)
        win_loss_ratio_str = str(win_loss_ratio[0])+":"+str(win_loss_ratio[1])
        R_kelly = get_R(final.values)
        df_list.append({'Year':y,'Top':top,'Total Capital at End':capital_compounding[top],'Total Profit Percent':total_profit[top],'Maximum DD':draw_down[top],'DD Days':draw_down_days[top],'Win Loss Ratio':win_loss_ratio_str,'R_Kelly':R_kelly})
        #print(y,"Top: ",top,"Total capital at end:",capital_compounding[top])
        #print(y,"Top: ",top,"Total profit percent:",total_profit[top])
        #print(y,"Top: ",top,"Maximum Draw Down:",draw_down[top])
    """fig = plt.figure()
    for top in range(1,10):
        plt.plot(dates[top],profit_percent_day[top],label = 'Top: ' + str(top))
    plt.xlabel('All dates in '+str(y))
    plt.ylabel('Total profit(starting from 0 at the start)')
    plt.legend()
    fig.savefig('Gap_Up_'+str(y)+'_different_top_total_profit_1.png',dpi=fig.dpi)

    fig = plt.figure()
    for top in range(1,10):
        plt.plot(dates[top],compounding_day[top],label = 'Top: ' + str(top))
    plt.xlabel('All dates in '+str(y))
    plt.ylabel('Total capital(starting from 1 at the start)')
    plt.legend()
    fig.savefig('Gap_Up_'+str(y)+'_different_top_compounding_1.png',dpi=fig.dpi)"""
print("Printing Gap Up Analysis")
final_ans = pd.DataFrame(df_list)
print(final_ans.to_string())
print("Printing the number of trading days")
df = pd.DataFrame(n_days)
print(df.to_string())
#final_ans.to_csv('Gap_Up_Analysis_top_n_average.csv',sep=',')
