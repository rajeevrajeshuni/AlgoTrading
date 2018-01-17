import kiteconnect
import metaData
#import Gap_Up
import Gap_Up_backtest_New
import corefunctions as core

api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()
kite = kiteconnect.KiteConnect(api_key,access_token)

#AllNSEFOStocks = metaData.getNSEFOStocks(kite,False)
#print(core.prev_day_high(AllNSEFOStocks,kite))

Gap_Up_backtest_New.applygapup(kite)



def start_gap_up(kite):
    AllNSEFOStocks = metaData.getNSEFOStocks(kite,True)
    dates = [{'from_date':'2016-01-01','to_date':'2016-05-31'}]
    for date in dates:
        #print(date['from_date'],date['to_date'])
        Gap_Up.applygapup(AllNSEFOStocks,date['from_date'],date['to_date'],kite)

#Gap up strategy
#start_gap_up(kite)
