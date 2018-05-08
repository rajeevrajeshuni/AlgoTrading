"""
Strategy 1 - This strategy selects instruments which opened higher than previous day high. Short them at day open with
SL and Target  or if both values are not hit in the day close the position at at 3:15pm. Only works with equity.
"""
import kiteconnect
import pandas as pd
import numpy as np
import time
import metaData
from datetime import datetime,timedelta
#CurrentDay_data in array of dictionaries received for the day from 9:15 to 15:15 from zerodha kite.
#Returns a list with the format
""" Date, Time since 2000, Trading Symbol, Instrumen Token, gap up percentage, position type(short,long), position open price,
position open time, position close price, position close time, total profit, profit percentage """
def applygapup_day(instrument,currentDay_data,prevDay_high,interval,kite):
    #target_list = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9]
    #stop_loss_list = [2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3.0]
    #target_list = [0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5,3.75,4,4.25,4.5,4.75,5]
    #stop_loss_list = [2,2.25,2.5,2.75,3]
    target_list = [5]
    stop_loss_list = [2]
    if currentDay_data.shape[0] == 0:
        return None
    tradingsymbol = currentDay_data.iloc[0:1]['tradingsymbol'].values[0]
    t = datetime.now()
    currentDay_open = currentDay_data.iloc[0:1]['open'].values[0]
    ans = []
    if currentDay_open > prevDay_high:
        gapup_percent = ((currentDay_open-prevDay_high)*100.0)/prevDay_high
        date = currentDay_data.iloc[0:1]['date'].values[0]
        date = str(date)[0:10]
        position_type = 'short'
        position_open_price = currentDay_open
        position_open_time = '09:15:00'
        currentDay_data_high = currentDay_data['high'].values
        currentDay_data_low = currentDay_data['low'].values
        currentDay_data_date = currentDay_data['date'].values
        for target_percent in target_list:
            target_percent = target_percent/100
            for stop_loss_percent in stop_loss_list:
                stop_loss_percent = stop_loss_percent/100
                target_price = position_open_price*(1-target_percent)
                stop_loss = position_open_price*(1+stop_loss_percent)
                finished = False
                if currentDay_data[currentDay_data['high'] >= stop_loss].shape[0] == 0:
                    if currentDay_data[currentDay_data['low'] <= target_price].shape[0] == 0:
                        position_close_price = currentDay_data['close'].values[-1]
                        position_close_time = "15:15:00"
                        total_profit =  position_open_price - position_close_price
                        finished = True
                for index in range(0,currentDay_data.shape[0]):
                    if finished == True:
                        break
                    #candle = currentDay_data.iloc[index:index+1]
                    hit_target = (currentDay_data_low[index] <= target_price)
                    hit_stoploss = (currentDay_data_high[index] >= stop_loss)
                    if hit_target and hit_stoploss:
                        #Reached an anamoly, both stop loss and target can be hit in the 15 minute candle
                        print("anamoly:",instrument,currentDay_data_date[index],target_percent,stop_loss_percent)
                        #Assuming stoploss was hit first
                        position_close_price = stop_loss
                        position_close_time = str(currentDay_data_date[index])[11:19]
                        total_profit = position_open_price - stop_loss
                        #print(candle)
                        finished = True
                        break
                    elif hit_target:
                        position_close_price = target_price
                        position_close_time = str(currentDay_data_date[index])[11:19]
                        total_profit = position_open_price - target_price
                        finished = True
                        #print(candle)
                        break
                    elif hit_stoploss:
                        position_close_price = stop_loss
                        position_close_time = str(currentDay_data_date[index])[11:19]
                        total_profit = position_open_price - stop_loss
                        finished = True
                        #print(candle)
                        break
                if not finished:
                    #Closing the position at 15:15:00
                    position_close_price = currentDay_data['close'].values[-1]
                    position_close_time = "15:15:00"
                    total_profit =  position_open_price - position_close_price
                profit_percent = (total_profit*100.0)/position_open_price
                ans.append({'Target':target_percent,'Stop loss':stop_loss_percent,'Date':date,'Gap_Up_Percent':gapup_percent,'Trading_Symbol':tradingsymbol,'instrument':instrument,'Previous_Day_High':prevDay_high,"Current_Day_Open":currentDay_open,'Position_Type':'short','Position_Open_Price':position_open_price,'Position_Open_Time':position_open_time,'Position_Close_Price':position_close_price,'Position_Close_Time':position_close_time,'Total_Profit':total_profit,'Profit_Percent':profit_percent})
        return ans
    return None
#apply gapup for all NSE FO Stocks
def applygapup(kite):
    t = datetime.now()
    ans = []
    All_NSE_FO_EQ = metaData.getNSEFOStocks(kite)
    tradingsymbols_NSE_FO_EQ = metaData.getTradingsymbol_NSE(All_NSE_FO_EQ,kite)
    #years = [2014,2015,2016,2017,2018]
    years = [2018]
    for year in years:
        t = datetime.now()
        ans = []
        file_name = str(year)+'_15minute.csv'
        day_file_name = str(year)+'_day.csv'
        df_year_15min = pd.read_csv(file_name)
        df_year_day = pd.read_csv(day_file_name)
        df_year_15min_open = df_year_15min[df_year_15min['onlytime'] == '09:15:00']
        onlydates_set = list(set(list(df_year_15min['onlydate'].values)))
        onlydates_set.sort()
        print(onlydates_set)
        onlydates_day_list = list(df_year_day['onlydate'].values)
        #Ignoring first two days - Do again for them
        for index in range(2,len(onlydates_set)):
            current_day = onlydates_set[index]
            current_day_date = int(current_day[0:4])
            current_day_month = int(current_day[5:7])
            current_day_day = int(current_day[8:10])
            temp = datetime(current_day_date,current_day_month,current_day_day) - timedelta(days=1)
            prev_day_onlydate = temp.strftime("%Y-%m-%d")
            while True:
                if prev_day_onlydate in onlydates_day_list:
                    break
                temp-=timedelta(days=1)
                prev_day_onlydate = temp.strftime("%Y-%m-%d")
            #print(current_day,prev_day_onlydate)
            for inst_index in range(0,len(All_NSE_FO_EQ)):
                t1 = datetime.now()
                instrument = All_NSE_FO_EQ[inst_index]
                temp = df_year_day[(df_year_day['onlydate'] == prev_day_onlydate) & (df_year_day['instrument_token'] == instrument)]
                if temp.shape[0] == 0:
                    print("No data:",tradingsymbols_NSE_FO_EQ[inst_index],current_day)
                    continue
                prev_day_high = temp['high'].values[0]
                if inst_index == 0:
                    print(inst_index,instrument,index,current_day,prev_day_onlydate,datetime.now())
                current_day_open = df_year_15min_open[(df_year_15min_open['onlydate'] == current_day) & (df_year_15min_open['instrument_token'] == instrument)]
                if current_day_open.shape[0] == 0:
                    continue
                current_day_open = current_day_open.iloc[0:1]['open'].values[0]
                t1 = datetime.now() - t1
                #print(inst_index,"First part time:",t1)
                if not (current_day_open > prev_day_high):
                    continue
                df_current_day_15min = df_year_15min[(df_year_15min['onlydate'] == current_day) & (df_year_15min['instrument_token']==instrument)]
                t = datetime.now()
                new_entry = applygapup_day(instrument,df_current_day_15min,prev_day_high,'15minute',kite)
                ans+=new_entry
                t = datetime.now() - t
                #print(inst_index,"Second part time:",t)
        dataframe = pd.DataFrame(ans)
        dataframe = dataframe[['Target','Stop loss','Trading_Symbol','instrument','Date','Previous_Day_High','Current_Day_Open','Gap_Up_Percent','Position_Type','Position_Open_Price','Position_Open_Time','Position_Close_Price','Position_Close_Time','Total_Profit','Profit_Percent']]
        print(year,dataframe.shape)
        #_all_possibilities
        dataframe.to_csv('Gap_Up_Backtest_'+str(year)+'_30_4_18.csv',sep=',')
        t = datetime.now() - t
        print("Time taken:",t,"for:",year)
    #return ans

def dfToListOfdict(df):
    columns = list(df.columns)
    rows = df.shape[0]
    temp = {}
    ans = []
    for column in columns:
        temp[column] = list(df[column].values)
    for row in range(0,rows):
        temp_ans = {}
        for column in columns:
            temp_ans[column] = temp[column][row]
        ans.append(temp_ans)
    return ans
