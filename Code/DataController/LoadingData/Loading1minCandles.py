import sys
sys.path.append('../../')
import mysql.connector
import keys
import kiteconnect
import metaData
from datetime import datetime

cnx = mysql.connector.connect(user=keys.getMysqlUser(),password=keys.getMysqlPassword(),database='candles')
cursor = cnx.cursor()
print('Connected to mysqlserver')

minute_table = "CREATE TABLE IF NOT EXISTS minute (cdate datetime NOT NULL, tradingsymbol_no int(7) NOT NULL,open decimal(7,2) NOT NULL,high decimal(7,2) NOT NULL,low decimal(7,2) NOT NULL,close decimal(7,2) NOT NULL,volume int(12) NOT NULL,PRIMARY KEY (cdate,tradingsymbol_no), KEY cdate (cdate), KEY tradingsymbol_no (tradingsymbol_no), CONSTRAINT tradingsymbol_no_ibfk3 FOREIGN KEY (tradingsymbol_no) REFERENCES tradingsymbols (tradingsymbol_no) ON DELETE CASCADE )"
cursor.execute(minute_table)

tradingsymbol_table = "CREATE TABLE IF NOT EXISTS tradingsymbols (tradingsymbol_no int(7) NOT NULL AUTO_INCREMENT, tradingsymbol varchar(25) NOT NULL,PRIMARY KEY (tradingsymbol_no), UNIQUE KEY tradingsymbol (tradingsymbol))"
cursor.execute(tradingsymbol_table)

print('First step')

access_token = metaData.getAccessToken()
api_key = keys.getApiKey()
kite = kiteconnect.KiteConnect(api_key,access_token)
full_instruments_list = kite.instruments(exchange = kite.EXCHANGE_NSE)
#print(full_instruments_list)

dates = [['2018-01-01','2018-01-30'],['2018-02-01','2018-02-28'],['2018-03-01','2018-03-30'],['2018-03-31','2018-03-31'],['2018-04-01','2018-04-30'],['2018-05-01','2018-05-30'],['2018-05-31','2018-05-31'],['2018-06-01','2018-06-30']]

#dates = [['2015-02-01','2015-02-28'],['2015-03-01','2015-03-30'],['2015-03-31','2015-03-31'],['2015-04-01','2015-04-30'],['2015-05-01','2015-05-30'],['2015-05-31','2015-05-31'],['2015-06-01','2015-06-30'],['2015-07-01','2015-07-30'],['2015-07-31','2015-07-31'],['2015-08-01','2015-08-30'],['2015-08-31','2015-08-31'],['2015-09-01','2015-09-30'],['2015-10-01','2015-10-30'],['2015-10-31','2015-10-31'],['2015-11-01','2015-11-30'],['2015-12-01','2015-12-30'],['2015-12-31','2015-12-31']]

#dates = [['2016-01-01','2016-01-30'],['2016-01-31','2016-01-31'],['2016-02-01','2016-02-29'],['2016-03-01','2016-03-30'],['2016-03-31','2016-03-31'],['2016-04-01','2016-04-30'],['2016-05-01','2016-05-30'],['2016-05-31','2016-05-31'],['2016-06-01','2016-06-30'],['2016-07-01','2016-07-30'],['2016-07-31','2016-07-31'],['2016-08-01','2016-08-30'],['2016-08-31','2016-08-31']]

#dates = [['2016-09-01','2016-09-30'],['2016-10-01','2016-10-30'],['2016-10-31','2016-10-31'],['2016-11-01','2016-11-30'],['2016-12-01','2016-12-30'],['2016-12-31','2016-12-31'],['2017-01-01','2017-01-30'],['2017-01-31','2017-01-31'],['2017-02-01','2017-02-28'],['2017-03-01','2017-03-30'],['2017-03-31','2017-03-31'],['2017-04-01','2017-04-30'],['2017-05-01','2017-05-30'],['2017-05-31','2017-05-31'],['2017-06-01','2017-06-30']]

#dates = [['2017-07-01','2017-07-30'],['2017-07-31','2017-07-31'],['2017-08-01','2017-08-30'],['2017-08-31','2017-08-31'],['2017-09-01','2017-09-30'],['2017-10-01','2017-10-30'],['2017-10-31','2017-10-31'],['2017-11-01','2017-11-30'],['2017-12-01','2017-12-30'],['2017-12-31','2017-12-31']]

get_tradingsymbols = "SELECT * FROM tradingsymbols"

cursor.execute(get_tradingsymbols)
tradingsybols_list = cursor.fetchall()
print("Second_step")

index = 0
flag = 0
for t in tradingsybols_list:
    tradingsymbol_no = t[0]
    tradingsymbol = t[1]
    instrument_token = metaData.getInstrumentToken(tradingsymbol,full_instruments_list)
    for d in dates:
        from_date = d[0]
        to_date = d[1]
        while True:
            try:
                candles = kite.historical_data(instrument_token,from_date,to_date,'minute')
                break
            except Exception as e:
                print(e,instrument_token,from_date,to_date)
        print(tradingsymbol,from_date,to_date)
        for candle in candles:
            cdate = candle['date']
            cdate = datetime(cdate.year,cdate.month,cdate.day,cdate.hour,cdate.minute)
            open = candle['open']
            high = candle['high']
            low = candle['low']
            close = candle['close']
            volume = candle['volume']
            add_candle = "INSERT INTO minute (cdate, tradingsymbol_no, open, high, low, close, volume)  VALUES (%(cdate)s, %(tradingsymbol_no)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s)"
            data_candle = {'cdate':cdate,'tradingsymbol_no':tradingsymbol_no,'open':open,'high':high,'low':low,'close':close,'volume':volume}
            try:
                cursor.execute(add_candle,data_candle)
                index+=1
            except mysql.connector.IntegrityError as err:
                print("Repeated candle",data_candle)
            if(index % 150000 == 0):
                print('Commited candles:',index)
                cnx.commit()
