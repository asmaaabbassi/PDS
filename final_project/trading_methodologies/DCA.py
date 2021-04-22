import pandas as pd
import csv
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
from missing_value import replace

def DCA(assets, portfolio_df, amount, inv_date, inv_period):
    stocks_df, cbonds_df, sbonds_df, gold_df, usd_df = assets
    
    #prices
    stocks_index = stocks_df.loc[stocks_df['Date'] == inv_date.strftime('%b %d, %Y')]
    if stocks_index.empty:
            print("No price data for date, stocks!")
    stocks_price = stocks_index.iloc[0]['Price']
    
    cbonds_index = cbonds_df.loc[cbonds_df['Date'] == inv_date.strftime('%b %d, %Y')]
    if cbonds_index.empty:
            print("No price data for date, cbonds!")
    cbonds_price = cbonds_index.iloc[0]['Price']
    
    sbonds_index = sbonds_df.loc[sbonds_df['Date'] == inv_date.strftime('%b %d, %Y')]
    if sbonds_index.empty:
            print("No price data for date!, sbonds")
    sbonds_price = sbonds_index.iloc[0]['Price']
    
    gold_index = gold_df.loc[gold_df['Date'] == inv_date.strftime('%b %d, %Y')]
    if gold_index.empty:
            print("No price data for date, gold!")
    gold_price = gold_index.iloc[0]['Price']
    
    usd_price = 1
    
    methodsFile = 'trading_methodologies.csv'
    
    monthly_inv = math.floor(amount/inv_period)
    
    #check data availability for the entire period
    end_date = inv_date + relativedelta(months = inv_period)
    
    if stocks_df.loc[stocks_df['Date'] == end_date.strftime('%b %d, %Y')].empty:
            print("no data for the entire period, stocks")
    if sbonds_df.loc[sbonds_df['Date'] == end_date.strftime('%b %d, %Y')].empty:
            print("no data for the entire period, sbonds")
    if cbonds_df.loc[cbonds_df['Date'] == end_date.strftime('%b %d, %Y')].empty:
            print("no data for the entire period, cbonds")
    if gold_df.loc[gold_df['Date'] == end_date.strftime('%b %d, %Y')].empty:
            print("no data for the entire period, gold")
    
    for index, row in portfolio_df.iterrows():
        stocks_rate = row['ST']
        cbonds_rate = row['CB']
        sbonds_rate = row['PB']
        gold_rate = row['GO']
        usd_rate = row['CA']
    
        stocks_monthly = stocks_rate*monthly_inv
        cbonds_monthly = cbonds_rate*monthly_inv
        sbonds_monthly = sbonds_rate*monthly_inv
        gold_monthly = gold_rate*monthly_inv
        usd_monthly = usd_rate*monthly_inv
    
        stocks_sum = 0
        cbonds_sum = 0
        sbonds_sum = 0
        gold_sum = 0
        usd_sum = 0
    
        stocks_cumm = 0
        cbonds_cumm = 0
        sbonds_cumm = 0
        gold_cumm = 0
        usd_cumm = 0
        
        for x in range(0, inv_period):
                
            curr_date = inv_date + relativedelta(months = x)
    
            stocks_price =  stocks_df.loc[stocks_df['Date'] == curr_date.strftime('%b %d, %Y')].iloc[0]['Price']
            cbonds_price =  cbonds_df.loc[cbonds_df['Date'] == curr_date.strftime('%b %d, %Y')].iloc[0]['Price']
            sbonds_price =  sbonds_df.loc[sbonds_df['Date'] == curr_date.strftime('%b %d, %Y')].iloc[0]['Price']
            gold_price =  gold_df.loc[gold_df['Date'] == curr_date.strftime('%b %d, %Y')].iloc[0]['Price']
            usd_price = 1
    
            stocks_amt = math.floor(stocks_monthly/stocks_price)
            stocks_sum += stocks_amt
            cbonds_amt = math.floor(cbonds_monthly/cbonds_price)
            cbonds_sum += cbonds_amt
            sbonds_amt = math.floor(sbonds_monthly/sbonds_price)
            sbonds_sum += sbonds_amt
            gold_amt = math.floor(gold_monthly/gold_price)
            gold_sum += gold_amt
            usd_amt = math.floor(usd_monthly/usd_price)
            usd_sum += usd_amt
    
             #amount of money to invest in each
    
            stocks_spend = round(stocks_amt*stocks_price,2)
            stocks_cumm += stocks_spend
            cbonds_spend = round(cbonds_amt*cbonds_price,2)
            cbonds_cumm += cbonds_spend
            sbonds_spend = round(sbonds_amt*sbonds_price,2)
            sbonds_cumm += sbonds_spend
            gold_spend = round(gold_amt*gold_price,2)
            gold_cumm += gold_spend
            usd_spend = round(usd_amt*usd_price,2)
            usd_cumm += gold_spend
    
            output = []
            output.append(tuple([curr_date.strftime('%b %d, %Y'),"DCA", str(index + 1),  "stocks", row['ST'], stocks_price, stocks_sum, stocks_cumm, inv_period]))
            output.append(tuple([curr_date.strftime('%b %d, %Y'),"DCA",  str(index + 1),  "cbonds",row['CB'], cbonds_price, cbonds_sum, cbonds_cumm, inv_period]))
            output.append(tuple([curr_date.strftime('%b %d, %Y'),"DCA", str(index + 1),  "sbonds", row['PB'], sbonds_price, sbonds_sum, sbonds_cumm, inv_period]))
            output.append(tuple([curr_date.strftime('%b %d, %Y'),"DCA", str(index + 1),  "gold", row['GO'], gold_price, gold_sum, gold_cumm, inv_period]))
            output.append(tuple([curr_date.strftime('%b %d, %Y'),"DCA", str(index + 1),  "cash", row['CA'], usd_price, usd_sum, usd_cumm, inv_period]))
    
            with open(methodsFile, 'a+', newline = '') as file:
                    writer = csv.writer(file)
                    for x in output:
                        writer.writerow(x)