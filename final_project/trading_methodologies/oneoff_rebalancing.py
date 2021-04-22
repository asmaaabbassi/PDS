import pandas as pd
import csv
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

# Change this with Thomas' missing_values function
stocks_df = pd.read_csv('../data_harvesting/amundi-msci-wrld-ae-c.csv')
cbonds_df = pd.read_csv('../data_harvesting/ishares-global-corporate-bond.csv')
sbonds_df = pd.read_csv('../data_harvesting/db-x-trackers-ii-global-sovereign-5.csv')
gold_df = pd.read_csv('../data_harvesting/spdr-gold-trust.csv')
usd_df = pd.read_csv('../data_harvesting/usdollar.csv')

portfolio_df = pd.read_csv('../portfolio_allocations/portfolio_allocations.csv')

#input data
amount = 100000
inv_date = datetime(2020, 7, 1)
inv_period = 3

methodsFile = '../trading_methodologies/trading_methodologies.csv'

oneoff_df = pd.read_csv('trading_methodologies.csv')
oneoff_df = oneoff_df[oneoff_df['Trading method'] == 'One-off']
oneoff_rebal = oneoff_df.copy()
oneoff_rebal =  oneoff_rebal.replace({"One-off": "Oneoff-rebal"})
assets = ['stocks', 'cbonds', 'sbonds', 'gold', 'cash']

rebal_portofolio = pd.DataFrame(columns=['Date','Trading method', 'Allocation no', 'Asset', 'Weight of asset', 'Asset price', 'Amount to buy', 'Total spending', 'Investment period'])

def new_quantities(allocation, date, prec_portofolio):
    stocks_w = allocation[0]
    cbonds_w = allocation[1]
    sbonds_w = allocation[2]
    gold_w = allocation[3]
    usd_w = allocation[4]

    amount_to_buy = list(prec_portofolio['Amount to buy'])
    stocks_q = amount_to_buy[0]
    cbonds_q = amount_to_buy[1]
    sbonds_q = amount_to_buy[2]
    gold_q = amount_to_buy[3]
    usd_q = amount_to_buy[4]

    stocks_index = stocks_df.loc[stocks_df['Date'] == date.strftime('%b %d, %Y')]
    stocks_price = stocks_index.iloc[0]['Price']
    cbonds_index = cbonds_df.loc[cbonds_df['Date'] == inv_date.strftime('%b %d, %Y')]
    cbonds_price = cbonds_index.iloc[0]['Price']
    sbonds_index = sbonds_df.loc[sbonds_df['Date'] == inv_date.strftime('%b %d, %Y')]
    sbonds_price = sbonds_index.iloc[0]['Price']
    gold_index = gold_df.loc[gold_df['Date'] == inv_date.strftime('%b %d, %Y')]
    gold_price = gold_index.iloc[0]['Price']
    usd_price = 1

    prices = [stocks_price, cbonds_price, sbonds_price, gold_price, usd_price]

    #How much money do I have in total
    total_usd = stocks_q*stocks_price + cbonds_q*cbonds_price + sbonds_q*sbonds_price + gold_q*gold_price + usd_q

    def new_quantity(w, price, total):
        quantity = total*w // price
        return quantity

    new_quantities = []
    for i in range(len(allocation)):
        new_quantities.append(new_quantity(allocation[i], prices[i], total_usd))

    return new_quantities, prices


def rebalancing(allocation_no, allocation, inv_date, nb_months, portofolio):
    rebal_portofolio1 = rebal_portofolio.append(portofolio)
    first_year, first_month = inv_date.year, inv_date.month
    dates = [datetime(first_year, first_month, 15)]
    #Dates à choisir en fonction de s'il existe ou pas
    for i in range(nb_months-1):
        month = inv_date.month + i + 1
        year = first_year + month // 12
        month = month % 12
        if month == 0:
            month = 12
        dates.append(datetime(year, month, 15))
        
    for date in dates:
        prec_portofolio = portofolio[-5:]
        new_portofolio = pd.DataFrame(columns=['Date','Trading method', 'Allocation no', 'Asset', 'Weight of asset', 'Asset price', 'Amount to buy', 'Total spending', 'Investment period'])
        new_quantity, prices = new_quantities(allocation, date, prec_portofolio)
        
        new_portofolio['Date'] = [date.strftime('%b %d, %Y') for _ in range(5)]
        new_portofolio['Trading method'] = ["Oneoff-rebal" for _ in range(5)]
        new_portofolio["Allocation no"] = [allocation_no for _ in range(5)]
        new_portofolio['Asset'] = assets
        new_portofolio['Weight of asset'] = allocation
        new_portofolio['Asset price'] = prices
        new_portofolio['Amount to buy'] = new_quantity
        new_portofolio['Total spending'] = np.multiply(prices, new_quantity)
        new_portofolio['Investment period'] = nb_months

        rebal_portofolio1 = rebal_portofolio1.append(new_portofolio)

    return rebal_portofolio1


#making the real portofolio
rebal_portofolio = pd.DataFrame(columns=['Date','Trading method', 'Allocation no', 'Asset', 'Weight of asset', 'Asset price', 'Amount to buy', 'Total spending', 'Investment period'])

def main():
    for iteration, row in portfolio_df.iterrows():
        print('.', flush=True, end='')
        initial_portofolio = oneoff_df.loc[oneoff_df['Allocation no'] == iteration + 1]
        rebal_portofolio = rebalancing(iteration + 1, list(row[1:]), inv_date, 3, initial_portofolio)
    rebal_portofolio = rebal_portofolio.replace({"One-off": "Oneoff-rebal"}) 
    
    with open(methodsFile, 'a+', newline = '') as file:
        writer = csv.writer(file)
        for x in rebal_portofolio.values.tolist():
            writer.writerow(tuple(x))
    
    print("one-off with rebalance done")
