import pandas as pd
import numpy as np


class BacktestAnalysis(object):
    def max_draw_down(self,profit_percent_day):
        max_negative = 0
        temp_negative = 0
        temp_days = 0
        max_days = 0
        for p in profit_percent_day:
            temp_negative+=p[0]
            temp_days+=1
            if temp_negative > 0:
                temp_negative = 0
                temp_days = 0
            if max_negative > temp_negative:
                max_negative = temp_negative
                max_days = temp_days
        return [max_negative*-1,max_days]

    def win_loss(self,profit_percent_day):
        if len(profit_percent_day) == 0:
            return [0,0]
        profit_percent_arr = np.array(profit_percent_day)
        profit_percent_arr[profit_percent_arr < 0] = -1
        profit_percent_arr[profit_percent_arr > 0] = 0
        loss_percent = (profit_percent_arr.sum()*100)/len(profit_percent_day)
        loss_percent = -1*loss_percent
        return [100-loss_percent,loss_percent]

    #This calculates the R value in kelly's ratio
    def get_R(self,profit_percent_day):
        total_gain = 0
        total_loss = 0
        gain_trades = 0
        loss_trades = 0
        for p in profit_percent_day:
            p = p[0]
            if p < 0:
                total_loss+=p
                loss_trades+=1
            else:
                total_gain+=p
                gain_trades+=1
        if gain_trades == 0 or loss_trades == 0:
            return None
        avg_gain = total_gain/gain_trades
        avg_loss = abs(total_loss/loss_trades)
        if avg_loss == 0:
            return None
        return avg_gain/avg_loss

    """
        The function takes input as list of profit percentages.
        This function returns the total profit for whole time period
        without compounding
    """
    def total_profit(self,profit_percent_day):
        total_profit = 0
        for value in profit_percent_day:
            total_profit+=value[0]
        return total_profit

    """
        The function takes input as list of profit percentages.
        This function assumes that if started with a capital 1 at beginning
        then it returns the final capital you will be end up with
        after for whole time period with compounding.
    """
    def capital_compounded(self,profit_percent_day):
        capital_compounded = 1
        for value in profit_percent_day:
            capital_compounded*=(1+value[0]*0.01)
        return capital_compounded

    """
        The input will be a dictionary with key as time period and
        value as dataframe with all the trades taken throughout the time period.
        From this dataframe we calculate various values like draw down, win loss ratio,
        total profit in the whole dataframe etc.
    """
    def analyzeTestResults(self,picked_stocks):
        df_list = []
        for y in picked_stocks:
            trades = picked_stocks[y]
            trades = trades.groupby('Date').agg({'Profit_Percent_Capital_Adjusted':np.sum})
            profit_percent_day = list(trades.values)
            total_profit = self.total_profit(profit_percent_day)
            capital_compounded = self.capital_compounded(profit_percent_day)
            win_loss_ratio = self.win_loss(profit_percent_day)
            win_loss_ratio[0] = int(win_loss_ratio[0]+0.5)
            win_loss_ratio[1] = int(win_loss_ratio[1]+0.5)
            win_loss_ratio_str = str(win_loss_ratio[0])+":"+str(win_loss_ratio[1])
            R_kelly = self.get_R(profit_percent_day)
            draw_down = self.max_draw_down(profit_percent_day)
            num_trades = len(profit_percent_day)
            df_list.append({'Year':y,'Total Profit Percent':total_profit,'Final Capital(Compounded)':capital_compounded,'Maximum Draw Down':draw_down[0],'Draw Down no. of Days':draw_down[1],'Win Loss Ratio':win_loss_ratio_str,'Kelly Ratio':R_kelly,'Number of days in trade':num_trades})
        return pd.DataFrame(df_list)
