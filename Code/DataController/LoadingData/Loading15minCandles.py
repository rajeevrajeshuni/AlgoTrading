import sys
sys.path.append('../../')
import mysql.connector
import keys
import pandas as pd
from datetime import datetime
#from mysql.connector import errorcode

file_prefix = "../../"
files = {2015:'2015_15minute.csv',2016:'2016_15minute.csv',2017:'2017_15minute.csv'}
years = list(files.keys())
years.sort()
cnx = mysql.connector.connect(user=keys.getMysqlUser(),password=keys.getMysqlPassword(),database='candles')
cursor = cnx.cursor()

minute15_table = "CREATE TABLE IF NOT EXISTS 15minute (cdate datetime NOT NULL, tradingsymbol_no int(7) NOT NULL,open decimal(7,2) NOT NULL,high decimal(7,2) NOT NULL,low decimal(7,2) NOT NULL,close decimal(7,2) NOT NULL,volume int(12) NOT NULL,PRIMARY KEY (cdate,tradingsymbol_no), KEY cdate (cdate), KEY tradingsymbol_no (tradingsymbol_no), CONSTRAINT tradingsymbol_no_ibfk2 FOREIGN KEY (tradingsymbol_no) REFERENCES tradingsymbols (tradingsymbol_no) ON DELETE CASCADE )"
cursor.execute(minute15_table)

tradingsymbol_table = "CREATE TABLE IF NOT EXISTS tradingsymbols (tradingsymbol_no int(7) NOT NULL AUTO_INCREMENT, tradingsymbol varchar(25) NOT NULL,PRIMARY KEY (tradingsymbol_no), UNIQUE KEY tradingsymbol (tradingsymbol))"
cursor.execute(tradingsymbol_table)

complete_tradingsymbols = []
for y in years:
    print(y)
    file_name = file_prefix+files[y]
    df = pd.read_csv(file_name)
    df = df.sort_values(['tradingsymbol','date'],ascending=(True,True))
    tradingsymbol_list = list(set(df['tradingsymbol'].values))
    for tradingsymbol in tradingsymbol_list:
        if tradingsymbol in complete_tradingsymbols:
            continue
        complete_tradingsymbols.append(tradingsymbol)
        add_tradingsymbol = "INSERT INTO tradingsymbols (tradingsymbol) VALUES (%(tradingsymbol)s)"
        data_tradingsymbol = {'tradingsymbol':tradingsymbol}
        try:
            cursor.execute(add_tradingsymbol,data_tradingsymbol)
            cnx.commit()
        except Exception as err:
            print(err)
    print("Second Step")
    tradingsymbol_list = list(df['tradingsymbol'].values)
    cdate_list = list(df['date'].values)
    close_list = list(df['close'].values)
    open_list = list(df['open'].values)
    high_list = list(df['high'].values)
    low_list = list(df['low'].values)
    volume_list = list(df['volume'].values)
    prev_tradingsymbol = None
    tradingsymbol_no = None
    for index in range(0,len(cdate_list)):
        curr_tradingsymbol = tradingsymbol_list[index]
        if curr_tradingsymbol is not prev_tradingsymbol:
            tradingsymbol_query = "SELECT tradingsymbol_no FROM tradingsymbols WHERE tradingsymbol = %(tradingsymbol)s"
            cursor.execute(tradingsymbol_query,{'tradingsymbol':curr_tradingsymbol})
            tradingsymbol_no = cursor.fetchone()[0]
        cdate = cdate_list[index]
        cdate = datetime(int(cdate[0:4]),int(cdate[5:7]),int(cdate[8:10]),int(cdate[11:13]),int(cdate[14:16]))
        close = close_list[index]
        open = open_list[index]
        high = high_list[index]
        low = low_list[index]
        volume = int(volume_list[index])
        #print(curr_tradingsymbol,tradingsymbol_no)
        add_candle = "INSERT INTO 15minute (cdate, tradingsymbol_no, open, high, low, close, volume)  VALUES (%(cdate)s, %(tradingsymbol_no)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volume)s)"
        data_candle = {'cdate':cdate,'tradingsymbol_no':tradingsymbol_no,'open':open,'high':high,'low':low,'close':close,'volume':volume}
        try:
            cursor.execute(add_candle,data_candle)
        except mysql.connector.IntegrityError as err:
            print("Repeated row")
        prev_tradingsymbol = curr_tradingsymbol
        if(index % 50000 == 0):
            print(index)
            cnx.commit()
