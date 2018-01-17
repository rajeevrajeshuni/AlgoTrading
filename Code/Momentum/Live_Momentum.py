#Need to add different kind of import as they are not in same folder
import metaData as meta
import corefunctions as core

from kiteconnect import KiteConnect,KiteTicker
import pandas as pd
import numpy as np
import logging
from datetime import datetime,timedelta

access_token = metaData.getAccessToken()
api_key = metaData.getApiKey()
kite = KiteConnect(api_key,access_token)
kws = KiteTicker(api_key,access_token)
All_NFO_EQ = meta.getNSEFOStocks(kite)
current_time = datetime.now()

#Assuming day2 as prev trading day and day1 as trading day before that and day0 is trading day before that
#Searches for all the stocks which satisfy the condition day0_close < day1_close < day2_close and increase_percent_of_close_price_from_0_to_1 < increase_percent_of_close_price_from_1_to_2
#Returns as shortlist of stocks in a dictionary with instrument_token as key and close prices on day0,day1,day2 in a list as value for the key.
def getShortlist(kite):
    day2 = core.prev_trading_day(1)
    day2_str = day2.strftime("%Y-%m-%d")
    day1 = core.prev_trading_day(2)
    day1_str = day1.strftime("%Y-%m-%d")
    day0 = core.prev_trading_day(3)
    day0_str = day0.strftime("%Y-%m-%d")
    shortlist = {}
    for eq in All_NFO_EQ:
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

def on_ticks(kws,ticks):


def on_connect(kws,response):
    eq_list = getShortlist(kite)
    kite.subscribe(eq_list)
    kite.set_mode(kite.MODE_FULL,eq_list)
kws.on_ticks = on_ticks
kws.on_connect = on_connect
