import kiteconnect
import metaData
import corefunctions as core
from datetime import datetime
import numpy as np
import pandas as pd
import pickle
import autologin_kiteconnect
import time

current_time = datetime.now()
print("Program started at:",current_time)
api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()
if access_token == None:
    autologin_kiteconnect.create_access_token()
    access_token = metaData.getAccessToken()
kite = kiteconnect.KiteConnect(api_key,access_token)
All_NFO_EQ = metaData.getNSEFOStocks(kite,False)
end_time = datetime(current_time.year,current_time.month,current_time.day,9,30)
ohlc_snapshot_file = open('ohlc_snapshot_all.pickle','wb')
ohlc_snapshot = None
while True:
    try:
        ohlc_snapshot = kite.ohlc(All_NFO_EQ)
    except:
        None
    t = datetime.now()
    pickle.dump(t,ohlc_snapshot_file)
    pickle.dump(ohlc_snapshot,ohlc_snapshot_file)
    if t > end_time:
        break
    time.sleep(1)
ohlc_snapshot_file.close()
