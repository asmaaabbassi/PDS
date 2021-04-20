import pandas as pd
import csv
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta


stocks_df = pd.read_csv('../data_harvesting/amundi-msci-wrld-ae-c.csv')
cbonds_df = pd.read_csv('../data_harvesting/ishares-global-corporate-bond.csv')
sbonds_df = pd.read_csv('../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv')
gold_df = pd.read_csv('../data_harvesting/spdr-gold-trust.csv')
usd_df = pd.read_csv('../data_harvesting/usdollar.csv')

portfolio_df = pd.read_csv('../portfolio_allocations/portfolio_allocations.csv')

#input data
amount = 100000
inv_date = datetime(2020, 9, 30)
inv_period = 3

print(sbonds_df)
print(portfolio_df.head())

#prices
stocks_index = stocks_df.loc[stocks_df['Date'] == inv_date.strftime('%b %d, %Y')]
if stocks_index.empty:
        print("No price data for date, stocks!")
stocks_price = stocks_index.iloc[0]['Price']

cbonds_index = cbonds_df.loc[cbonds_df['Date'] == inv_date.strftime('%b %d, %Y')]
if cbonds_index.empty:
        print("No price data for date, cbonds!")
cbonds_price = stocks_index.iloc[0]['Price']

sbonds_index = sbonds_df.loc[sbonds_df['Date'] == inv_date.strftime('%b %d, %Y')]
if sbonds_index.empty:
        print("No price data for date!, sbonds")
sbonds_price = sbonds_index.iloc[0]['Price']

gold_index = gold_df.loc[gold_df['Date'] == inv_date.strftime('%b %d, %Y')]
if gold_index.empty:
        print("No price data for date, gold!")
gold_price = gold_index.iloc[0]['Price']

usd_price = 1

print(stocks_price)
print(cbonds_price)
print(sbonds_price)
print(gold_price)

methodsFile = '../trading_methodologies/trading_methodologies.csv'
with open(methodsFile, 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Trading method", "Allocation no", "Asset", "Weight of asset" "Asset price", "Amount to buy ", "Total spending", "Investment period"])

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
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "stocks", row['ST'], stocks_price, stocks_amt, stocks_spend, inv_period]))
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off",  str(index + 1),  "sbonds",row['CB'], cbonds_price, cbonds_amt, cbonds_spend, inv_period]))
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "sbonds", row['PB'], sbonds_price, sbonds_amt, sbonds_spend, inv_period]))
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "gold", row['GO'], gold_price, gold_amt, gold_spend, inv_period]))
    output.append(tuple([inv_date.strftime('%b %d, %Y'),"One-off", str(index + 1),  "cash", row['CA'], usd_price, usd_amt, usd_spend, inv_period]))

    with open(methodsFile, 'a+', newline = '') as file:
        writer = csv.writer(file)
        for x in output:
            writer.writerow(x)
            
#one-off, rebalance

#DCA, no rebalance

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

    allocation_index = row[0]
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
        output.append(tuple([inv_date.strftime('%b %d, %Y'),"DCA", str(index + 1),  "stocks", row['ST'], stocks_price, stocks_sum, stocks_cumm, inv_period]))
        output.append(tuple([inv_date.strftime('%b %d, %Y'),"DCA",  str(index + 1),  "sbonds",row['CB'], cbonds_price, cbonds_sum, cbonds_cumm, inv_period]))
        output.append(tuple([inv_date.strftime('%b %d, %Y'),"DCA", str(index + 1),  "sbonds", row['PB'], sbonds_price, sbonds_sum, sbonds_cumm, inv_period]))
        output.append(tuple([inv_date.strftime('%b %d, %Y'),"DCA", str(index + 1),  "gold", row['GO'], gold_price, gold_sum, gold_cumm, inv_period]))
        output.append(tuple([inv_date.strftime('%b %d, %Y'),"DCA", str(index + 1),  "cash", row['CA'], usd_price, usd_sum, usd_cumm, inv_period]))

        with open(methodsFile, 'a+', newline = '') as file:
                writer = csv.writer(file)
                for x in output:
                    writer.writerow(x)
          
#DCA, rebalance
