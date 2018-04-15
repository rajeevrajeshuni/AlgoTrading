import kiteconnect
import metaData
import numpy as np
import pandas as pd
from datetime import datetime,timedelta

api_key = metaData.getApiKey()
access_token = metaData.getAccessToken()
kite = kiteconnect.KiteConnect(api_key,access_token)

def getReturns(ITC_6month_data,target):
    returns = 0
    ans = []
    for item in ITC_6month_data:
        temp = 'No'
        if item['low'] <= item['open']*(1-(target/100)):
            temp = 'Yes'
        max_stop_loss = ((item['high']-item['low'])*100.0)/item['open']
        if temp=='Yes':
            profit = target
        else:
            profit = -1*max_stop_loss
        returns+=profit
        ans.append({'Date':item['date'].strftime("%Y-%m-%d"),'Success':temp,'Open':item['open'],'Low':item['low'],'High':item['high'],'Max Stop Loss/Loss':max_stop_loss,'Close':item['close'],'Profit':profit})
    df = pd.DataFrame(ans)
    df = df[['Date','Success','Open','Low','High','Max Stop Loss/Loss','Close','Profit']]
    df.to_csv('ITC_180day_backtest_strategy_'+str(target)+'.csv',sep=',')
    print("Total returns:",returns,'for ',target,'%')
    return returns

today = datetime.now()
date_180days_ago = today - timedelta(days=179)
today = today.strftime("%Y-%m-%d")
date_180days_ago = date_180days_ago.strftime("%Y-%m-%d")
ITC_token = 424961
ITC_6month_data = kite.historical_data(ITC_token,date_180days_ago,today,'day')
target = 0.3 #In percent
for i in range(1,10):
    target = i/10
    returns = getReturns(ITC_6month_data,target)
