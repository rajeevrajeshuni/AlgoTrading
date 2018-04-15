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
kws = kiteconnect.KiteTicker(api_key,access_token)
kite = kiteconnect.KiteConnect(api_key,access_token)
All_NFO_EQ = metaData.getNSEFOStocks(kite,False)
All_NFO_EQ.sort()
max_percent = 2
#print(All_NFO_EQ)
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
iterations = metaData.iterations
gapup_df = pd.DataFrame()
start_hr = 9
start_min = 15
capital_each_stock = 150000

def print_list(l):
    for i in range(len(l)):
        print(i+1,l[i])

#Write code for gap up strategy here.
def start_gap_up():
    #all_gapped_up = [{'Instrument':738561,'Gap_Up_Percent':1.9,'Open Price':25},{'Instrument':424961,'Gap_Up_Percent':2,'Open Price':200},{'Instrument':160001,'Gap_Up_Percent':1.3,'Open Price':2500}]
    print("Staring gap up strategy")
    gapup_df = pd.DataFrame(all_gapped_up)
    gapup_df = gapup_df.sort_values('Gap_Up_Percent',ascending = False)
    gapup_df = gapup_df[gapup_df['Gap_Up_Percent']<=max_percent]
    #print("All gapped up stocks:")
    #print(gapup_df)
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
        #quantity = 1
        quantity = int((capital/open_price)+0.5)
        tradingsymbol = metaData.getTradingsymbol(stocks[index],list_NSE_instruments)
        print("Placing MIS order for:",tradingsymbol,"at:",datetime.now())
        kite.place_order('REGULAR',kite.EXCHANGE_NSE,tradingsymbol,'SELL',quantity,'MIS','MARKET',stocks_prices[index])
    current_time = datetime.now()
    print("Strategy execution completed at:",current_time)
    #Ending code - only for debugging
    gapup_df = pd.DataFrame(all_gapped_up)
    gapup_df = gapup_df.sort_values('Gap_Up_Percent',ascending = False)
    gapup_df = gapup_df[gapup_df['Gap_Up_Percent']<=max_percent]
    gapup_df['Trading Symbol'] = metaData.getTradingsymbol_NSE(gapup_df['Instrument'].values,kite)
    print("All gapped up stocks with trading symbol:")
    print(gapup_df)
def initialise():
    all_gapped_up = []
    open_price_checked = []
    iterations = 0
    All_NFO_EQ.sort()

def on_ticks(kws,ticks):
    """Iterate through the list and whenever you get the first tick of a stock note that as open price
    immediately unsubsribe to the stock. Compare the open price with prev_day_high and if it is store it in a
    separate list"""
    metaData.iterations+=1
    print("Ticks:",metaData.iterations,ticks[0]['timestamp'],datetime.now())
    for tick in ticks:
        timestamp = tick['timestamp']
        #print("Tick timestamp:",timestamp,datetime.now())
        if not (timestamp.date() == datetime.today().date() and timestamp.hour>=start_hr and timestamp.minute>=start_min):
            continue
        instrument_token = tick['instrument_token']
        ltp = tick['last_price']
        if instrument_token not in open_price_checked:
            kws.unsubscribe([instrument_token])
            open_price_checked.append(instrument_token)
            if ltp > prev_day_high[instrument_token] and (instrument_token not in all_gapped_up):
                high_prev_day = prev_day_high[instrument_token]
                gap_up_percent = (ltp - high_prev_day)*100.0/high_prev_day
                all_gapped_up.append({'Instrument':instrument_token,'Gap_Up_Percent':gap_up_percent,'Open Price':ltp})
    open_price_checked.sort()
    print("Open price checked for:",len(open_price_checked)," stocks")
    if open_price_checked == All_NFO_EQ:
        kws.close()
        current_time = datetime.now()
        print("The current time is:",current_time)
        start_gap_up()
def on_connect(kws,response):
    initialise()
    kws.subscribe(All_NFO_EQ)
    kws.set_mode(kws.MODE_FULL,All_NFO_EQ)
print(kws)
print("Connecting to websocket")
kws.on_connect = on_connect
kws.on_ticks = on_ticks
kws.connect()
#start_gap_up()
