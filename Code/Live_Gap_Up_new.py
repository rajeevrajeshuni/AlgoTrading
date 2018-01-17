import kiteconnect
import metaData
import corefunctions as core
from datetime import datetime
import numpy as np
import pandas as pd
import pickle
import autologin_kiteconnect

current_time = datetime.now()
print("Program started at:",current_time)
api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()
if access_token == None:
    autologin_kiteconnect.create_access_token()
    access_token = metaData.getAccessToken()
kite = kiteconnect.KiteConnect(api_key,access_token)
All_NFO_EQ = metaData.getNSEFOStocks(kite,False)
All_NFO_EQ.sort()
max_percent = 2
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
open_price_checked = []
start_hr = 9
start_min = 15
capital_each_stock = 150000


#Write code for gap up strategy here.
def start_gap_up():
    #all_gapped_up = [{'Instrument':738561,'Gap_Up_Percent':1.9,'Open Price':25},{'Instrument':424961,'Gap_Up_Percent':2,'Open Price':200},{'Instrument':160001,'Gap_Up_Percent':1.3,'Open Price':2500}]
    print("Staring gap up strategy")
    gapup_df = pd.DataFrame(all_gapped_up)
    gapup_df = gapup_df.sort_values('Gap_Up_Percent',ascending = False)
    gapup_df = gapup_df[gapup_df['Gap_Up_Percent']<=max_percent]
    gapup_df = gapup_df.head(4)
    stocks = gapup_df['Instrument'].values
    stocks_prices = gapup_df['Open Price'].values
    print("The top four stocks less than two percent are:")
    print(stocks)
    #Placing order for stocks
    print("Preparing for placing orders at:",datetime.now())
    for index in range(gapup_df.shape[0]):
        capital = capital_each_stock
        open_price = stocks_prices[index]
        #quantity = int(capital/open_price)
        quantity = 1
        tradingsymbol = metaData.getTradingsymbol(stocks[index],list_NSE_instruments)
        print("Placing MIS order for:",tradingsymbol,"at:",datetime.now())
        kite.place_order('REGULAR',kite.EXCHANGE_NSE,tradingsymbol,'SELL',quantity,'MIS','LIMIT',stocks_prices[index])
    current_time = datetime.now()
    print("Strategy execution completed at:",current_time)
    #Ending code - only for debugging
    gapup_df = pd.DataFrame(all_gapped_up)
    gapup_df = gapup_df.sort_values('Gap_Up_Percent',ascending = False)
    gapup_df = gapup_df[gapup_df['Gap_Up_Percent']<=max_percent]
    gapup_df['Trading Symbol'] = metaData.getTradingsymbol_NSE(gapup_df['Instrument'].values,kite)
    print("All gapped up stocks with trading symbol:")
    print(gapup_df)

def get_All_gapped_up_stocks():
    ohlc_all = []
    while True:
        try:
            ohlc_all = kite.quote(All_NFO_EQ)
            if len(ohlc_all)>0:
                keys = list(ohlc_all.keys())
                timestamp = ohlc_all[keys[0]]['timestamp']
                if not (timestamp.date() == datetime.today().date() and timestamp.hour>=start_hr and timestamp.minute>=start_min):
                    continue
        except:
            continue
        if len(ohlc_all) == len(All_NFO_EQ):
            break
    for instrument in All_NFO_EQ:
        open_price = ohlc_all[str(instrument)]['ohlc']['open']
        prev_day_high_instrument = prev_day_high[instrument]
        if open_price > prev_day_high_instrument:
            gap_up_percent = (open_price - prev_day_high_instrument)*100.0/prev_day_high_instrument
            all_gapped_up.append({'Instrument':instrument,'Gap_Up_Percent':gap_up_percent,'Open Price':open_price})
    start_gap_up()
get_All_gapped_up_stocks()
