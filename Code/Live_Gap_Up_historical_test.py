import kiteconnect
import metaData
import corefunctions as core
from datetime import datetime
import numpy as np
import pandas as pd
import pickle
import keys
import logging
#import autologin_kiteconnect

log_file_name = datetime.now().strftime("%Y-%m-%d")+'_test.log'
root_path = keys.getRootPath()
full_path = root_path+'AlgoTrading/Code/Gap_Up_Daily_Logs/'+log_file_name
#logging.basicConfig(filename=full_path,filemode='w',level=logging.DEBUG)

current_time = datetime.now()
logging.info("Program started at: "+str(current_time))
api_key = keys.getApiKey()
access_token = metaData.getAccessToken()
kws = kiteconnect.KiteTicker(api_key,access_token)
kite = kiteconnect.KiteConnect(api_key,access_token)
All_NFO_EQ = metaData.getNSEFOStocks(kite,False)
All_NFO_EQ.sort()
All_NFO_EQ = metaData.removeOutliers(All_NFO_EQ)
list_NSE_instruments = kite.instruments(exchange = kite.EXCHANGE_NSE)

logging.info("Getting the previous day high values")
try:
    pickle_file = open('Prev_day_high.pickle','rb')
    pickle_file_date = pickle.load(pickle_file)
    prev_day_high = pickle.load(pickle_file)
    pickle_file.close()
except:
    logging.info("Getting the values again today")
    core.prev_day_high(All_NFO_EQ,kite)
    pickle_file = open('Prev_day_high.pickle','rb')
    pickle_file_date = pickle.load(pickle_file)
    prev_day_high = pickle.load(pickle_file)

if pickle_file_date.date() == datetime.today().date():
    logging.info("Got previous day high values for: "+str(pickle_file_date.date()))
else:
    logging.info("Got the previous day high values for: "+str(pickle_file_date.date()))
    logging.info("Getting the values again today")
    core.prev_day_high(All_NFO_EQ,kite)
    pickle_file = open('Prev_day_high.pickle','rb')
    pickle_file_date = pickle.load(pickle_file)
    prev_day_high = pickle.load(pickle_file)

all_gapped_up = []
today = str(datetime.now().date())
max_percent = 2
num_top_stocks = 8
#Write code for gap up strategy here.
def start_gap_up():
    #all_gapped_up = [{'Instrument':738561,'Gap_Up_Percent':1.9,'Open Price':25},{'Instrument':424961,'Gap_Up_Percent':2,'Open Price':200},{'Instrument':160001,'Gap_Up_Percent':1.3,'Open Price':2500}]
    logging.info("Staring gap up strategy")
    logging.info("Number of gapped up stocks: "+str(len(all_gapped_up)))
    gapup_df = pd.DataFrame(all_gapped_up)
    gapup_df = gapup_df.sort_values('Gap_Up_Percent',ascending = False)
    gapup_df = gapup_df[gapup_df['Gap_Up_Percent']<=max_percent]
    logging.info("All gapped up stocks:")
    logging.info(gapup_df.to_string())
    gapup_df = gapup_df.head(num_top_stocks)
    stocks = gapup_df['Instrument'].values
    stocks_prices = gapup_df['Open Price'].values
    #logging.info("The top four stocks less than two percent are:")
    #logging.info(stocks)
    #Placing order for stocks
    logging.info("Preparing for placing orders at: "+str(datetime.now()))
    for index in range(gapup_df.shape[0]):
        open_price = stocks_prices[index]
        quantity = 1
        #quantity = int(capital/open_price)
        tradingsymbol = metaData.getTradingsymbol(stocks[index],list_NSE_instruments)
        logging.info("Placing MIS order for: "+str(tradingsymbol)+" at: "+str(datetime.now()))
        logging.info(str(tradingsymbol)+" Stock price "+str(stocks_prices[index]))
        #kite.place_order('REGULAR',kite.EXCHANGE_NSE,tradingsymbol,'SELL',quantity,'MIS','LIMIT',1)
    current_time = datetime.now()
    logging.info("Strategy execution completed at: "+str(current_time))

i = 0
#logging.info("-----")
while i < len(All_NFO_EQ):
    instrument = All_NFO_EQ[i]
    while True:
        #logging.info(i)
        try:
            today_open_price = kite.historical_data(instrument,today,today,'day')[0]['open']
            #logging.info(today_open_price)
            break
        except Exception as e:
            logging.info(str(i)+' '+str(e))
            continue
    logging.info(str(i)+' '+str(instrument))
    i+=1
    if today_open_price > prev_day_high[instrument]:
        high_prev_day = prev_day_high[instrument]
        gap_up_percent = (today_open_price - high_prev_day)*100.0/high_prev_day
        tradingsymbol = metaData.getTradingsymbol(instrument,list_NSE_instruments)
        all_gapped_up.append({'Instrument':instrument,'Gap_Up_Percent':gap_up_percent,'Open Price':today_open_price,'Trading Symbol':tradingsymbol})

start_gap_up()
#gapup_df = pd.DataFrame(all_gapped_up)
#gapup_df = gapup_df.sort_values('Gap_Up_Percent',ascending = False)
#logging.info(gapup_df)
