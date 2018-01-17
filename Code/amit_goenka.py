import kiteconnect
import metaData
from datetime import datetime
api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()

kite = kiteconnect.KiteConnect(api_key,access_token)
ticker = kiteconnect.KiteTicker(api_key,access_token)

suggested_prices_temp = {'PAISALO':302.5,'BHARATFIN':1096.85,'TITAN':942.3}
max_increase_percent = 2
capital = 90000

instruments_tradingsymbol = {}
suggested_prices = {}
ltp = {}
start_hr = 9
start_min = 15

def initialize():
    list_instruments_NSE = kite.instruments(exchange = kite.EXCHANGE_NSE)
    instruments = []
    for t in suggested_prices_temp.keys():
        instrument = metaData.getInstrumentToken(t,list_instruments_NSE)
        instruments.append(instrument)
        instruments_tradingsymbol[instrument] = t
        suggested_prices[instrument] = suggested_prices_temp[t]
    return instruments

def buy_stocks(ltp):
    print(ltp)
    total_increase_percent = 0
    for instrument in suggested_prices.keys():
        total_increase_percent+=((ltp[instrument]-suggested_prices[instrument])*100.0)/suggested_prices[instrument]
    total_increase_percent = total_increase_percent/len(suggested_prices)
    if total_increase_percent <= max_increase_percent:
        for instrument in suggested_prices.keys():
            tradingsymbol = instruments_tradingsymbol[instrument]
            cap_stock = capital/len(suggested_prices)
            quantity = int(cap_stock/ltp[instrument])
            #print(cap_stock,quantity)
            kite.place_order('REGULAR',kite.EXCHANGE_NSE,tradingsymbol,'BUY',quantity,'CNC','LIMIT',ltp[instrument])

def on_ticks(ticker,ticks):
    for tick in ticks:
        timestamp = tick['timestamp']
        if not (timestamp.date() == datetime.today().date() and timestamp.hour>=start_hr and timestamp.minute>=start_min):
            continue
        instrument_token = tick['instrument_token']
        if instrument_token not in ltp.keys():
            ltp[instrument_token] = tick['last_price']
        ticker.unsubscribe([instrument_token])
        if len(ltp) == len(suggested_prices):
            buy_stocks(ltp)
            ticker.close()
    print("Open price checked for:",len(ltp)," stocks")
def on_connect(ticker,response):
    instruments = initialize()
    #print(instruments,suggested_prices)
    ticker.subscribe(instruments)
    ticker.set_mode(ticker.MODE_FULL,instruments)

#print(initialize())

ticker.on_connect = on_connect
ticker.on_ticks = on_ticks

ticker.connect()

"""ltp = {6519809:303.5,4995329:1106.85,897537:932.3}
instruments_tradingsymbol = {6519809:'PAISALO',4995329:'BHARATFIN',897537:'TITAN'}
initialize()
buy_stocks(ltp)"""
