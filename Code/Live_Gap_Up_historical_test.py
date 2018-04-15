import kiteconnect
import metaData
import corefunctions as core
from datetime import datetime
import numpy as np
import pandas as pd
import pickle
import keys
#import autologin_kiteconnect

current_time = datetime.now()
print("Program started at:",current_time)
api_key = keys.getApiKey()
access_token = metaData.getAccessToken()
kws = kiteconnect.KiteTicker(api_key,access_token)
kite = kiteconnect.KiteConnect(api_key,access_token)
All_NFO_EQ = metaData.getNSEFOStocks(kite,False)
All_NFO_EQ.sort()
list_NSE_instruments = kite.instruments(exchange = kite.EXCHANGE_NSE)

print("Getting the previous day high values")
try:
    pickle_file = open('Prev_day_high.pickle','rb')
    pickle_file_date = pickle.load(pickle_file)
    prev_day_high = pickle.load(pickle_file)
    pickle_file.close()
except:
    print("Getting the values again today")
    core.prev_day_high(All_NFO_EQ,kite)
    pickle_file = open('Prev_day_high.pickle','rb')
    pickle_file_date = pickle.load(pickle_file)
    prev_day_high = pickle.load(pickle_file)

if pickle_file_date.date() == datetime.today().date():
    print("Got previous day high values for:",pickle_file_date.date())
else:
    print("Got the previous day high values for:",pickle_file_date.date())
    print("Getting the values again today")
    core.prev_day_high(All_NFO_EQ,kite)
    pickle_file = open('Prev_day_high.pickle','rb')
    pickle_file_date = pickle.load(pickle_file)
    prev_day_high = pickle.load(pickle_file)

all_gapped_up = []
today = str(datetime.now().date())
max_percent = 2
#Write code for gap up strategy here.
def start_gap_up():
    #all_gapped_up = [{'Instrument':738561,'Gap_Up_Percent':1.9,'Open Price':25},{'Instrument':424961,'Gap_Up_Percent':2,'Open Price':200},{'Instrument':160001,'Gap_Up_Percent':1.3,'Open Price':2500}]
    print("Staring gap up strategy")
    gapup_df = pd.DataFrame(all_gapped_up)
    gapup_df = gapup_df.sort_values('Gap_Up_Percent',ascending = False)
    gapup_df = gapup_df[gapup_df['Gap_Up_Percent']<=max_percent]
    print("All gapped up stocks:")
    print(gapup_df)
    gapup_df = gapup_df.head(4)
    stocks = gapup_df['Instrument'].values
    stocks_prices = gapup_df['Open Price'].values
    print("The top four stocks less than two percent are:")
    print(stocks)
    #Placing order for stocks
    print("Preparing for placing orders at:",datetime.now())
    for index in range(gapup_df.shape[0]):
        open_price = stocks_prices[index]
        quantity = 1
        #quantity = int(capital/open_price)
        tradingsymbol = metaData.getTradingsymbol(stocks[index],list_NSE_instruments)
        print("Placing MIS order for:",tradingsymbol,"at:",datetime.now())
        print(tradingsymbol,"Stock price",stocks_prices[index])
        kite.place_order('REGULAR',kite.EXCHANGE_NSE,tradingsymbol,'SELL',quantity,'MIS','LIMIT',10)
    current_time = datetime.now()
    print("Strategy execution completed at:",current_time)

i = 0
while i < len(All_NFO_EQ):
    instrument = All_NFO_EQ[i]
    while True:
        try:
            today_open_price = kite.historical_data(instrument,today,today,'day')[0]['open']
            #print(today_open_price)
            break
        except Exception as e:
            #print(i,e)
            continue
    print(i,instrument)
    i+=1
    if today_open_price > prev_day_high[instrument]:
        high_prev_day = prev_day_high[instrument]
        gap_up_percent = (today_open_price - high_prev_day)*100.0/high_prev_day
        tradingsymbol = metaData.getTradingsymbol(instrument,list_NSE_instruments)
        all_gapped_up.append({'Instrument':instrument,'Gap_Up_Percent':gap_up_percent,'Open Price':today_open_price,'Trading Symbol':tradingsymbol})

start_gap_up()
#gapup_df = pd.DataFrame(all_gapped_up)
#gapup_df = gapup_df.sort_values('Gap_Up_Percent',ascending = False)
#print(gapup_df)
