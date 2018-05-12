!!!!Need to add different kind of import as they are not in same folder!!!
import metaData as meta
import corefunctions as core

from kiteconnect import KiteConnect
import pandas as pd
import numpy as np
import logging
from datetime import datetime,timedelta

!!! Still need to do logging!!!

#Assuming day2 as prev trading day and day1 as trading day before that and day0 is trading day before that
#Searches for all the stocks in the instrument list given which satisfy the condition day0_close < day1_close < day2_close and increase_percent_of_close_price_from_0_to_1 < increase_percent_of_close_price_from_1_to_2
#Returns as shortlist of stocks in a dictionary with instrument_token as key and close prices on day0,day1,day2 in a list as value for the key.
def getShortlist(kite,instrument_list):
    day2 = core.prev_trading_day(1)
    day2_str = day2.strftime("%Y-%m-%d")
    day1 = core.prev_trading_day(2)
    day1_str = day1.strftime("%Y-%m-%d")
    day0 = core.prev_trading_day(3)
    day0_str = day0.strftime("%Y-%m-%d")
    shortlist = {}
    for eq in instrument_list:
        day2_close = kite.historical_data(eq,day2_str,day2_str,'day')[0]['close']
        day1_close = kite.historical_data(eq,day1_str,day1_str,'day')[0]['close']
        day0_close = kite.historical_data(eq,day0_str,day0_str,'day')[0]['close']
        increase_percent_1 = (day1_close - day0_close)*100/day0_close
        increase_percent_2 = (day2_close - day1_close)*100/day1_close
        #Condition 1
        if day0_close < day1_close and day1_close < day2_close:
            #Condition 2
            if increase_percent_1 < increase_percent_2:
                shortlist[eq] = [day0_close,day1_close,day2_close]
    return shortlist
if __name__ == "__main__":
    start_hr = 15
    start_min = 25

    total_capital = 600000
    num_top_stocks = 4
    access_token = metaData.getAccessToken()
    api_key = metaData.getApiKey()
    kite = KiteConnect(api_key,access_token)

    All_NFO_EQ = meta.getNSEFOStocks(kite)
    shortlist = getShortlist(kite,All_NFO_EQ)
    logging_file_name = datetime.now().strftime("%Y-%m-%d") + ".txt"

    while True:
        current_time = datetime.now()
        if not(current_time.hour>=start_hr and current_time.minute>=start_min):
            continue
        for instrument in shortlist:
            prev_day_close_prices = shortlist[instrument]
            day0_close = prev_day_close_prices[0]
            day1_close = prev_day_close_prices[1]
            day2_close = prev_day_close_prices[2]
            increase_percent_1 = (day1_close - day0_close)*100/day0_close
            increase_percent_2 = (day2_close - day1_close)*100/day1_close
            day3_str = current_time.strftime("%Y-%m-%d")
            #Need to create a datetime object to get the historical data for close price
            day3_close = kite.historical_data(instrument,!!!!,!!!!,'5min')[0]['close']
            increase_percent_3 = (day3_close - day2_close)*100/day2_close
            #Condition 1
            if day2_close < day3_close:
                #Condition 2
                if increase_percent_1 < increase_percent_2 and increase_percent_2 < increase_percent_3:
                    tradingsymbol = metaData.getTradingsymbol(instrument,kite.instruments(exchange = kite.EXCHANGE_NSE))
                    capital_each_stock = int((total_capital/num_top_stocks)+0.5)
                    quantity = int((capital_each_stock/day3_close)+0.5)
                    kite.place_order('REGULAR',kite.EXCHANGE_NSE,tradingsymbol,'BUY',quantity,'CNC','LIMIT',0.05)
