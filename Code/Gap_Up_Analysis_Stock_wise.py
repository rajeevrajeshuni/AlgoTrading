import kiteconnect
import metaData
import corefunctions as core
import keys
import pandas as pd
import numpy as np

access_token = metaData.getAccessToken()
api_key = keys.getApiKey()
kite = kiteconnect.KiteConnect(api_key,access_token)

df = pd.DataFrame({})
lst = ['Gap_Up_Backtest_All_FO_2017.csv','Gap_Up_Backtest_All_FO_2016.csv','Gap_Up_Backtest_All_FO_2015.csv','Gap_Up_Backtest_2018_30_4_18.csv']
for item in lst:
  temp = pd.read_csv(item)
  df = pd.concat([df,temp])
top = 12
max_percent = 2
df = df[['Date','Gap_Up_Percent','Profit_Percent','Trading_Symbol']]
df = df[df['Gap_Up_Percent']<=max_percent]
df_date_sorted = df.sort_values(['Date','Gap_Up_Percent'],ascending = [True,False])
df_date_sorted['Trade order in day'] = df_date_sorted.groupby('Date').cumcount() + 1
df_date_top_gap_up = df_date_sorted[df_date_sorted['Trade order in day']<=top]
df_temp = df_date_top_gap_up[df_date_top_gap_up['Profit_Percent'] == -2]
df_temp = df_temp.groupby('Trading_Symbol').agg({'Profit_Percent':np.size})
df_temp.rename(columns={'Date': 'Number of Days'}, inplace=True)
df_temp.to_csv('Gap_Up_SL_hits_top_'+ str(top) +'.csv')


final_df = df_date_top_gap_up.groupby('Trading_Symbol').agg({'Profit_Percent':np.sum,'Date':np.size})
final_df.rename(columns={'Date': 'Number of Days'}, inplace=True)
final_df.to_csv('Gap_Up_Stock_Wise_Top_'+ str(top) +'.csv')
