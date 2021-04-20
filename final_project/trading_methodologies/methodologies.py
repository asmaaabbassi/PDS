import pandas as pd
import csv
import math
from datetime import datetime


stocks_df = pd.read_csv('../data_harvesting/amundi-msci-wrld-ae-c.csv')
cbonds_df = pd.read_csv('../data_harvesting/ishares-global-corporate-bond.csv')
sbonds_df = pd.read_csv('../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv')
gold_df = pd.read_csv('../data_harvesting/spdr-gold-trust.csv')
usd_df = pd.read_csv('../data_harvesting/usdollar.csv')

portfolio_df = pd.read_csv('../portfolio_allocations/portfolio_allocations.csv')

#input data
amount = 100000
inv_date = datetime(2020, 12, 30)

print(sbonds_df)
print(portfolio_df.head())

#prices
stocks_index = stocks_df.loc[stocks_df['Date'] == inv_date.strftime('%b %d, %Y')]
if stocks_index.empty:
        print("No price data for date, stocks!")
        return
stocks_price = stocks_index.iloc[0]['Price']

cbonds_index = cbonds_df.loc[cbonds_df['Date'] == inv_date.strftime('%b %d, %Y')]
if cbonds_index.empty:
        print("No price data for date, cbonds!")
        return
cbonds_price = stocks_index.iloc[0]['Price']

sbonds_index = sbonds_df.loc[sbonds_df['Date'] == inv_date.strftime('%b %d, %Y')]
if sbonds_index.empty:
        print("No price data for date!, sbonds")
        return
sbonds_price = sbonds_index.iloc[0]['Price']

gold_index = gold_df.loc[gold_df['Date'] == inv_date.strftime('%b %d, %Y')]
if gold_index.empty:
        print("No price data for date, gold!")
        return
gold_price = gold_index.iloc[0]['Price']

usd_price = 1

print(stocks_price)
print(cbonds_price)
print(sbonds_price)
print(gold_price)

methodsFile = '../trading_methodologies/trading_methodologies.csv'
with open(methodsFile, 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Trading method", "Allocation no", "Asset", "Asset price", "Amount to buy ", "Total spending", "Timeframe"])

#one-off, no rebalance

for index, row in portfolio_df.iterrows():

    allocation_index = row[0]
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
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "stocks", stocks_price, stocks_amt, stocks_spend, ""]))
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "sbonds", cbonds_price, cbonds_amt, cbonds_spend, ""]))
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "sbonds", sbonds_price, sbonds_amt, sbonds_spend, ""]))
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "gold", gold_price, gold_amt, gold_spend, ""]))
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "cash", usd_price, usd_amt, usd_spend, ""]))

    with open(methodsFile, 'a+', newline = '') as file:
        writer = csv.writer(file)
        for x in output:
            writer.writerow(x)
            
#one-off, rebalance



#DCA, no rebal

#DCA, rebal
