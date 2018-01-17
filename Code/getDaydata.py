import pandas as pd
import numpy as np
import metaData
import kiteconnect
import time
from datetime import datetime

t = datetime.now()
kite = kiteconnect.KiteConnect(metaData.getApiKey(),metaData.getAccessToken())
All_NFO_EQ = metaData.getNSEFOStocks(kite,False)
tradingsymbols = {}
full_list = kite.instruments(exchange = kite.EXCHANGE_NSE)
for instrument in All_NFO_EQ:
    tradingsymbols[instrument] = metaData.getTradingsymbol(instrument,full_list)
for year in range(2013,2014):
    print("Getting the data for ",year)
    file_name = str(year) + '_day.csv'
    dates = [['-01-01','-05-31'],['-06-01','-10-31'],['-11-01','-12-31']]
    ans = []
    for instrument_token in All_NFO_EQ:
        for item in dates:
            from_date = str(year) + item[0]
            to_date = str(year) + item[1]
            print("Getting the data for ",instrument_token,"from",from_date,"to",to_date)
            while True:
                try:
                    temp_data = kite.historical_data(instrument_token,from_date,to_date,'day')
                    break
                except Exception as e:
                    print(e)
                    print("Retrying the data for ",instrument_token,"from",from_date,"to",to_date)
            print("Got the data for ",instrument_token,"from",from_date,"to",to_date)
            for a in temp_data:
                a['instrument_token'] = instrument_token
                a['tradingsymbol'] = tradingsymbols[instrument_token]
                ans.append(a)
    print("Got the data for ",year)
    print("Number of rows:",len(ans))
    df = pd.DataFrame(ans)
    df.to_csv(file_name,sep = ',')
t = datetime.now() - t
print("Total time taken:",t)
