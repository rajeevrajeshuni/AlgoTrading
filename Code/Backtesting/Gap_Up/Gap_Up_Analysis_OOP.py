import pandas as pd
import os
import BacktestAnlysis


class Tests(object):
    """
        Each function in Tests will only return the stocks picked everyday and the
        capital allocated(as a fraction of total capital) for that instrument for that day.
        It also returns the entry and exit prices and times and profit percent for that instrument.
    """

    """
        In this test we sort the stocks by gap up percent and then
        take only the top 'max_top' stocks in the list.
        Out of that list we remove the outliers and place orders for the rest of them.
        Each order will be placed with capital total_capital/max_top.
    """
    def Test1_omitList(self,files,max_percent,max_top,outliers):
        cwd = os.getcwd()
        picked_stocks = {}
        capital_each_stock = 1/max_top
        for y in files:
            file_name = files[y]
            df = pd.read_csv(file_name)
            df = df[df['Gap_Up_Percent']<=max_percent]
            df_final = df.sort_values(['Date','Gap_Up_Percent'],ascending = [True,False])
            df_final['Trade order in day'] = df_final.groupby('Date').cumcount() + 1
            df_final = df_final[df_final['Trade order in day']<=max_top]
            df_final = self.removeOutliers(df_final,outliers)
            df_final['Capital_Allocated'] = [capital_each_stock]*len(df_final)
            profit_percent_trade = []
            for index in range(0,len(df_final)):
                profit_percent_trade.append(df_final.iloc[index]['Capital_Allocated']*df_final.iloc[index]['Profit_Percent'])
            df_final['Profit_Percent_Capital_Adjusted'] = profit_percent_trade
            picked_stocks[y] = df_final
            folder_path = cwd+'/Test1_omitlist/'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            df_final.to_csv('Test1_omitlist/Gap_Up_Test1_omitList_Trades_Picked_'+str(y)+'_Top_'+str(max_top)+'.csv')
        return picked_stocks

    """
        In this test we remove the outliers
        and sort the rest of stocks by gap up percent and then
        From the remaining stocks take only the top 'max_top' stocks in the list
        and place orders for them.
        Each order will be placed with capital total_capital/max_top.
    """
    def Test2_omitList(self,files,max_percent,max_top,outliers):
        cwd = os.getcwd()
        picked_stocks = {}
        capital_each_stock = 1/max_top
        for y in files:
            file_name = files[y]
            df = pd.read_csv(file_name)
            df = df[df['Gap_Up_Percent']<=max_percent]
            df = self.removeOutliers(df,outliers)
            df_final = df.sort_values(['Date','Gap_Up_Percent'],ascending = [True,False])
            df_final['Trade order in day'] = df_final.groupby('Date').cumcount() + 1
            df_final = df_final[df_final['Trade order in day']<=max_top]
            df_final['Capital_Allocated'] = [capital_each_stock]*len(df_final)
            profit_percent_trade = []
            for index in range(0,len(df_final)):
                profit_percent_trade.append(df_final.iloc[index]['Capital_Allocated']*df_final.iloc[index]['Profit_Percent'])
            df_final['Profit_Percent_Capital_Adjusted'] = profit_percent_trade
            picked_stocks[y] = df_final
            folder_path = cwd+'/Test2_omitlist/'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            df_final.to_csv('Test2_omitlist/Gap_Up_Test2_omitlist_Trades_Picked_'+str(y)+'_Top_'+str(max_top)+'.csv')
        return picked_stocks

    #Calculates the return of each individual stock in top n stocks everyday.
    def Test_top_nth(self,files,max_percent,max_top):
        cwd = os.getcwd()
        picked_stocks = {}
        capital_each_stock = 1
        for y in files:
            file_name = files[y]
            df = pd.read_csv(file_name)
            df = df[df['Gap_Up_Percent']<=max_percent]
            df_final = df.sort_values(['Date','Gap_Up_Percent'],ascending = [True,False])
            df_final['Trade order in day'] = df_final.groupby('Date').cumcount() + 1
            df_final = df_final[df_final['Trade order in day']==max_top]
            df_final['Capital_Allocated'] = [capital_each_stock]*len(df_final)
            profit_percent_trade = []
            for index in range(0,len(df_final)):
                profit_percent_trade.append(df_final.iloc[index]['Capital_Allocated']*df_final.iloc[index]['Profit_Percent'])
            df_final['Profit_Percent_Capital_Adjusted'] = profit_percent_trade
            picked_stocks[y] = df_final
            folder_path = cwd+'/Test_top_nth/'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            df_final.to_csv('Test_top_nth/Gap_Up_Test_top_nth_Trades_Picked_'+str(y)+'_Top_'+str(max_top)+'.csv')
        return picked_stocks

    #Calculate the average return of top n stocks every day
    def Test_topn_average(self,files,max_percent,max_top):
        cwd = os.getcwd()
        picked_stocks = {}
        capital_each_stock = 1/max_top
        for y in files:
            file_name = files[y]
            df = pd.read_csv(file_name)
            df = df[df['Gap_Up_Percent']<=max_percent]
            df_final = df.sort_values(['Date','Gap_Up_Percent'],ascending = [True,False])
            df_final['Trade order in day'] = df_final.groupby('Date').cumcount() + 1
            df_final = df_final[df_final['Trade order in day']<=max_top]
            df_final['Capital_Allocated'] = [capital_each_stock]*len(df_final)
            profit_percent_trade = []
            for index in range(0,len(df_final)):
                profit_percent_trade.append(df_final.iloc[index]['Capital_Allocated']*df_final.iloc[index]['Profit_Percent'])
            df_final['Profit_Percent_Capital_Adjusted'] = profit_percent_trade
            picked_stocks[y] = df_final
            folder_path = cwd+'/Test_topn_average/'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            df_final.to_csv('Test_topn_average/Gap_Up_Test_topn_average_Trades_Picked_'+str(y)+'_Top_'+str(max_top)+'.csv')
        return picked_stocks

    """
        We only choose days where max_top stocks gapped up.
        E.g. if max_top = 1, then we only take days when only one stock gapped up.
        Capital allocated for each stock is 1/max_top.
    """
    def Test_only_topn(self,files,max_percent,max_top,outliers):
        cwd = os.getcwd()
        picked_stocks = {}
        capital_each_stock = 1/max_top
        for y in files:
            file_name = files[y]
            df = pd.read_csv(file_name)
            df = df[df['Gap_Up_Percent']<=max_percent]
            #Selecting only the days where only max_top stocks gapped up.
            series_count = df.groupby('Date').size()
            df_count = pd.DataFrame({'Date':list(series_count.index),'No. of Gapped Up':list(series_count.values)})
            df_count_max_top = df_count[df_count['No. of Gapped Up']==max_top]
            df_final = pd.merge(df,df_count_max_top,on='Date')
            df_final = self.removeOutliers(df_final,outliers)
            df_final['Capital_Allocated'] = [capital_each_stock]*len(df_final)
            profit_percent_trade = []
            for index in range(0,len(df_final)):
                profit_percent_trade.append(df_final.iloc[index]['Capital_Allocated']*df_final.iloc[index]['Profit_Percent'])
            df_final['Profit_Percent_Capital_Adjusted'] = profit_percent_trade
            picked_stocks[y] = df_final
            folder_path = cwd+'/Test_only_topn/'
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            df_final.to_csv('Test_only_topn/Gap_Up_Test_only_topn_Trades_Picked_'+str(y)+'_Top_'+str(max_top)+'.csv')
        return picked_stocks

    def removeOutliers(self,df,outliers):
        removeIndices = []
        for index in range(0,len(df)):
            if df.iloc[index]['Instrument_Token'] in outliers:
                removeIndices.append(index)
        df = df.drop(df.index[removeIndices])
        return df


if __name__ == "__main__":
    files = {2015:'Gap_Up_Backtest_All_FO_2015.csv',2016:'Gap_Up_Backtest_All_FO_2016.csv',2017:'Gap_Up_Backtest_All_FO_2017.csv'}
    max_percent = 2
    max_top = 32
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
    tests = Tests()
    analysis = BacktestAnlysis()

    """
    # Test1 omitlist backtest
    results_file = 'Gap_Up_Test1_OmitList_Summary.csv'
    df = pd.DataFrame([])
    for top in range(1,max_top+1):
        picked_stocks = tests.Test1_omitList(files,max_percent,top,outliers)
        temp = analysis.analyzeTestResults(picked_stocks)
        temp['Top'] = [top]*len(temp)
        df = pd.concat([temp,df])
    df.to_csv(results_file)

    # Test2 omitlist backtest
    results_file = 'Gap_Up_Test2_OmitList_Summary.csv'
    df = pd.DataFrame([])
    for top in range(1,max_top+1):
        picked_stocks = tests.Test2_omitList(files,max_percent,top,outliers)
        temp = analysis.analyzeTestResults(picked_stocks)
        temp['Top'] = [top]*len(temp)
        df = pd.concat([temp,df])
    df.to_csv(results_file)

    # Test top n average
    results_file = 'Gap_Up_Test_topn_average_Summary.csv'
    df = pd.DataFrame([])
    for top in range(1,max_top+1):
        picked_stocks = tests.Test_topn_average(files,max_percent,top)
        temp = analysis.analyzeTestResults(picked_stocks)
        temp['Top'] = [top]*len(temp)
        df = pd.concat([temp,df])
    df.to_csv(results_file)

    # Test top nth
    results_file = 'Gap_Up_Test_top_nth_Summary.csv'
    df = pd.DataFrame([])
    for top in range(1,max_top+1):
        picked_stocks = tests.Test_top_nth(files,max_percent,top)
        temp = analysis.analyzeTestResults(picked_stocks)
        temp['Top'] = [top]*len(temp)
        df = pd.concat([temp,df])
    df.to_csv(results_file)
    """

    # Test only top n average
    results_file = 'Gap_Up_Test_only_topn_Summary.csv'
    df = pd.DataFrame([])
    for top in range(1,max_top+1):
        picked_stocks = tests.Test_only_topn(files,max_percent,top,outliers)
        temp = analysis.analyzeTestResults(picked_stocks)
        temp['Top'] = [top]*len(temp)
        df = pd.concat([temp,df])
    df.to_csv(results_file)
