import kiteconnect
import metaData
import corefunctions as core
import pandas as pd
import time
from datetime import datetime
api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()

kite = kiteconnect.KiteConnect(api_key,access_token)
All_NFO_EQ = metaData.getNSEFOStocks(kite)
prev_day_high = core.prev_day_high(All_NFO_EQ,kite)
all_gapped_up = []

t = datetime.now()
index = 0
while True:
    ist = All_NFO_EQ[index]
    try:
        candle = kite.historical_data(ist,'2018-04-06','2018-04-06','day')[0]
    except Exception as e:
        continue
    print("Yesterday high:",prev_day_high[ist],"Today open:",candle['open'],"Instrument:",ist,"Trading Symbol:",metaData.getTradingsymbol_NFO(ist,kite))
    if candle['open'] > prev_day_high[ist]:
        gap_up_percent = (candle['open']-prev_day_high[ist])*1.0/prev_day_high[ist]
        all_gapped_up.append({'instrument token':ist,'gap_up_percent':gap_up_percent,'Today open':candle['open'],'Yesterday high':prev_day_high[ist]})
    index+=1
    if index == len(All_NFO_EQ):
        break
t = datetime.now() - t
print(len(all_gapped_up))
df = pd.DataFrame(all_gapped_up)
print(df)
print("Total time taken:",t)
