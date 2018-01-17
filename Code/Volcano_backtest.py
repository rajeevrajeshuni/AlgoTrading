import metaData
import corefunctions as core
import pandas as pd
import numpy as np
from datetime import datetime,timedelta
import kiteconnect

api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()
if access_token == None:
    autologin_kiteconnect.create_access_token()
    access_token = metaData.getAccessToken()
kite = kiteconnect.KiteConnect(api_key,access_token)

file_names = ['2014_day.csv','2015_day.csv','2016_day.csv','2017_day.csv','2018_day.csv']
All_NFO_EQ = metaData.getNSEFOStocks(kite,False)
All_NFO_EQ_tradingsymbol = metaData.getNSEFOStocks_instrument_tradingsymbol(kite)

check_prev_days = 4

for fname in file_names:
    #count = 0
    df = pd.read_csv(fname)
    ans = []
    for instrument_index in range(len(All_NFO_EQ)):
        instrument = All_NFO_EQ[instrument_index]
        df_instrument = df[df['instrument_token']==instrument]
        df_instrument = df_instrument.sort_values('onlydate',ascending = True)
        onlydates = list(set(df_instrument['onlydate'].values))
        onlydates.sort()
        df_instrument_volume = list(df_instrument['volume'].values)
        df_instrument_close = list(df_instrument['close'].values)
        df_instrument_open = list(df_instrument['open'].values)
        if not (len(df_instrument_volume) == len(onlydates)):
            print("Error!!",instrument,fname,len(onlydates),len(df_instrument_volume),len(df_instrument_volume))
            onlydates_temp = list(df_instrument['onlydate'].values)
            onlydates_temp.sort()
            print_list(onlydates_temp)
            break
        for date_index in range(check_prev_days,len(onlydates)-1):
            day_0_volume = df_instrument_volume[date_index - 4]
            day_1_volume = df_instrument_volume[date_index - 3]
            day_2_volume = df_instrument_volume[date_index - 2]
            day_3_volume = df_instrument_volume[date_index-1]
            current_date_volume = df_instrument_volume[date_index]
            avg_volume_last_4_days = (day_0_volume + day_1_volume + day_2_volume + day_3_volume)*0.25
            if avg_volume_last_4_days< current_date_volume:
                #Eligible for momemtum strategy here
                #Buy on end of day 4 and sell at day 5 open
                #Take slippage to be 0.21%
                avg_volume_last_4_days_today_volume_ratio = (current_date_volume*1.0)/avg_volume_last_4_days
                current_date = onlydates[date_index]
                next_date = onlydates[date_index+1]
                tradingsymbol = All_NFO_EQ_tradingsymbol[instrument]
                profit = df_instrument_open[date_index+1] - df_instrument_close[date_index+1]
                profit_percent = (profit*100.0)/df_instrument_open[date_index+1]
                #count+=1
                ans.append({'Trading_Symbol':tradingsymbol,'Instrument_Token':instrument,'Curreny_Day(day 4)':current_date,'Day_0_volume':day_0_volume,'Day_1_volume':day_1_volume,'Day_2_volume':day_2_volume,'Day_3_volume':day_3_volume,'Day_4_volume':current_date_volume,'Profit':profit,'Profit_Percent':profit_percent,'Next_Day_Open':df_instrument_open[date_index+1],'Next_Day_Close':df_instrument_close[date_index+1],'Avg_Volume_Last_4_Days_Today_Volume_Ratio':avg_volume_last_4_days_today_volume_ratio,'Next_Day':next_date})
    #print(fname[0:4],count)
    ans_df = pd.DataFrame(ans)
    ans_file_name = 'Volcano_4_'+fname[0:4]+'.csv'
    ans_df.to_csv(ans_file_name,sep=',')
