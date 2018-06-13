from datetime import datetime,timedelta
import kiteconnect
import metaData
import pickle

#This function gives the high value for previous day for a list of instruments given.
#While calculating the previous day if immediate previous day is holiday then we go back another day. So if today is Monday, function will give high values for Friday(assuming it is a trading day)
def prev_day_high(instruments,kite):
    pickle_file = open('Prev_day_high.pickle','wb')
    prev_day_high = {}
    t = datetime.now()
    prev_trading_day = t - timedelta(days=1)
    while not is_trading_day(prev_trading_day):
        prev_trading_day-=timedelta(days=1)
    prev_trading_day = prev_trading_day.strftime("%Y-%m-%d")
    index = 0
    while True:
        ist = instruments[index]
        try:
            prev_day_candle = kite.historical_data(ist,prev_trading_day,prev_trading_day,'day')[0]
        except Exception as e:
            print(index,ist,e)
            continue
        prev_day_high[ist] = prev_day_candle['high']
        index+=1
        if index == len(instruments):
            break
    t = datetime.now() - t
    print("Time taken to extract previous day high values:",t)
    pickle.dump(datetime.now(),pickle_file)
    pickle.dump(prev_day_high,pickle_file)
    pickle_file.close()
    return prev_day_high

#This function returns true if the input datetime object is a day on which trading happens.
#Added days for 2014,2015,2016,2017,2018
def is_trading_day(date):
    #print(date,type(date))
    #print(date.year,type(date.year))

    #Returns None if the date is not in year 2018
    if date.year not in [2014,2015,2016,2017,2018]:
        return None
    date_of_week = date.weekday()
    #Checking if the day is saturday or sunday
    if date_of_week == 5 or date_of_week == 6:
        return False

    trading_holidays = metaData.getTradingHolidays()

    #date is a datetime object
    day = date.day
    month = date.month
    str_date = ""
    if month<10:
        str_date+='0'+str(month)+'/'
    else:
        str_date+=str(month)+'/'
    if day<10:
        str_date+='0'+str(day)
    else:
        str_date+=str(day)
    str_date = str_date + '/' + str(date.year)
    #print(str_date)
    if str_date in trading_holidays:
        return False
    return True

#This function returns true if the input datetime object is a day on which trading happens.
def is_trading_day_2018(date):
    #print(date,type(date))
    #print(date.year,type(date.year))

    #Returns None if the date is not in year 2018
    if date.year != 2018:
        return None
    date_of_week = date.weekday()
    #Checking if the day is saturday or sunday
    if date_of_week == 5 or date_of_week == 6:
        return False

    trading_holidays_2018 = metaData.getTradingHolidays2018()

    #date is a datetime object
    day = date.day
    month = date.month
    str_date = ""
    if month<10:
        str_date+='0'+str(month)+'/'
    else:
        str_date+=str(month)+'/'
    if day<10:
        str_date+='0'+str(day)
    else:
        str_date+=str(day)
    #print(str_date)
    if str_date in trading_holidays_2018:
        return False
    return True

#The input will be the number of trading days before the current trading day. If you need immediate previous trading day pass 1. Pass 2 for the days before that.
#Returns a datetime object with only date,month and year.
def prev_trading_day(prior_days):
    ans = datetime.now()
    i = 0
    while i<prior_days:
        ans = ans - timedelta(days=1)
        if is_trading_day(ans):
            i+=1
    return datetime(ans.year,ans.month,ans.day)

def buy_impact_cost(tick,instrument_token,quantity):
    cost_buy = 0
    for i in tick:
        if i['instrument_token'] == instrument_token:
            sell_orders = i['depth']['sell']
            quantity_required = quantity
            for offer in sell_orders:
                if quantity_required >= offer['quantity']:
                    cost_buy+=offer['quantity']*offer['price']
                    quantity_required-=offer['quantity']
                else:
                    cost_buy+=quantity_required*offer['price']
                    quantity_required = 0
                    break
            if quantity_required == 0:
                cost_buy = (cost_buy*1.0)/quantity
            else:
                print("Not enough orders available to fulfill the required quantity.")
                cost_buy = -1
    return cost_buy
def sell_impact_cost(tick,instrument_token,quantity):
    cost_sell = 0
    tick_instrument = {}
    for i in tick:
        if i['instrument_token'] == instrument_token:
            buy_orders = i['depth']['buy']
            quantity_required = quantity
            for offer in buy_orders:
                if quantity_required >= offer['quantity']:
                    cost_sell+=offer['quantity']*offer['price']
                    quantity_required-=offer['quantity']
                else:
                    cost_sell+=quantity_required*offer['price']
                    quantity_required = 0
                    break
            if quantity_required == 0:
                cost_sell = (cost_sell*1.0)/quantity
            else:
                print("Not enough orders available to fulfill the required quantity.")
                cost_sell = -1
    return cost_sell
def print_list(l):
    for i in range(len(l)):
        print(i+1,l[i])
def remove_exceptions(l,kite):
    exceptions_tradingsymbols = ['SHREECEM']
    full_instruments_list = kite.instruments(exchange = kite.EXCHANGE_NSE)
    exceptions_tokens = []
    for symbol in exceptions_tradingsymbols:
        exceptions_tokens.append(metaData.getInstrumentToken(symbol,full_instruments_list))
    ans = [x for x in l if x not in exceptions_tokens]
    return ans
