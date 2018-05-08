import kiteconnect
from datetime import datetime
import pickle
import keys
import autologin_kiteconnect

iterations = 0

trading_holidays_2018 = ['01/26','02/13','03/02','03/29','03/30','05/01','08/15','08/22','09/13','09/20','10/02','10/18','11/07','11/08','11/23','12/25']

def getApiKey():
    return keys.getApiKey()

def getApiSecret():
    return keys.getAccessToken()

def getAccessToken():
    try:
        access_token_file = open('Secure/access_token.pickle','rb')
        pickle_file_date = pickle.load(access_token_file)
        #print(pickle_file_date,"metaData getAccessToken")
        #print(pickle_file_date)
        access_token = pickle.load(access_token_file)
        #print(access_token)
    except:
        autologin_kiteconnect.create_access_token()
        access_token_file = open('Secure/access_token.pickle','rb')
        pickle_file_date = pickle.load(access_token_file)
        access_token = pickle.load(access_token_file)
    if not (pickle_file_date.date() == datetime.today().date() and (pickle_file_date.hour*60 + pickle_file_date.minute) > 510):
        autologin_kiteconnect.create_access_token()
        access_token_file = open('Secure/access_token.pickle','rb')
        pickle_file_date = pickle.load(access_token_file)
        access_token = pickle.load(access_token_file)
    return access_token

def getUserID():
    return keys.getUserID()

def getTradingHolidays2018():
    return trading_holidays_2018


def getTradingsymbol(instrument,list_instruments):
    ans = None
    for item in list_instruments:
        if item['instrument_token'] == instrument:
            ans = item['tradingsymbol']
            break
    return ans
#get Trading symbol for a list of instruments
def getTradingsymbol_NSE(instruments,kite):
    list_instruments = kite.instruments(exchange = kite.EXCHANGE_NSE)
    ans = []
    for item in instruments:
        ans.append(getTradingsymbol(item,list_instruments))
    return ans

#This function will return the instrument token for the given tradingsymbol
def getInstrumentToken(tradingsymbol,list_instruments):
    ans = None
    for instrument in list_instruments:
        if instrument['tradingsymbol'] == tradingsymbol:
            ans = instrument['instrument_token']
            break
    return ans

#Return the list of Nifty 50. Each value in the format "tradename:instrument_token"
def getNifty50(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty 50.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Next 50. Each value in the format "tradename:instrument_token"
def getNiftyNext50(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Next 50.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Auto. Each value in the format "tradename:instrument_token"
def getNiftyAuto(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Auto.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of FO stocks in NSE. Each value in the format "tradename:instrument_token"
def getNSEFOStocks(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/NSE FO Stocks.csv',kite.EXCHANGE_NSE,kite,1,need_trading_symbol)
    #return remove_exceptions(l)
#Return a dictionary of FO stocks in NSE with instrument token as key and tradingsymbol as value.
def getNSEFOStocks_instrument_tradingsymbol(kite):
    return getInstrumentToken_TradingSymbol_csv('/Users/Rajeev/AlgoTrading/Files/NSE FO Stocks.csv',kite.EXCHANGE_NSE,kite,1)

#Return the list of Nifty Bank. Each value in the format "tradename:instrument_token"
def getNiftyBank(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Bank.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Energy. Each value in the format "tradename:instrument_token"
def getNiftyEnergy(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Energy.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Financial Services. Each value in the format "tradename:instrument_token"
def getNiftyFinancialServices(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/FilesNifty Financial Services.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty IT. Each value in the format "tradename:instrument_token"
def getNiftyIT(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty IT.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty FMCG. Each value in the format "tradename:instrument_token"
def getNiftyFMCG(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty FMCG.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Media. Each value in the format "tradename:instrument_token"
def getNiftyMedia(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Media.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Metal. Each value in the format "tradename:instrument_token"
def getNiftyMetal(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Metal.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Midcap 50. Each value in the format "tradename:instrument_token"
def getNiftyMidcap50(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Midcap 50.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty pharma. Each value in the format "tradename:instrument_token"
def getNiftyPharma(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Pharma.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Private Bank. Each value in the format "tradename:instrument_token"
def getNiftyPrivateBank(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Private Bank.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty PSU Bank. Each value in the format "tradename:instrument_token"
def getNiftyPSUBank(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty PSU Bank.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Realty. Each value in the format "tradename:instrument_token"
def getNiftyRealty(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv('/Users/Rajeev/AlgoTrading/Files/Nifty Realty.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol=False)

def getInstrumentTokens_csv(path,exchange,kite,ignore_lines=2,need_trading_symbol=False):
    f = open(path,'r')
    #ignoring the no. of lines passed
    for i in range(ignore_lines):
        f.readline()
    ans_list = []
    full_instruments_list = kite.instruments(exchange = exchange)
    for line in f.readlines():
        line = line.split(",")
        #print(line)
        tradingsymbol = line[0][1:-1]
        if need_trading_symbol:
            item = tradingsymbol+":"+str(getInstrumentToken(tradingsymbol,full_instruments_list))
        else:
            item = getInstrumentToken(tradingsymbol,full_instruments_list)
        ans_list.append(item)
    return ans_list

def getInstrumentToken_TradingSymbol_csv(path,exchange,kite,ignore_lines=2):
    f = open(path,'r')
    #ignoring the no. of lines passed
    for i in range(ignore_lines):
        f.readline()
    ans = {}
    full_instruments_list = kite.instruments(exchange = exchange)
    for line in f.readlines():
        line = line.split(",")
        tradingsymbol = line[0][1:-1]
        instrument_token = getInstrumentToken(tradingsymbol,full_instruments_list)
        ans[instrument_token] = tradingsymbol
    return ans
