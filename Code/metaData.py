from datetime import datetime
import pickle
import keys
import autologin_kiteconnect

iterations = 0

trading_holidays_2018 = ['01/26','02/13','03/02','03/29','03/30','05/01','08/15','08/22','09/13','09/20','10/02','10/18','11/07','11/08','11/23','12/25']
#Added for 2015,2016,2017,2018
trading_holidays = ['27/02/2014','17/03/2014','08/04/2014','14/04/2014','18/04/2014','24/04/2014','01/05/2014','29/07/2014','15/08/2014','29/08/2014','02/10/2014','03/10/2014','06/10/2014','15/10/2014','24/10/2014','04/11/2014','06/11/2014','25/12/2014','26/01/2015','17/02/2015','06/03/2015','02/04/2015','03/04/2015','14/04/2015','01/05/2015','17/09/2015','25/09/2015','02/10/2015','22/10/2015','12/11/2015','25/11/2015','25/12/2015','26/01/2016','07/03/2016','24/03/2016','25/03/2016','14/04/2016','15/04/2016','19/04/2016','06/07/2016','15/08/2016','05/09/2016','13/09/2016','11/10/2016','12/10/2016','31/10/2016','14/11/2016','26/01/2017','24/02/2017','13/03/2017','04/04/2017','14/04/2017','01/05/2017','26/06/2017','15/08/2017','25/08/2017','02/10/2017','20/10/2017','25/12/2017','01/26/2018','02/13/2018','03/02/2018','03/29/2018','03/30/2018','05/01/2018','08/15/2018','08/22/2018','09/13/2018','09/20/2018','10/02/2018','10/18/2018','11/07/2018','11/08/2018','11/23/2018','12/25/2018']
root_path = keys.getRootPath()

def getApiKey():
    return keys.getApiKey()


def getApiSecret():
    return keys.getAccessToken()

def getAccessToken():
    try:
        access_token_file = open(root_path+'AlgoTrading/Code/Secure/access_token.pickle','rb')
        pickle_file_date = pickle.load(access_token_file)
        #print(pickle_file_date,"metaData getAccessToken")
        #print(pickle_file_date)
        access_token = pickle.load(access_token_file)
        #print(access_token)
    except Exception as e:
        autologin_kiteconnect.create_access_token()
        access_token_file = open(root_path+'AlgoTrading/Code/Secure/access_token.pickle','rb')
        pickle_file_date = pickle.load(access_token_file)
        access_token = pickle.load(access_token_file)
    if not (pickle_file_date.date() == datetime.today().date() and (pickle_file_date.hour*60 + pickle_file_date.minute) > 510):
        autologin_kiteconnect.create_access_token()
        access_token_file = open(root_path+'AlgoTrading/Code/Secure/access_token.pickle','rb')
        pickle_file_date = pickle.load(access_token_file)
        access_token = pickle.load(access_token_file)
    return access_token

def getUserID():
    return keys.getUserID()

def getTradingHolidays2018():
    return trading_holidays_2018

def getTradingHolidays():
    return trading_holidays

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
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty 50.csv',kite.EXCHANGE_NSE,kite,1,need_trading_symbol)

#Return the list of Nifty Next 50. Each value in the format "tradename:instrument_token"
def getNiftyNext50(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Next 50.csv',kite.EXCHANGE_NSE,kite,1,need_trading_symbol)

#Return the list of Nifty Auto. Each value in the format "tradename:instrument_token"
def getNiftyAuto(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Auto.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of FO stocks in NSE. Each value in the format "tradename:instrument_token"
def getNSEFOStocks(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/NSE FO Stocks.csv',kite.EXCHANGE_NSE,kite,1,need_trading_symbol)
    #return remove_exceptions(l)
#Return a dictionary of FO stocks in NSE with instrument token as key and tradingsymbol as value.
def getNSEFOStocks_instrument_tradingsymbol(kite):
    return getInstrumentToken_TradingSymbol_csv(root_path+'AlgoTrading/Files/NSE FO Stocks.csv',kite.EXCHANGE_NSE,kite,1)

#Return the list of Nifty Bank. Each value in the format "tradename:instrument_token"
def getNiftyBank(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Bank.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Energy. Each value in the format "tradename:instrument_token"
def getNiftyEnergy(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Energy.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Financial Services. Each value in the format "tradename:instrument_token"
def getNiftyFinancialServices(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/FilesNifty Financial Services.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty IT. Each value in the format "tradename:instrument_token"
def getNiftyIT(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty IT.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty FMCG. Each value in the format "tradename:instrument_token"
def getNiftyFMCG(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty FMCG.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Media. Each value in the format "tradename:instrument_token"
def getNiftyMedia(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Media.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Metal. Each value in the format "tradename:instrument_token"
def getNiftyMetal(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Metal.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Midcap 50. Each value in the format "tradename:instrument_token"
def getNiftyMidcap50(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Midcap 50.csv',kite.EXCHANGE_NSE,kite,1,need_trading_symbol)

#Return the list of Nifty pharma. Each value in the format "tradename:instrument_token"
def getNiftyPharma(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Pharma.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Private Bank. Each value in the format "tradename:instrument_token"
def getNiftyPrivateBank(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Private Bank.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty PSU Bank. Each value in the format "tradename:instrument_token"
def getNiftyPSUBank(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty PSU Bank.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol)

#Return the list of Nifty Realty. Each value in the format "tradename:instrument_token"
def getNiftyRealty(kite,need_trading_symbol=False):
    return getInstrumentTokens_csv(root_path+'AlgoTrading/Files/Nifty Realty.csv',kite.EXCHANGE_NSE,kite,need_trading_symbol=False)

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

def removeOutliers(instruments):
    final_instruments = []
    outliers = {
        2933761:'JPASSOCIAT',
        4369665:'UJJIVAN',
        884737:'TATAMOTORS',
        2170625:'TVSMOTOR',
        141569:'RELINFRA',
        1723649:'JINDALSTEL',
        2661633:'JISLJALEQS',
        2674433:'MCDOWELL-N',
        225537:'DRREDDY',
        345089:'HEROMOTOCO',
        3076609:'SUZLON',
        4708097:'RBLBANK',
        3637249:'TV18BRDCST',
        3903745:'CAPF',
        4454401:'NHPC',
        7670273:'JUSTDIAL',
        7712001:'IBULHSGFIN',
        2939649:'LT',
        2953217:'TCS',
        4159745:'INFIBEAM',
        593665:'NCC',
        737793:'RELCAPITAL',
        245249:'ESCORTS',
        3861249:'ADANIPORTS',
        424961:'ITC',
        4465665:'RNAVAL',
        134657:'BPCL',
        356865:'HINDUNILVR',
        4268801:'BAJAJFINSV'
    }
    for i in instruments:
        if i not in outliers:
            final_instruments.append(i)
    return final_instruments
