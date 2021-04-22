import pandas as pd
import csv
import math
from missing_value import replace

def oneoff(assets, portfolio_df, amount, inv_date, inv_period):
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
        with open(methodsFile, 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Date", "Trading method", "Allocation no", "Asset", "Weight of asset", "Asset price", "Amount to buy", "Total spending", "Investment period"])
        
        for index, row in portfolio_df.iterrows():
            stocks_rate = row['ST']*amount
            cbonds_rate = row['CB']*amount
            sbonds_rate = row['PB']*amount
            gold_rate = row['GO']*amount
            usd_rate = row['CA']*amount
            
            
            #number of assets to buy from each
            
            stocks_amt = math.floor(stocks_rate/stocks_price)
            cbonds_amt = math.floor(cbonds_rate/cbonds_price)
            sbonds_amt = math.floor(sbonds_rate/sbonds_price)
            gold_amt = math.floor(gold_rate/gold_price)
            usd_amt = math.floor(usd_rate/usd_price)
            
            
            #amount of money to invest in each
            
            stocks_spend = round(stocks_amt*stocks_price,2)
            cbonds_spend = round(cbonds_amt*cbonds_price,2)
            sbonds_spend = round(sbonds_amt*sbonds_price,2)
            gold_spend = round(gold_amt*gold_price,2)
            usd_spend = round(usd_amt*usd_price,2)
            
            
            output = []
            output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "stocks", row['ST'], stocks_price, stocks_amt, stocks_spend, inv_period]))
            output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off",  str(index + 1),  "cbonds",row['CB'], cbonds_price, cbonds_amt, cbonds_spend, inv_period]))
            output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "sbonds", row['PB'], sbonds_price, sbonds_amt, sbonds_spend, inv_period]))
            output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "gold", row['GO'], gold_price, gold_amt, gold_spend, inv_period]))
            output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "cash", row['CA'], usd_price, usd_amt, usd_spend, inv_period]))
            
            with open(methodsFile, 'a+', newline = '') as file:
                writer = csv.writer(file)
                for x in output:
                    writer.writerow(x)