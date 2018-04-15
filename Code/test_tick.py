import logging
import kiteconnect
import metaData
import pandas as pd
import corefunctions as core
from datetime import datetime
import pickle

current_time = datetime.now()
api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()
if access_token == None:
    autologin_kiteconnect.create_access_token()
    access_token = metaData.getAccessToken()
kws = kiteconnect.KiteTicker(api_key,access_token)
kite = kiteconnect.KiteConnect(api_key,access_token)
f = open('FULL_ticks_all.pickle','wb')
end_time = datetime(current_time.year,current_time.month,current_time.day,9,30)
def on_ticks(kws,ticks):
    #print("Ticks: "+" "+str(metaData.iterations))
    #for i in range(len(ticks)):
    #    tick = ticks[i]
    #    text = str(datetime.now())+" "+str(tick['instrument_token'])+" LTP: "+str(tick['last_price'])
    #    print(text)
    pickle.dump(datetime.now(),f)
    pickle.dump(ticks,f)
    if datetime.now() > end_time:
        kws.close()
        f.close()

def on_connect(kws,response):
    instruments = metaData.getNSEFOStocks(kite)
    kws.subscribe(instruments)
    kws.set_mode(kws.MODE_FULL,instruments)

kws.on_connect = on_connect
kws.on_ticks = on_ticks
kws.connect()
