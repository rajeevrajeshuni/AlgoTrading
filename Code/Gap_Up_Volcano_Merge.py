import pandas as pd
import numpy as np

gap_files = ['Gap_Up_Backtest_All_FO_2015.csv','Gap_Up_Backtest_All_FO_2016.csv','Gap_Up_Backtest_All_FO_2017.csv']
volcano_files = ['Volcano_4_2015.csv','Volcano_4_2016.csv','Volcano_4_2017.csv']
years = [2015,2016,2017]
for i in range(len(gap_files)):
    df_gap = pd.read_csv(gap_files[i])
    df_volcano = pd.read_csv(volcano_files[i])
    df = pd.merge(df_gap,df_volcano,on=['Date','Instrument_Token'])
    file_name = 'Gap_Volcano_'+str(years[i])+'_Data.csv'
    df._csv(file_name,sep=',')
