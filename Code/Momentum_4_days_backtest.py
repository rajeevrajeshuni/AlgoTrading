import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import corefunctions as core
import metaData
import kiteconnect

api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()
if access_token == None:
    autologin_kiteconnect.create_access_token()
    access_token = metaData.getAccessToken()
kite = kiteconnect.KiteConnect(api_key,access_token)

file_names = ['2014_day.csv','2015_day.csv','2016_day.csv','2017_day.csv','2018_day.csv']
#file_names = ['2015_day.csv']
All_NFO_EQ = metaData.getNSEFOStocks(kite,False)
All_NFO_EQ_tradingsymbol = metaData.getNSEFOStocks_instrument_tradingsymbol(kite)
#If the stock rises for these many days
check_prev_days = 4

def print_list(l):
    for i in range(len(l)):
        print(i+1,l[i])

for fname in file_names:
    df = pd.read_csv(fname)
    ans = []
    for instrument_index in range(len(All_NFO_EQ)):
        instrument = All_NFO_EQ[instrument_index]
        df_instrument = df[df['instrument_token']==instrument]
        df_instrument = df_instrument.sort_values('onlydate',ascending = True)
        onlydates = list(set(df_instrument['onlydate'].values))
        onlydates.sort()
        df_instrument_close = list(df_instrument['close'].values)
        df_instrument_open = list(df_instrument['open'].values)
        if not (len(df_instrument_close) == len(df_instrument_open) and len(df_instrument_close) == len(onlydates)):
            print("Error!!",instrument,fname,len(onlydates),len(df_instrument_close),len(df_instrument_open))
            onlydates_temp = list(df_instrument['onlydate'].values)
            onlydates_temp.sort()
            print_list(onlydates_temp)
            break
        for date_index in range(check_prev_days,len(onlydates)-1):
            day_0_close = df_instrument_close[date_index - 4]
            day_1_close = df_instrument_close[date_index - 3]
            day_2_close = df_instrument_close[date_index - 2]
            day_3_close = df_instrument_close[date_index-1]
            day_4_open = df_instrument_open[date_index]
            #day_5_open = df_instrument_open[date_index+1]
            if day_0_close<day_1_close and day_1_close < day_2_close and day_2_close<day_3_close:
                #Eligible for momemtum strategy here
                #Buy on end of day 4 and sell at day 5 open
                #Take slippage to be 0.21%
                current_date = onlydates[date_index-1]
                tradingsymbol = All_NFO_EQ_tradingsymbol[instrument]
                profit = day_5_open - day_4_close
                profit_percent = (profit*100.0)/day_4_close
                ans.append({'Trading_Symbol':tradingsymbol,'Instrument_Token':instrument,'Current_Day(day_4)':current_date,'Day_0_Close':day_0_close,'Day_1_Close':day_1_close,'Day_2_Close':day_2_close,'Day_3_Close':day_3_close,'Day_4_Close':day_4_close,'Day_5_Open':day_5_open,'Profit':profit,'Profit_Percent':profit_percent})
    ans_df = pd.DataFrame(ans)
    ans_file_name = 'Momentum_4_'+fname[0:4]+'_1.csv'
    ans_df.to_csv(ans_file_name,sep=',')
